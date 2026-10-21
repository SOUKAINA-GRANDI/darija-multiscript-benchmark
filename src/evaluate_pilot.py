import sys
import os

# Permet à Python de trouver le dossier prompts/ depuis la racine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import time
import pandas as pd
from dotenv import load_dotenv
from groq import Groq
from prompts.templates import PROMPT_QCM, PROMPT_NLI, PROMPT_CONV_TO_AR, PROMPT_CONV_TO_LAT

load_dotenv()

# Vérifier la clé API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ Veuillez définir GROQ_API_KEY dans votre fichier .env")

client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "qwen/qwen3.8-27b" # Modèle gratuit, rapide et très adapté pour le pilote

PILOT_PATH = "data/pilot/pilot.xlsx"
df = pd.read_excel(PILOT_PATH, dtype=str).fillna("")

results = []

print(f"🚀 Début de l'évaluation sur {len(df)} exemples avec le modèle : {MODEL_NAME}...\n")

for idx, row in df.iterrows():
    tache = row["tache"]
    graphie = row["graphie"]
    item_id = row["id"]
    
    # 1. Préparation du prompt selon la tâche
    if tache == "qcm":
        prompt = PROMPT_QCM.format(
            texte=row["texte"],
            question=row["question"],
            choix_a=row["choix_a"],
            choix_b=row["choix_b"],
            choix_c=row["choix_c"],
            choix_d=row["choix_d"]
        )
    elif tache == "nli":
        prompt = PROMPT_NLI.format(
            texte=row["texte"],
            texte_2=row["texte_2"]
        )
    elif tache == "conversion":
        if graphie == "lat":
            prompt = PROMPT_CONV_TO_AR.format(texte=row["texte"])
        else:
            prompt = PROMPT_CONV_TO_LAT.format(texte=row["texte"])
    else:
        continue

    # 2. Appel au modèle
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0, # Indispensable pour la reproductibilité (mode déterministe)
            max_tokens=100
        )
        prediction = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erreur sur {item_id} [{graphie}] : {e}")
        prediction = "ERROR"

    results.append({
        "id": item_id,
        "tache": tache,
        "graphie": graphie,
        "gold": row["gold"],
        "gold_alt": row.get("gold_alt", ""),
        "prediction": prediction,
        "prompt": prompt
    })
    
    print(f"[{idx+1}/{len(df)}] {item_id} ({tache}-{graphie}) -> Sortie : {prediction[:30]}...")
    time.sleep(0.3)  # Respecter les limites de taux (rate limit)

# 3. Sauvegarder les résultats bruts
os.makedirs("results/raw", exist_ok=True)
out_file = f"results/raw/results_{MODEL_NAME.replace('/', '_')}.json"

with open(out_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n✅ Évaluation terminée ! Résultats bruts enregistrés dans : {out_file}")