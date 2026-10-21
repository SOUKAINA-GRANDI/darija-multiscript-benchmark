import os, sys, json, re
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROMPT_TPL = open("prompts/qcm_sans_texte.txt", encoding="utf-8").read()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

df = pd.read_excel("data/final/benchmark.xlsx", dtype=str).fillna("")
# On teste UNIQUEMENT sur le dev
qcm_dev = df[(df.tache == "qcm") & (df.split == "dev")].copy()

correct = 0
total = len(qcm_dev)

print(f"Lancement du test aveugle (sans texte) sur {total} QCM de développement...")

for _, r in qcm_dev.iterrows():
    p = PROMPT_TPL.format(
        question=r["question"],
        choix_a=r["choix_a"], choix_b=r["choix_b"],
        choix_c=r["choix_c"], choix_d=r["choix_d"]
    )
    rep = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[{"role": "user", "content": p}],
        temperature=0.0
    )
    ans = rep.choices[0].message.content.strip()
    m = re.search(r"\b([ABCD])\b", ans)
    pred = m.group(1) if m else ""
    if pred == r["gold"]:
        correct += 1

acc = (correct / total) * 100
print(f"\nRésultat QCM sans texte (Dev) : {correct}/{total} ({acc:.1f}%)")
print(f"Rappel de référence : Choix purement aléatoire = 25.0%")