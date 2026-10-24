import re, sys, json, unicodedata, os
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score
from rapidfuzz.distance import Levenshtein

if len(sys.argv) < 3:
    print("Usage: python src/score.py <data.xlsx> <raw.jsonl>")
    sys.exit(1)

DATA, RAW = sys.argv[1], sys.argv[2]
gold = pd.read_excel(DATA, dtype=str).fillna("")

# Ne charger que la DERNIÈRE réponse valide pour chaque (id, graphie)
raw_dict = {}
for line in open(RAW, encoding="utf-8"):
    if line.strip():
        j = json.loads(line)
        if not j.get("erreur"):
            raw_dict[(j["id"], j["graphie"])] = j

raw = pd.DataFrame(list(raw_dict.values()))

# On inclut 'tache' dans le "on" pour éviter les doublons tache_x / tache_y
df = raw.merge(
    gold[["id", "tache", "graphie", "split", "gold", "gold_alt"]],
    on=["id", "tache", "graphie"],
    how="left"
)

ARABIC_REGEX = re.compile(r"[\u0600-\u06FF]")

def nettoyer(t):
    t = re.sub(r"<think>.*?</think>", "", t, flags=re.S)
    t = re.sub(r"[*`#]", "", t)
    t = re.sub(r"^(réponse|conversion|arabizi|answer)\s*:\s*", "", t.strip(), flags=re.I)
    return t.strip()

def extraire(r):
    t = nettoyer(r["reponse_brute"])
    if r["tache"] == "qcm":
        m = re.search(r"\b([ABCD])\b", t)
        return m.group(1) if m else "INVALIDE"
    
    if r["tache"] == "nli":
        t2 = t.lower()
        # Prendre le premier label qui apparaît chronologiquement
        pos = {l: t2.find(l) for l in ["implication", "contradiction", "neutre"] if l in t2}
        return min(pos, key=pos.get) if pos else "INVALIDE"
        
    return t.splitlines()[0].strip() if t else "INVALIDE"

def norm(t, sans_espace=False):
    t = unicodedata.normalize("NFC", str(t).lower())
    # 1. Enlever voyelles brèves arabes (harakat) et tatweel
    t = re.sub(r"[\u064B-\u0652\u0640]", "", t)
    # 2. Normalisation des alefs
    t = re.sub(r"[أإآ]", "ا", t)
    # 3. Enlever ponctuation et apostrophes/tirets
    t = re.sub(r"['’\-?.,!؟،;]", "", t)
    if sans_espace:
        return re.sub(r"\s+", "", t).strip()
    return re.sub(r"\s+", " ", t).strip()

df["pred"] = df.apply(extraire, axis=1)

def evaluer(r):
    if r["tache"] != "conversion":
        return pd.Series({"correct": int(r["pred"] == r["gold"]), "cer": None, "cer_no_space": None, "script_ok": None})
    
    refs = [r["gold"]] + [g for g in str(r["gold_alt"]).split("|") if g]
    p_norm = norm(r["pred"])
    p_no_sp = norm(r["pred"], sans_espace=True)
    
    cer = min(Levenshtein.distance(p_norm, norm(g)) / max(len(norm(g)), 1) for g in refs)
    cer_ns = min(Levenshtein.distance(p_no_sp, norm(g, sans_espace=True)) / max(len(norm(g, sans_espace=True)), 1) for g in refs)
    
    cible_arabe = (r["graphie"] == "lat")
    a_lettres_arabes = bool(ARABIC_REGEX.search(str(r["pred"])))
    script_ok = int(a_lettres_arabes == cible_arabe)
    
    return pd.Series({
        "correct": int(any(p_norm == norm(g) for g in refs)),
        "cer": round(cer, 3),
        "cer_no_space": round(cer_ns, 3),
        "script_ok": script_ok
    })

df[["correct", "cer", "cer_no_space", "script_ok"]] = df.apply(evaluer, axis=1)

print("\n" + "=" * 80)
print("=== 1. SCORES OFFICIELS PAR SPLIT, TÂCHE ET GRAPHIE ===")
print("=== (Ligne de base aléatoire : QCM = 25.0% | NLI = 33.3%) ===")
print("=" * 80)
scores = df.groupby(["split", "tache", "graphie"]).agg(
    n=("correct", "size"),
    accuracy=("correct", "mean"),
    invalides=("pred", lambda s: (s == "INVALIDE").sum()),
    cer=("cer", "mean"),
    cer_sans_espace=("cer_no_space", "mean"),
    script_ok=("script_ok", "mean")
).round(3)
print(scores)

print("\n" + "=" * 80)
print("=== 2. MACRO-F1 NLI PAR SPLIT ET GRAPHIE ===")
print("=" * 80)
nli = df[df["tache"] == "nli"]
for (split, graphie), sub in nli.groupby(["split", "graphie"]):
    score_f1 = f1_score(
        sub["gold"], sub["pred"],
        labels=["implication", "contradiction", "neutre"],
        average="macro", zero_division=0
    )
    print(f"[{split.upper()}] Graphie {graphie} : F1 = {score_f1:.3f}")

print("\n" + "=" * 80)
print("=== 3. COHÉRENCE ET ROBUSTESSE CONJOINTE (ar ET lat réussis) ===")
print("=" * 80)
for split in ["dev", "test"]:
    for tache in ["qcm", "nli"]:
        sub = df[(df["split"] == split) & (df["tache"] == tache)]
        p_pred = sub.pivot_table(index="id", columns="graphie", values="pred", aggfunc="first")
        p_corr = sub.pivot_table(index="id", columns="graphie", values="correct", aggfunc="first")
        
        if {"ar", "lat"}.issubset(p_pred.columns):
            coherence = (p_pred["ar"] == p_pred["lat"]).mean()
            robustesse = ((p_corr["ar"] == 1) & (p_corr["lat"] == 1)).mean()
            print(f"[{split.upper()}] {tache.upper():<4} | Cohérence : {coherence:.1%} | Robustesse conjointe : {robustesse:.1%}")

os.makedirs("results/tables", exist_ok=True)
out = RAW.replace("results/raw", "results/tables").replace(".jsonl", "_detail.csv")
df.drop(columns=["prompt", "reponse_brute"], errors="ignore").to_csv(out, index=False, encoding="utf-8-sig")
print(f"\n📁 Fichier de détail mis à jour : {out}")