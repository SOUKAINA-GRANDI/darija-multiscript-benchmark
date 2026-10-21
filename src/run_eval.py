import os, sys, json, time
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

load_dotenv()

MODELS = {
    "qwen3.8-27b":  {"key": "GROQ_API_KEY", "base_url": "https://api.groq.com/openai/v1",
                     "model": "qwen/qwen3.8-27b"},
    "allam-2-7b":   {"key": "GROQ_API_KEY", "base_url": "https://api.groq.com/openai/v1",
                     "model": "allam-2-7b"},
    "gpt-oss-120b": {"key": "GROQ_API_KEY", "base_url": "https://api.groq.com/openai/v1",
                     "model": "openai/gpt-oss-120b"},
}

DATA = sys.argv[1] if len(sys.argv) > 1 else "data/pilot/pilot.xlsx"
MODEL_NAME = sys.argv[2] if len(sys.argv) > 2 else "qwen3.8-27b"

if MODEL_NAME not in MODELS:
    raise ValueError(f"Modèle inconnu : {MODEL_NAME}. Choisis parmi : {list(MODELS.keys())}")

os.makedirs("results/raw", exist_ok=True)
OUT = f"results/raw/{os.path.basename(DATA).split('.')[0]}_{MODEL_NAME}.jsonl"
PAUSE = 1.5  # Pause pour respecter le quota Groq

PROMPTS = {t: open(f"prompts/{t}.txt", encoding="utf-8").read()
           for t in ["qcm", "nli", "conversion"]}

def build_prompt(r):
    if r["tache"] == "conversion":
        cible = "l'arabizi (lettres latines)" if r["graphie"] == "ar" else "l'écriture arabe"
        return PROMPTS["conversion"].format(cible=cible, texte=r["texte"])
    return PROMPTS[r["tache"]].format(**r)

# Système de cache (pour reprendre si coupure réseau ou quota atteint)
done = set()
if os.path.exists(OUT):
    with open(OUT, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                j = json.loads(line)
                done.add((j["id"], j["graphie"]))

cfg = MODELS[MODEL_NAME]
client = OpenAI(api_key=os.getenv(cfg["key"]), base_url=cfg["base_url"])
df = pd.read_excel(DATA, dtype=str).fillna("")
todo = [r for _, r in df.iterrows() if (r["id"], r["graphie"]) not in done]
print(f"Modèle : {MODEL_NAME} | {len(todo)} items à évaluer ({len(done)} déjà en cache)")

with open(OUT, "a", encoding="utf-8") as out:
    for r in tqdm(todo):
        prompt = build_prompt(r)
        reponse, erreur = "", ""
        for essai in range(3):
            try:
                rep = client.chat.completions.create(
                    model=cfg["model"],
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                )
                reponse = rep.choices[0].message.content or ""
                erreur = ""
                break
            except Exception as e:
                erreur = str(e)
                time.sleep(5 * (essai + 1))
        
        out.write(json.dumps({
            "id": r["id"], "tache": r["tache"], "graphie": r["graphie"],
            "modele": MODEL_NAME, "model_id": cfg["model"],
            "date": datetime.now().isoformat(timespec="seconds"),
            "temperature": 0.0, "prompt": prompt,
            "reponse_brute": reponse, "erreur": erreur,
        }, ensure_ascii=False) + "\n")
        out.flush()
        time.sleep(PAUSE)

print(f"\n✅ Réponses enregistrées dans : {OUT}")