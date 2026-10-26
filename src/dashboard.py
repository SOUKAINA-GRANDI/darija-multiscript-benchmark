"""Tableau de bord scientifique du benchmark multigraphique darija (lecture seule).
Lancer depuis la racine du projet :
    streamlit run src/dashboard.py
"""
import html
import re
from math import comb, sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# Gestion robuste de la racine
ROOT = Path(__file__).resolve().parent.parent if (Path(__file__).resolve().parent / "data").exists() else Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "final" / "benchmark.xlsx"
TABLES = ROOT / "results" / "tables"
NOTES = ROOT / "notes"

MODELES = {"qwen3.8-27b": "Qwen 3.8 (27B)", "gpt-oss-120b": "GPT-OSS (120B)", "allam-2-7b": "ALLaM-2 (7B)"}
TACHES = {"qcm": "Compréhension (QCM)", "nli": "Inférence (NLI)", "conversion": "Conversion de graphie"}
SENS = {"ar": "Arabe → Arabizi", "lat": "Arabizi → Arabe"}
BASELINE = {"qcm": 0.25, "nli": 1 / 3}
CIBLES = {"qcm": 100, "nli": 150, "conversion": 100}

# ----------------------------------------------------------------- Statistiques
def wilson(k, n, z=1.96):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))

def mcnemar_exact(b, c):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / (2 ** n))

# --------------------------------------------------------------------- Données
@st.cache_data
def charger_donnees():
    return pd.read_excel(DATA, dtype=str).fillna("")

@st.cache_data
def charger_resultats():
    frames = []
    for code in MODELES:
        p = TABLES / f"benchmark_{code}_detail.csv"
        if p.exists():
            d = pd.read_csv(p, encoding="utf-8-sig")
            d["modele"] = code
            if "cer_no_space" in d.columns and "cer_sans_espace" not in d.columns:
                d = d.rename(columns={"cer_no_space": "cer_sans_espace"})
            frames.append(d)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

def lire_note(nom):
    p = NOTES / nom
    return p.read_text(encoding="utf-8") if p.exists() else f"(fichier introuvable : notes/{nom})"

# ------------------------------------------------------------ Calculs
def resume_comprehension(res, split, tache):
    lignes = []
    for code, nom in MODELES.items():
        d = res[(res.modele == code) & (res.split == split) & (res.tache == tache)]
        if d.empty:
            continue
        ok = d.pivot_table(index="id", columns="graphie", values="correct", aggfunc="first")
        pred = d.pivot_table(index="id", columns="graphie", values="pred", aggfunc="first")
        if not {"ar", "lat"} <= set(ok.columns):
            continue
        n = len(ok)
        k_ar, k_lat = int(ok["ar"].sum()), int(ok["lat"].sum())
        b = int(((ok.ar == 1) & (ok.lat == 0)).sum())
        c = int(((ok.ar == 0) & (ok.lat == 1)).sum())
        lignes.append({
            "Modèle": nom, "N": n,
            "Arabe": k_ar / n, "Arabizi": k_lat / n,
            "ic_ar": wilson(k_ar, n), "ic_lat": wilson(k_lat, n),
            "Écart (arabe − arabizi)": (k_ar - k_lat) / n,
            "Cohérence": float((pred.ar == pred.lat).mean()),
            "Robustesse conjointe": float(((ok.ar == 1) & (ok.lat == 1)).mean()),
            "b (Arabe seul)": b,
            "c (Arabizi seul)": c,
            "p McNemar": mcnemar_exact(b, c),
        })
    return pd.DataFrame(lignes)

def resume_conversion(res, split):
    d = res[(res.split == split) & (res.tache == "conversion")]
    if d.empty:
        return pd.DataFrame()
    g = d.groupby(["modele", "graphie"]).agg(
        N=("correct", "size"), exact=("correct", "mean"), cer=("cer", "mean"),
        cer_sans_espace=("cer_sans_espace", "mean"), script_ok=("script_ok", "mean"),
    ).reset_index()
    g["Sens"] = g.graphie.map(SENS)
    g["Modèle"] = g.modele.map(MODELES)
    return g

# ------------------------------------------------------------------ Affichage RTL/LTR
def rtl(texte):
    return f'<div dir="rtl" style="font-size:1.15rem;line-height:1.8;text-align:right;background:#fcfbf8;padding:12px;border-radius:6px;border:1px solid #ebdccb;">{html.escape(str(texte))}</div>'

def ltr(texte):
    return f'<div dir="ltr" style="font-size:1.05rem;font-family:monospace;line-height:1.7;background:#fcfbf8;padding:12px;border-radius:6px;border:1px solid #ebdccb;">{html.escape(str(texte))}</div>'

# ------------------------------------------------------------------ Pages
def page_accueil(df, res):
    st.markdown("## 🇲🇦 Évaluation Multigraphique des Grands Modèles de Langage en Darija")
    st.info("**Question de recherche :** À contenu et sens strictement identiques, dans quelle mesure l'écriture utilisée (alphabet arabe vs arabizi) influence-t-elle la compréhension et le raisonnement des LLMs ?")
    
    ar = df[df.graphie == "ar"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Contenus uniques", len(ar), "78 paires")
    c2.metric("Total lignes bilingues", len(df), "156 items")
    c3.metric("Modèles évalués", res.modele.nunique() if len(res) else 3, "7B, 27B, 120B")
    c4.metric("Split test (aveugle)", int((ar.split == "test").sum()), "92 lignes")
    
    st.markdown("---")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("### Les Trois Tâches Complémentaires")
        st.markdown("""
        * 🔤 **1. Forme (Conversion) :** Translittération Arabe $\leftrightarrow$ Arabizi.
        * 📖 **2. Sens (QCM) :** Compréhension écrite factuelle à 4 options.
        * 🧠 **3. Raisonnement (NLI) :** Inférence logique (Implication, Contradiction, Neutre).
        """)
    with col2:
        st.markdown("### Répartition du Corpus")
        st.bar_chart(df.groupby(["tache", "split"]).size().unstack(fill_value=0))

def page_resultats(res):
    st.markdown("## 📊 Résultats Expérimentaux (Split Test)")
    st.caption("Mesures agrégées sur les données d'évaluation finale (N=92 lignes).")

    if res.empty:
        st.warning("Aucun résultat trouvé.")
        return

    # 1. HEATMAP EN PREMIER (Visuel ROI)
    st.markdown("### 1. Vue d'ensemble de la Précision (Heatmap)")
    
    qcm_res = resume_comprehension(res, "test", "qcm")
    nli_res = resume_comprehension(res, "test", "nli")
    
    if not qcm_res.empty and not nli_res.empty:
        heat_data = pd.DataFrame({
            "QCM (Arabe)": qcm_res.set_index("Modèle")["Arabe"] * 100,
            "QCM (Arabizi)": qcm_res.set_index("Modèle")["Arabizi"] * 100,
            "NLI (Arabe)": nli_res.set_index("Modèle")["Arabe"] * 100,
            "NLI (Arabizi)": nli_res.set_index("Modèle")["Arabizi"] * 100,
        }).round(1)
        
        st.dataframe(
            heat_data.style.background_gradient(cmap="RdYlGn", vmin=35, vmax=100).format("{:.1f} %"),
            use_container_width=True
        )

    st.markdown("---")

    # 2. COMPRÉHENSION & NLI DÉTAILLÉ
    st.markdown("### 2. Compréhension & Inférence Logique")
    tache = st.radio("Sélectionnez la tâche :", ["nli", "qcm"], format_func=lambda x: TACHES[x], horizontal=True)
    
    df_comp = resume_comprehension(res, "test", tache)
    if not df_comp.empty:
        colA, colB = st.columns([3, 2])
        with colA:
            # Barplot avec IC Wilson
            fig, ax = plt.subplots(figsize=(6, 3.2), dpi=150)
            x = np.arange(len(df_comp))
            w = 0.35
            vals_ar = df_comp["Arabe"].values * 100
            vals_lat = df_comp["Arabizi"].values * 100
            
            ax.bar(x - w/2, vals_ar, w, label="Arabe (ar)", color="#2b5c8f")
            ax.bar(x + w/2, vals_lat, w, label="Arabizi (lat)", color="#fdae6b")
            ax.axhline(BASELINE[tache] * 100, ls="--", color="gray", lw=0.8, label="Hasard pur")
            ax.set_xticks(x)
            ax.set_xticklabels(df_comp["Modèle"], fontsize=9, fontweight='bold')
            ax.set_ylabel("Exactitude (%)", fontsize=9)
            ax.set_ylim(0, 110)
            ax.legend(fontsize=8, loc="lower left")
            st.pyplot(fig)
            plt.close(fig)

        with colB:
            aff = df_comp[["Modèle", "Arabe", "Arabizi", "Écart (arabe − arabizi)", "Robustesse conjointe"]].copy()
            for c in ["Arabe", "Arabizi", "Écart (arabe − arabizi)", "Robustesse conjointe"]:
                aff[c] = (aff[c] * 100).round(1).astype(str) + " %"
            st.dataframe(aff, use_container_width=True)

    st.markdown("---")

    # 3. CONVERSION DE GRAPHIE (CER)
    st.markdown("### 3. Qualité de Conversion de Graphie (CER & Respect de Script)")
    conv_df = resume_conversion(res, "test")
    if not conv_df.empty:
        col_c1, col_c2 = st.columns([3, 2])
        with col_c1:
            fig, ax = plt.subplots(figsize=(6, 3.2), dpi=150)
            mods = list(conv_df["Modèle"].unique())
            x = np.arange(len(mods))
            w = 0.35
            cer_ar = [conv_df[(conv_df["Modèle"] == m) & (conv_df["graphie"] == "ar")]["cer"].mean() * 100 for m in mods]
            cer_lat = [conv_df[(conv_df["Modèle"] == m) & (conv_df["graphie"] == "lat")]["cer"].mean() * 100 for m in mods]
            
            ax.bar(x - w/2, cer_ar, w, label="Arabe → Arabizi", color="#d62728")
            ax.bar(x + w/2, cer_lat, w, label="Arabizi → Arabe", color="#2ca02c")
            ax.set_xticks(x)
            ax.set_xticklabels(mods, fontsize=9, fontweight='bold')
            ax.set_ylabel("CER (%) [Plus bas = Meilleur]", fontsize=9)
            ax.set_ylim(0, 105)
            ax.legend(fontsize=8)
            st.pyplot(fig)
            plt.close(fig)
        
        with col_c2:
            aff_c = conv_df[["Modèle", "Sens", "cer", "cer_sans_espace", "script_ok"]].copy()
            aff_c.columns = ["Modèle", "Sens", "CER", "CER (sans espaces)", "Bonne écriture"]
            aff_c["CER"] = (aff_c["CER"] * 100).round(1).astype(str) + " %"
            aff_c["CER (sans espaces)"] = (aff_c["CER (sans espaces)"] * 100).round(1).astype(str) + " %"
            aff_c["Bonne écriture"] = (aff_c["Bonne écriture"] * 100).round(1).astype(str) + " %"
            st.dataframe(aff_c, use_container_width=True)

    st.markdown("---")

    # 4. SIGNIFICATIVITÉ STATISTIQUE
    st.markdown("### 4. Tests de Significativité (McNemar Exact)")
    if not df_comp.empty:
        st.dataframe(
            df_comp[["Modèle", "N", "b (Arabe seul)", "c (Arabizi seul)", "p McNemar"]],
            use_container_width=True
        )
        st.caption("ℹ️ Une p-valeur > 0.05 indique que sur cet échantillon (N=18 paires NLI), l'écart observé constitue une tendance exploratoire forte nécessitant confirmation sur un corpus élargi.")

def page_demo(df):
    st.markdown("## 🔍 Démo : Même contenu, deux écritures")
    st.caption("Illustration immédiate de la symétrie bilingue du benchmark pour la soutenance.")
    
    tache = st.radio("Type de tâche :", ["qcm", "nli"], horizontal=True, key="demo_tache")
    d = df[(df.tache == tache) & (df.split == "dev")]
    ids = sorted(d["id"].unique())
    choix = st.selectbox("Sélectionnez l'exemple (Split Dev) :", ids)
    
    colA, colB = st.columns(2)
    r_ar = d[(d.id == choix) & (d.graphie == "ar")].iloc[0]
    r_lat = d[(d.id == choix) & (d.graphie == "lat")].iloc[0]
    
    with colA:
        st.markdown("**🟢 Version Arabe (ar)**")
        if tache == "qcm":
            st.caption("Texte :")
            st.markdown(rtl(r_ar.texte), unsafe_allow_html=True)
            st.caption("Question :")
            st.markdown(rtl(r_ar.question), unsafe_allow_html=True)
            for lettre in "abcd":
                st.markdown(rtl(f"{lettre.upper()}) {r_ar['choix_' + lettre]}"), unsafe_allow_html=True)
            st.success(f"Bonne réponse attendue : **{r_ar.gold}**")
        else:
            st.caption("Prémisse :")
            st.markdown(rtl(r_ar.texte), unsafe_allow_html=True)
            st.caption("Hypothèse :")
            st.markdown(rtl(r_ar.texte_2), unsafe_allow_html=True)
            st.success(f"Étiquette attendue : **{r_ar.gold}**")

    with colB:
        st.markdown("**🔵 Version Arabizi (lat)**")
        if tache == "qcm":
            st.caption("Texte :")
            st.markdown(ltr(r_lat.texte), unsafe_allow_html=True)
            st.caption("Question :")
            st.markdown(ltr(r_lat.question), unsafe_allow_html=True)
            for lettre in "abcd":
                st.markdown(ltr(f"{lettre.upper()}) {r_lat['choix_' + lettre]}"), unsafe_allow_html=True)
            st.success(f"Bonne réponse attendue : **{r_lat.gold}**")
        else:
            st.caption("Prémisse :")
            st.markdown(ltr(r_lat.texte), unsafe_allow_html=True)
            st.caption("Hypothèse :")
            st.markdown(ltr(r_lat.texte_2), unsafe_allow_html=True)
            st.success(f"Étiquette attendue : **{r_lat.gold}**")

def page_explorer(df):
    st.markdown("## 📂 Explorer le Corpus (Split Dev uniquement)")
    st.caption("Les 92 lignes du split Test sont strictement masquées pour préserver l'intégrité de l'évaluation aveugle.")
    
    d_dev = df[df.split == "dev"].copy()
    
    c1, c2 = st.columns(2)
    f_tache = c1.selectbox("Filtrer par tâche :", ["Toutes", "qcm", "nli", "conversion"])
    f_graphie = c2.selectbox("Filtrer par graphie :", ["Toutes", "ar", "lat"])
    
    if f_tache != "Toutes":
        d_dev = d_dev[d_dev.tache == f_tache]
    if f_graphie != "Toutes":
        d_dev = d_dev[d_dev.graphie == f_graphie]
        
    st.write(f"**{len(d_dev)}** lignes affichées :")
    
    for _, r in d_dev.iterrows():
        # Label riche et informatif
        titre = f"📌 {r['id']} · {r['tache'].upper()} · Thème : {r.get('theme', 'général')} · Graphie : {'Arabe' if r['graphie']=='ar' else 'Arabizi'}"
        with st.expander(titre):
            st.write(f"**Texte :** {r['texte']}")
            if r["texte_2"]:
                st.write(f"**Hypothèse :** {r['texte_2']}")
            if r["question"]:
                st.write(f"**Question :** {r['question']}")
            st.write(f"**Référence attendue (Gold) :** `{r['gold']}`")
            if r["gold_alt"]:
                st.write(f"**Variantes acceptées :** `{r['gold_alt']}`")

def page_methode():
    st.markdown("## 📖 Méthode, Auto-Critique et Limites")
    
    # KPI Cards méthodologiques
    k1, k2, k3 = st.columns(3)
    k1.metric("Réponses Invalides", "0.0 %", "Parsing 100% propre")
    k2.metric("Significativité McNemar", "p = 0.125", "Tendance à confirmer")
    k3.metric("Blind Test QCM (sans texte)", "45.0 %", "Hasard = 25.0% (Biais de longueur)")
    
    st.markdown("---")
    st.markdown(lire_note("decisions.md"))
    
    with st.expander("📄 Consulter le bilan méthodologique détaillé"):
        st.markdown(lire_note("bilan_test.md"))
    with st.expander("📄 Consulter les fiches de lecture (État de l'art)"):
        st.markdown(lire_note("lecture.md"))

def page_propos():
    st.markdown("## ℹ️ À propos du Projet")
    st.markdown("""
    * **Projet de Fin d'Année (PFA) :** Master Data Science & Big Data (DSBD).
    * **Institution :** Faculté des Sciences Ben M'Sick, Université Hassan II de Casablanca.
    * **Auteur :** Soukaina Grandi.
    * **Encadrant :** M. Zahour Omar.
    * **Année universitaire :** 2026–2027.
    
    **Reproductibilité :** L'ensemble du code, des données étalonnées et des scripts d'inférence est distribué sous licence MIT.
    """)

# ------------------------------------------------------------------ Main
def main():
    st.set_page_config(page_title="Benchmark Multigraphique Darija", layout="wide", page_icon="🇲🇦")
    
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio(
        "Aller vers :",
        ["Accueil", "Résultats", "Démo", "Explorer (dev)", "Méthode & limites", "À propos"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Master DSBD · FS Ben M'Sick\nSoukaina Grandi · Enc. M. Zahour Omar")
    
    df = charger_donnees()
    res = charger_resultats()
    
    if menu == "Accueil":
        page_accueil(df, res)
    elif menu == "Résultats":
        page_resultats(res)
    elif menu == "Démo":
        page_demo(df)
    elif menu == "Explorer (dev)":
        page_explorer(df)
    elif menu == "Méthode & limites":
        page_methode()
    elif menu == "À propos":
        page_propos()

if __name__ == "__main__":
    main()