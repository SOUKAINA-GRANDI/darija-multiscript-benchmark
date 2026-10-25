"""Tableau de bord du benchmark multigraphique darija (lecture seule).

Lancer depuis la racine du projet :
    streamlit run src/dashboard.py

Règle de sécurité : le split `test` n'est JAMAIS détaillé (ni textes, ni réponses
attendues, ni réponses des modèles). Seuls ses scores agrégés sont affichés.
"""
import html
import re
from math import comb, sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "final" / "benchmark.xlsx"
TABLES = ROOT / "results" / "tables"
NOTES = ROOT / "notes"

MODELES = {"qwen3.8-27b": "Qwen3.8-27B", "allam-2-7b": "ALLaM-2-7B", "gpt-oss-120b": "GPT-OSS-120B"}
TACHES = {"qcm": "Compréhension (QCM)", "nli": "Inférence (NLI)", "conversion": "Conversion de graphie"}
SENS = {"ar": "Arabe → Arabizi", "lat": "Arabizi → Arabe"}
BASELINE = {"qcm": 0.25, "nli": 1 / 3}
# Objectifs de volume (à adapter avec ton encadrant)
CIBLES = {"qcm": 100, "nli": 150, "conversion": 100}
# Les items du test ne sont jamais affichés. Ne change pas ceci avant la publication finale.
AFFICHER_ITEMS_TEST = False

NEGATION = re.compile(r"\bما\b|ماشي|حتى|عمرو|بلا")


# ----------------------------------------------------------------- statistiques
def wilson(k, n, z=1.96):
    """Intervalle de confiance de Wilson à 95 % pour une proportion."""
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def mcnemar_exact(b, c):
    """Test de McNemar exact (bilatéral). b : arabe seul correct, c : arabizi seul correct."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


# --------------------------------------------------------------------- données
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


# ------------------------------------------------------------ calculs résultats
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
            "Réussite dans les 2": float(((ok.ar == 1) & (ok.lat == 1)).mean()),
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


# --------------------------------------------------------------------- graphiques
def graphique_comprehension(df, tache, titre):
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    x = np.arange(len(df))
    w = 0.36
    for i, (col, ic, lab, coul) in enumerate(
            [("Arabe", "ic_ar", "Arabe", "#2E74B5"), ("Arabizi", "ic_lat", "Arabizi", "#E07028")]):
        vals = df[col].values * 100
        bas = vals - np.array([t[0] for t in df[ic]]) * 100
        haut = np.array([t[1] for t in df[ic]]) * 100 - vals
        ax.bar(x + (i - 0.5) * w, vals, w, yerr=[bas, haut], capsize=3, label=lab, color=coul)
    ax.axhline(BASELINE[tache] * 100, ls="--", color="grey", lw=1)
    ax.text(len(df) - 0.5, BASELINE[tache] * 100 + 1.5, "hasard", color="grey", ha="right", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(df["Modèle"])
    ax.set_ylim(0, 108)
    ax.set_ylabel("Exactitude (%)")
    ax.set_title(titre, fontsize=11)
    ax.legend(loc="lower right")
    fig.tight_layout()
    return fig


def graphique_conversion(g, titre):
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    modeles = list(g["Modèle"].unique())
    x = np.arange(len(modeles))
    w = 0.36
    for i, (sens, coul) in enumerate([(SENS["ar"], "#2E74B5"), (SENS["lat"], "#E07028")]):
        vals = [g[(g["Modèle"] == m) & (g["Sens"] == sens)].cer.mean() for m in modeles]
        ax.bar(x + (i - 0.5) * w, vals, w, label=sens, color=coul)
    ax.set_xticks(x)
    ax.set_xticklabels(modeles)
    ax.set_ylabel("CER moyen (plus bas = mieux)")
    ax.set_title(titre, fontsize=11)
    ax.legend()
    fig.tight_layout()
    return fig


# ------------------------------------------------------------------ affichage texte
def rtl(texte):
    return f'<div dir="rtl" style="font-size:1.25rem;line-height:1.9">{html.escape(str(texte))}</div>'


def ltr(texte):
    return f'<div style="font-size:1.05rem;font-family:monospace">{html.escape(str(texte))}</div>'


def afficher(texte, graphie):
    st.markdown(rtl(texte) if graphie == "ar" else ltr(texte), unsafe_allow_html=True)


# --------------------------------------------------------------------- diagnostics
def diagnostics(df):
    ar = df[df.graphie == "ar"]
    q = ar[ar.tache == "qcm"]
    n_ = ar[ar.tache == "nli"]
    c_ = ar[ar.tache == "conversion"]
    out = []

    def ajouter(nom, valeur, attendu, ok):
        out.append({"Indicateur": nom, "Valeur": valeur, "Attendu": attendu, "Statut": "OK" if ok else "À améliorer"})

    ajouter("Contenus QCM", len(q), f"≥ {CIBLES['qcm']}", len(q) >= CIBLES["qcm"])
    ajouter("Paires NLI", len(n_), f"≥ {CIBLES['nli']}", len(n_) >= CIBLES["nli"])
    ajouter("Phrases de conversion", len(c_), f"≥ {CIBLES['conversion']}", len(c_) >= CIBLES["conversion"])

    if len(q):
        mots = q.texte.str.split().str.len().mean()
        ajouter("Longueur moyenne des textes QCM (mots)", round(mots, 1), "30 à 70 (indicatif)", 30 <= mots <= 70)

        def plus_long(r):
            L = {x: len(r["choix_" + x.lower()]) for x in "ABCD"}
            m = max(L.values())
            return L[r.gold] == m and list(L.values()).count(m) == 1
        part = q.apply(plus_long, axis=1).mean()
        ajouter("QCM : bonne réponse strictement la plus longue", f"{part:.0%}", "proche de 25 %", part <= 0.35)
        pos = q.gold.value_counts(normalize=True)
        ajouter("QCM : position la plus fréquente de la bonne réponse", f"{pos.max():.0%}", "≤ 35 %", pos.max() <= 0.35)

    if len(n_):
        neg = n_.groupby("gold").apply(lambda d: d.texte_2.str.contains(NEGATION).mean())
        ecart = neg.max() - neg.min()
        ajouter("NLI : écart de fréquence de la négation entre étiquettes", f"{ecart:.0%}", "≤ 20 %", ecart <= 0.20)
        lg = n_.groupby("gold").texte_2.apply(lambda s: s.str.split().str.len().mean())
        ajouter("NLI : longueur moyenne des hypothèses (impl. / contr. / neutre)",
                " / ".join(f"{lg.get(k, float('nan')):.1f}" for k in ["implication", "contradiction", "neutre"]),
                "valeurs proches", (lg.max() - lg.min()) <= 0.8)

    facile = (ar.difficulty == "easy").mean()
    ajouter("Part de contenus « easy »", f"{facile:.0%}", "≤ 60 %", facile <= 0.60)
    relu = (df.reviewed_by != "self").mean()
    ajouter("Lignes relues par une autre personne", f"{relu:.0%}", "≥ 20 %", relu >= 0.20)
    lat2ar = df[(df.tache == "conversion") & (df.graphie == "lat")]
    couv = (lat2ar.gold_alt != "").mean() if len(lat2ar) else 0
    ajouter("Conversion arabizi → arabe : variantes acceptées (gold_alt)", f"{couv:.0%}", "> 0 %", couv > 0)
    return pd.DataFrame(out)


# ---------------------------------------------------------------------- application
def onglet_accueil(df, res):
    st.subheader("Question de recherche")
    st.info("À contenu et sens identiques, dans quelle mesure la graphie (arabe, arabizi) influence-t-elle "
            "la compréhension de la darija marocaine par les grands modèles de langage ?")
    ar = df[df.graphie == "ar"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Contenus", len(ar))
    c2.metric("Lignes (ar + arabizi)", len(df))
    c3.metric("Modèles évalués", res.modele.nunique() if len(res) else 0)
    c4.metric("Split test", int((ar.split == "test").sum()))
    st.markdown("**Trois tâches complémentaires** : la conversion de graphie teste la **forme** (lire l'écriture), "
                "le QCM teste le **sens** (comprendre), le NLI teste le **raisonnement** (déduire).")
    st.subheader("Avancement du corpus (par rapport aux cibles)")
    for t in ["qcm", "nli", "conversion"]:
        n = int((ar.tache == t).sum())
        st.progress(min(1.0, n / CIBLES[t]), text=f"{TACHES[t]} : {n} / {CIBLES[t]}")
    st.warning("Résultats **préliminaires** : corpus petit et split test déjà consulté lors des diagnostics "
               "(voir l'onglet Méthode et limites).")


def onglet_resultats(res):
    if res.empty:
        st.warning("Aucun tableau trouvé dans results/tables/. Lance run_eval.py puis score.py.")
        return
    c1, c2 = st.columns(2)
    split = c1.selectbox("Split", ["dev", "test"], format_func=lambda s: "Développement (dev)" if s == "dev" else "Test (agrégats seulement)")
    tache = c2.selectbox("Tâche", list(TACHES), format_func=lambda t: TACHES[t])

    if tache in ("qcm", "nli"):
        df = resume_comprehension(res, split, tache)
        if df.empty:
            st.info("Pas de résultats pour cette sélection.")
            return
        fig = graphique_comprehension(df, tache, f"{TACHES[tache]} : exactitude par graphie (IC 95 %)")
        st.pyplot(fig)
        plt.close(fig)
        aff = df.drop(columns=["ic_ar", "ic_lat"]).copy()
        for col in ["Arabe", "Arabizi", "Écart (arabe − arabizi)", "Cohérence", "Réussite dans les 2"]:
            aff[col] = (aff[col] * 100).round(1).astype(str) + " %"
        aff["p McNemar"] = aff["p McNemar"].round(3)
        st.dataframe(aff)
        n = int(df["N"].iloc[0])
        st.caption(f"N = {n} contenus par graphie. Barres d'erreur : intervalle de Wilson à 95 %. "
                   "Ligne pointillée : niveau du hasard. Un p McNemar > 0,05 signifie que l'écart entre graphies "
                   "n'est pas statistiquement établi à cette taille d'échantillon.")
        if tache == "nli":
            st.caption("Attention : en NLI, trois hypothèses partagent la même prémisse. Le nombre réel "
                       "d'observations indépendantes est le nombre de prémisses, bien plus petit que N.")
        if (df["Arabe"] >= 0.99).any() or (df["Arabizi"] >= 0.99).any():
            st.warning("Plafond atteint (≈ 100 %) pour au moins un modèle : le test ne discrimine plus. "
                       "Il faut des questions plus difficiles.")
    else:
        g = resume_conversion(res, split)
        if g.empty:
            st.info("Pas de résultats pour cette sélection.")
            return
        fig = graphique_conversion(g, "Conversion de graphie : CER moyen par modèle et par sens")
        st.pyplot(fig)
        plt.close(fig)
        aff = g[["Modèle", "Sens", "N", "exact", "cer", "cer_sans_espace", "script_ok"]].copy()
        aff.columns = ["Modèle", "Sens", "N", "Correspondance exacte", "CER", "CER sans espaces", "Bonne écriture produite"]
        for col in ["Correspondance exacte", "Bonne écriture produite"]:
            aff[col] = (aff[col] * 100).round(1).astype(str) + " %"
        aff["CER"] = aff["CER"].round(3)
        aff["CER sans espaces"] = aff["CER sans espaces"].round(3)
        st.dataframe(aff)
        st.caption("La correspondance exacte est très basse car la darija n'a pas d'orthographe unique : "
                   "le CER est la mesure principale. « Bonne écriture produite » vérifie que la sortie est bien "
                   "dans l'écriture demandée.")


def onglet_donnees(df):
    st.caption("Seuls les items du split dev sont affichés. Les items du test restent masqués.")
    c1, c2 = st.columns(2)
    tache = c1.selectbox("Tâche", list(TACHES), format_func=lambda t: TACHES[t], key="d_tache")
    splits = ["dev"] + (["test"] if AFFICHER_ITEMS_TEST else [])
    d = df[(df.tache == tache) & (df.split.isin(splits))]
    ids = sorted(d.id.unique())
    if not ids:
        st.info("Aucun item.")
        return
    choix = c2.selectbox("Item", ids, key="d_id")
    colA, colB = st.columns(2)
    for col, g, titre in [(colA, "ar", "Écriture arabe"), (colB, "lat", "Arabizi")]:
        r = d[(d.id == choix) & (d.graphie == g)]
        with col:
            st.markdown(f"**{titre}**")
            if r.empty:
                st.write("(variante absente)")
                continue
            r = r.iloc[0]
            if tache == "qcm":
                afficher(r.texte, g)
                afficher(r.question, g)
                for lettre in "abcd":
                    afficher(f"{lettre.upper()}) {r['choix_' + lettre]}", g)
                st.write(f"Bonne réponse : **{r.gold}**")
            elif tache == "nli":
                st.caption("Prémisse")
                afficher(r.texte, g)
                st.caption("Hypothèse")
                afficher(r.texte_2, g)
                st.write(f"Étiquette : **{r.gold}**")
            else:
                st.caption("Entrée")
                afficher(r.texte, g)
                st.caption("Sortie attendue")
                afficher(r.gold, "lat" if g == "ar" else "ar")
                if r.gold_alt:
                    st.caption("Variantes acceptées : " + r.gold_alt.replace("|", "  |  "))
    st.subheader("Répartition du corpus")
    rep = df.groupby(["tache", "split", "graphie"]).size().unstack("graphie", fill_value=0)
    st.dataframe(rep)
    st.write("Difficulté (déclarée) :", df[df.graphie == "ar"].difficulty.value_counts().to_dict())


def onglet_reponses(res):
    st.caption("Réponses des modèles sur le split dev uniquement.")
    if res.empty:
        st.warning("Aucun résultat.")
        return
    c1, c2, c3 = st.columns(3)
    modele = c1.selectbox("Modèle", list(MODELES), format_func=lambda m: MODELES[m], key="r_m")
    tache = c2.selectbox("Tâche", list(TACHES), format_func=lambda t: TACHES[t], key="r_t")
    erreurs = c3.checkbox("Erreurs seulement", key="r_e")
    splits = ["dev"] + (["test"] if AFFICHER_ITEMS_TEST else [])
    d = res[(res.modele == modele) & (res.tache == tache) & (res.split.isin(splits))].copy()
    if erreurs:
        d = d[d.correct == 0]
    cols = ["id", "graphie", "pred", "gold", "correct"] + (["cer"] if tache == "conversion" else [])
    st.write(f"{len(d)} lignes")
    st.dataframe(d[cols].sort_values(["id", "graphie"]))


def onglet_qualite(df):
    diag = diagnostics(df)
    st.dataframe(diag)
    nb = int((diag.Statut != "OK").sum())
    st.warning(f"{nb} indicateur(s) à améliorer sur {len(diag)}.") if nb else st.success("Tous les indicateurs sont OK.")
    st.caption("Ces indicateurs repèrent les raccourcis que les modèles peuvent exploiter "
               "(longueur des réponses, négation, déséquilibres) et les écarts avec les cibles de volume.")


def onglet_methode():
    st.markdown(lire_note("decisions.md"))
    with st.expander("Bilan méthodologique"):
        st.markdown(lire_note("bilan_test.md"))
    with st.expander("Bilan du pilote"):
        st.markdown(lire_note("pilote_bilan.md"))


def main():
    st.set_page_config(page_title="Benchmark multigraphique darija", layout="wide")
    st.title("Benchmark multigraphique pour LLM en darija marocaine")
    st.caption("PFA, Master DSBD, Faculté des Sciences Ben M'Sick. Tableau de bord en lecture seule.")
    if not DATA.exists():
        st.error(f"Fichier introuvable : {DATA}. Lance la commande depuis la racine du projet.")
        return
    df = charger_donnees()
    res = charger_resultats()
    onglets = st.tabs(["Accueil", "Résultats", "Données (dev)", "Réponses des modèles (dev)",
                       "Qualité du corpus", "Méthode et limites"])
    with onglets[0]:
        onglet_accueil(df, res)
    with onglets[1]:
        onglet_resultats(res)
    with onglets[2]:
        onglet_donnees(df)
    with onglets[3]:
        onglet_reponses(res)
    with onglets[4]:
        onglet_qualite(df)
    with onglets[5]:
        onglet_methode()


if __name__ == "__main__":
    main()