import re, sys, json, unicodedata, os
import pandas as pd
from sklearn.metrics import f1_score
from rapidfuzz.distance import Levenshtein

if len(sys.argv) < 3:
    print("Usage: python src/score.py <fichier_data.xlsx> <fichier_raw.jsonl>")
    sys.exit(1)

DATA, RAW = sys.argv[1], sys.argv[2]
gold = pd.read_excel(DATA, dtype=str).fillna("")
raw = pd.DataFrame([json.loads(l) for l in open(RAW, encoding="utf-8") if l.strip()])
df = raw.merge(gold[["id", "graphie", "gold", "gold_alt"]], on=["id", "graphie"])

def nettoyer(t):
    t = re.sub(r"<think>.*?</think>", "", t, flags=re.S)   # cas des modèles raisonnants type DeepSeek/Qwen
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
        for lab in ["contradiction", "implication", "neutre"]:
            if lab in t2:
                return lab
        return "INVALIDE"
    # Pour conversion : on prend la 1ère ligne
    return t.splitlines()[0].strip() if t else "INVALIDE"

def norm(t):
    t = unicodedata.normalize("NFC", t.lower())
    t = re.sub(r"[أإآ]", "ا", t)
    t = re.sub(r"[?.,!؟،]", "", t)
    return re.sub(r"\s+", " ", t).strip()

df["pred"] = df.apply(extraire, axis=1)

def evaluer(r):
    if r["tache"] != "conversion":
        return pd.Series({"correct": int(r["pred"] == r["gold"]), "cer": None})
    refs = [r["gold"]] + [g for g in r["gold_alt"].split("|") if g]
    p = norm(r["pred"])
    cer = min(Levenshtein.distance(p, norm(g)) / max(len(norm(g)), 1) for g in refs)
    return pd.Series({"correct": int(any(p == norm(g) for g in refs)), "cer": round(cer, 3)})

df[["correct", "cer"]] = df.apply(evaluer, axis=1)

print("\n" + "=" * 55)
print("=== SCORE PAR TÂCHE ET GRAPHIE ===")
print("=" * 55)
print(df.groupby(["tache", "graphie"]).agg(
    n=("correct", "size"),
    accuracy=("correct", "mean"),
    invalides=("pred", lambda s: (s == "INVALIDE").sum()),
    cer=("cer", "mean")
).round(3))

nli = df[df.tache == "nli"]
if len(nli):
    print("\n=== Macro-F1 NLI ===")
    for g, sub in nli.groupby("graphie"):
        print(f"Graphie [{g}] :", round(f1_score(sub["gold"], sub["pred"], average="macro"), 3))

print("\n=== COHÉRENCE ENTRE GRAPHIES (ar vs lat) ===")
for t in ["qcm", "nli"]:
    p = df[df.tache == t].pivot_table(index="id", columns="graphie", values="pred", aggfunc="first")
    if {"ar", "lat"} <= set(p.columns):
        taux_coherence = (p['ar'] == p['lat']).mean()
        print(f"Tâche {t.upper()} : {round(taux_coherence * 100, 1)}% de réponses identiques")

os.makedirs("results/tables", exist_ok=True)
out = RAW.replace("results/raw", "results/tables").replace(".jsonl", "_detail.csv")
df.drop(columns=["prompt"]).to_csv(out, index=False, encoding="utf-8-sig")
print(f"\n📊 Fichier de détail généré : {out}")