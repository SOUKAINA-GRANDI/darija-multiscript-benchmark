import pandas as pd
from math import comb

def mcnemar_exact(b, c):
    """b = arabe seul correct, c = arabizi seul correct."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = 2 * sum(comb(n, i) for i in range(k + 1)) / (2**n)
    return min(1.0, p)

for model, path in [
    ("QWEN 3.8-27B", "results/tables/benchmark_qwen3.8-27b_detail.csv"),
    ("ALLAM-2-7B", "results/tables/benchmark_allam-2-7b_detail.csv")
]:
    print(f"\n=== Test de McNemar (Arabe vs Arabizi) : {model} ===")
    d = pd.read_csv(path, encoding="utf-8-sig")
    for (split, tache), sub in d[d.tache.isin(["qcm", "nli"])].groupby(["split", "tache"]):
        p = sub.pivot_table(index="id", columns="graphie", values="correct", aggfunc="first")
        if {"ar", "lat"}.issubset(p.columns):
            b = int(((p["ar"] == 1) & (p["lat"] == 0)).sum())
            c = int(((p["ar"] == 0) & (p["lat"] == 1)).sum())
            pval = mcnemar_exact(b, c)
            signif = "Significatif (p < 0.05) ✅" if pval < 0.05 else "Non significatif (p >= 0.05) ❌"
            print(f"[{split.upper()}] {tache.upper():<4} : ar_seul={b}, lat_seul={c} | p-valeur = {pval:.4f} -> {signif}")