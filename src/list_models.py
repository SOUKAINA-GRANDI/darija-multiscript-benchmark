import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDERS = {
    "gemini": ("GEMINI_API_KEY", "https://generativelanguage.googleapis.com/v1beta/openai/"),
    "groq": ("GROQ_API_KEY", "https://api.groq.com/openai/v1"),
}

for name, (key, url) in PROVIDERS.items():
    api_key = os.getenv(key)
    if not api_key:
        continue
    print(f"\n=== {name} ===")
    try:
        client = OpenAI(api_key=api_key, base_url=url)
        for m in client.models.list():
            print(m.id)
    except Exception as e:
        print("ERREUR :", e)