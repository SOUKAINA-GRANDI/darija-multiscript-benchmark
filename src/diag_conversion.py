import re
import pandas as pd

def tester_conversion(csv_path, nom_modele):
    d = pd.read_csv(csv_path, encoding="utf-8-sig")
    c = d[(d.tache == "conversion") & (d.split == "test")].copy()

    ARAB = r"[\u0600-\u06FF]"
    c["cible_arabe"] = c["graphie"].eq("lat")  # Si entrée = lat, la sortie attendue doit être arabe
    c["script_ok"] = c.apply(
        lambda r: bool(re.search(ARAB, str(r["pred"]))) == r["cible_arabe"], axis=1
    )

    print(f"\n{'='*20} {nom_modele} {'='*20}")
    print("Taux de sorties dans la bonne écriture (script_ok) :")
    print(c.groupby("graphie")["script_ok"].mean().round(3))
    print("\nÉchantillon des prédictions vs gold (test) :")
    print(c[["id", "graphie", "pred", "gold"]].head(6).to_string())

tester_conversion("results/tables/benchmark_qwen3.8-27b_detail.csv", "QWEN 3.8-27B")
tester_conversion("results/tables/benchmark_allam-2-7b_detail.csv", "ALLAM-2-7B")