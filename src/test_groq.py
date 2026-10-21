import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

print("=== TEST DE L'API GROQ (GRATUIT) ===")

# Configuration pour Groq (compatible OpenAI)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

try:
    # On utilise le modèle Llama 3.1 8B (très rapide et gratuit sur Groq)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages=[
            {"role": "system", "content": "Tu es un expert en darija marocaine."},
            {"role": "user", "content": "Convertis cette phrase en arabizi (latin avec chiffres) : عجبني هاد الفيلم بزاف"}
        ],
        temperature=0
    )
    
    reponse = response.choices[0].message.content
    print(f"\n✅ SUCCÈS GROQ ! Le modèle a répondu :")
    print(f"-> {reponse}\n")

    # Sauvegarder
    os.makedirs("results/raw", exist_ok=True)
    with open("results/raw/test_groq.txt", "w", encoding="utf-8") as f:
        f.write(reponse)
    print("💾 Réponse sauvegardée dans results/raw/test_groq.txt")

except Exception as e:
    print(f"\n ERREUR GROQ : {e}")