import os, sys, json, time
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

load_dotenv()

# Récupérer la clé Gemini
GEMINI_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not GEMINI_KEY:
    raise ValueError("❌ Veuillez définir GEMINI_API_KEY ou GOOGLE_API_KEY dans votre fichier .env")

# Google expose une API 100% compatible OpenAI officielle
client = OpenAI(
    api_key=GEMINI_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

MODEL_NAME = "gemini-3.8-flash"
DATA = "data/final/benchmark.xlsx"
OUT = f"results/raw/benchmark_{MODEL_NAME}.jsonl"
PAUSE = 1.0

PROMPTS = {t: open(f"prompts/{t}.txt", encoding="utf-8").read()
           for t in ["qcm", "nli", "conversion"]}

def build_prompt(r):
    if r["tache"] == "conversion":
        cible = "l'arabizi (lettres latines)" if r["graphie"] == "ar" else "l'écriture arabe"
        return PROMPTS["conversion"].format(cible=cible, texte=r["texte"])
    return PROMPTS[r["tache"]].format(**r)

# Cache
done = set()
if os.path.exists(OUT):
    with open(OUT, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                j = json.loads(line)
                done.add((j["id"], j["graphie"]))

df = pd.read_excel(DATA, dtype=str).fillna("")
todo = [r for _, r in df.iterrows() if (r["id"], r["graphie"]) not in done]
print(f"Modèle : {MODEL_NAME} | {len(todo)} items à évaluer ({len(done)} déjà en cache)")

os.makedirs("results/raw", exist_ok=True)
with open(OUT, "a", encoding="utf-8") as out:
    for r in tqdm(todo):
        prompt = build_prompt(r)
        reponse, erreur = "", ""
        for essai in range(3):
            try:
                rep = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                )
                reponse = rep.choices[0].message.content or ""
                erreur = ""
                break
            except Exception as e:
                erreur = str(e)
                time.sleep(3 * (essai + 1))
        
        out.write(json.dumps({
            "id": r["id"], "tache": r["tache"], "graphie": r["graphie"],
            "modele": MODEL_NAME, "model_id": MODEL_NAME,
            "date": datetime.now().isoformat(timespec="seconds"),
            "temperature": 0.0, "prompt": prompt,
            "reponse_brute": reponse, "erreur": erreur,
        }, ensure_ascii=False) + "\n")
        out.flush()
        time.sleep(PAUSE)

print(f"\n✅ Réponses enregistrées dans : {OUT}")