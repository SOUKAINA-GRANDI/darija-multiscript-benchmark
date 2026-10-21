import re, sys, json, unicodedata, os
import pandas as pd
from sklearn.metrics import f1_score
from rapidfuzz.distance import Levenshtein

if len(sys.argv) < 3:
    print("Usage: python src/score.py <data.xlsx> <raw.jsonl>")
    sys.exit(1)

DATA, RAW = sys.argv[1], sys.argv[2]
gold = pd.read_excel(DATA, dtype=str).fillna("")
raw = pd.DataFrame([json.loads(l) for l in open(RAW, encoding="utf-8") if l.strip()])

ARABIC_REGEX = re.compile(r"[\u0600-\u06FF]")

df = raw.merge(
    gold[["id", "tache", "graphie", "split", "gold", "gold_alt"]],
    on=["id", "tache", "graphie"],
    how="left"
)

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
        for lab in ["contradiction", "implication", "neutre"]:
            if lab in t2:
                return lab
        return "INVALIDE"
    return t.splitlines()[0].strip() if t else "INVALIDE"

def norm(t):
    t = unicodedata.normalize("NFC", t.lower())
    t = re.sub(r"[أإآ]", "ا", t)
    t = re.sub(r"[?.,!؟،]", "", t)
    return re.sub(r"\s+", " ", t).strip()

df["pred"] = df.apply(extraire, axis=1)

def evaluer(r):
    if r["tache"] != "conversion":
        return pd.Series({"correct": int(r["pred"] == r["gold"]), "cer": None, "script_ok": None})
    
    refs = [r["gold"]] + [g for g in r["gold_alt"].split("|") if g]
    p = norm(r["pred"])
    cer = min(Levenshtein.distance(p, norm(g)) / max(len(norm(g)), 1) for g in refs)
    
    cible_arabe = (r["graphie"] == "lat")
    a_lettres_arabes = bool(ARABIC_REGEX.search(str(r["pred"])))
    script_ok = int(a_lettres_arabes == cible_arabe)
    
    return pd.Series({
        "correct": int(any(p == norm(g) for g in refs)),
        "cer": round(cer, 3),
        "script_ok": script_ok
    })

df[["correct", "cer", "script_ok"]] = df.apply(evaluer, axis=1)

print("\n" + "=" * 70)
print("=== 1. SCORE PAR SPLIT, TÂCHE ET GRAPHIE ===")
print("=" * 70)
scores = df.groupby(["split", "tache", "graphie"]).agg(
    n=("correct", "size"),
    accuracy=("correct", "mean"),
    invalides=("pred", lambda s: (s == "INVALIDE").sum()),
    cer=("cer", "mean"),
    script_ok=("script_ok", "mean")
).round(3)
print(scores)

print("\n" + "=" * 70)
print("=== 2. MACRO-F1 NLI PAR SPLIT ET GRAPHIE ===")
print("=" * 70)
nli = df[df["tache"] == "nli"]
for (split, graphie), sub in nli.groupby(["split", "graphie"]):
    score_f1 = f1_score(
        sub["gold"],
        sub["pred"],
        labels=["implication", "contradiction", "neutre"],
        average="macro",
        zero_division=0
    )
    print(f"[{split.upper()}] Graphie {graphie} : F1 = {score_f1:.3f}")

print("\n" + "=" * 70)
print("=== 3. COHÉRENCE ENTRE GRAPHIES (ar == lat) ===")
print("=" * 70)
for split in ["dev", "test"]:
    for tache in ["qcm", "nli"]:
        sub = df[(df["split"] == split) & (df["tache"] == tache)]
        pivot = sub.pivot_table(index="id", columns="graphie", values="pred", aggfunc="first")
        if {"ar", "lat"}.issubset(pivot.columns):
            coherence = (pivot["ar"] == pivot["lat"]).mean()
            print(f"[{split.upper()}] {tache.upper()} : {coherence:.1%} de réponses identiques")

print("\n" + "=" * 70)
print("=== 4. RÉUSSITE CONJOINTE DANS LES DEUX GRAPHIES (ROBUSTESSE) ===")
print("=" * 70)
for split in ["dev", "test"]:
    for tache in ["qcm", "nli"]:
        sub = df[(df["split"] == split) & (df["tache"] == tache)]
        pivot = sub.pivot_table(index="id", columns="graphie", values="correct", aggfunc="first")
        if {"ar", "lat"}.issubset(pivot.columns):
            robustesse = ((pivot["ar"] == 1) & (pivot["lat"] == 1)).mean()
            print(f"[{split.upper()}] {tache.upper()} : {robustesse:.1%} réussis dans les 2 graphies à la fois")

os.makedirs("results/tables", exist_ok=True)
out = RAW.replace("results/raw", "results/tables").replace(".jsonl", "_detail.csv")
df.drop(columns=["prompt"]).to_csv(out, index=False, encoding="utf-8-sig")
print(f"\n📁 Fichier de détail mis à jour : {out}")