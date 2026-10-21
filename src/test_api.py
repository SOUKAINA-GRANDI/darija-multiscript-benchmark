import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROMPT = "Convertis en arabizi : عجبني هاد الفيلم بزاف"

# Noms de modèles à vérifier sur la page officielle de chaque fournisseur
MODELS = {
    "deepseek": {
        "key": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
    },
    "gemini": {
        "key": "GEMINI_API_KEY",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "model": "gemini-3.8-flash",
    },
    "groq": {
        "key": "GROQ_API_KEY",
        "base_url": "https://api.groq.com/openai/v1",
        "model": "openai/gpt-oss-120b",
    },
    "groq_allam": {
        "key": "GROQ_API_KEY",
        "base_url": "https://api.groq.com/openai/v1",
        "model": "allam-2-7b",
    },
}

with open("results/raw/test_api.txt", "w", encoding="utf-8") as out:
    for name, cfg in MODELS.items():
        api_key = os.getenv(cfg["key"])
        if not api_key:
            print(f"[{name}] pas de clé -> ignoré")
            continue
        try:
            client = OpenAI(api_key=api_key, base_url=cfg["base_url"])
            reply = client.chat.completions.create(
                model=cfg["model"],
                messages=[{"role": "user", "content": PROMPT}],
                temperature=0,
            )
            text = reply.choices[0].message.content
            print(f"[{name}] OK : {text}")
            out.write(f"=== {name} ({cfg['model']}) ===\n{text}\n\n")
        except Exception as e:
            print(f"[{name}] ERREUR : {e}")
            out.write(f"=== {name} ===\nERREUR : {e}\n\n")