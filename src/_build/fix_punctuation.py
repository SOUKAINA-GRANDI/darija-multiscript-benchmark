import pandas as pd

PATH = "data/final/benchmark.xlsx"
df = pd.read_excel(PATH, dtype=str).fillna("")

cols_to_fix = ["texte", "texte_2", "question", "choix_a", "choix_b", "choix_c", "choix_d", "gold", "gold_alt"]
for c in cols_to_fix:
    if c in df.columns:
        df[c] = df[c].str.replace("،", ",", regex=False)
        df[c] = df[c].str.replace("؟", "?", regex=False)
        df[c] = df[c].str.replace("؛", ";", regex=False)

df.to_excel(PATH, index=False)
print("✅ Ponctuation uniformisée avec succès dans benchmark.xlsx !")