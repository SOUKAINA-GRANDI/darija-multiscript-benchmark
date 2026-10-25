import re
import sys
import pandas as pd

PATH = sys.argv[1] if len(sys.argv) > 1 else "data/pilot/pilot.xlsx"

# Regex
ARABIC = re.compile(r"[\u0600-\u06FF]")
DIGIT = re.compile(r"[0-9\u0660-\u0669]")
NLI_LABELS = {"implication", "contradiction", "neutre"}

# 1. Chargement et nettoyage automatique des espaces résiduels
df = pd.read_excel(PATH, dtype=str).fillna("")
for col in df.columns:
    df[col] = df[col].astype(str).str.strip()

# Conversion de la colonne cs en entier pour les vérifications
if "cs" in df.columns:
    df["cs"] = pd.to_numeric(df["cs"], errors="coerce").fillna(0).astype(int)
else:
    df["cs"] = 0

errors, warnings = [], []

def txt(r):
    return " ".join(r[c] for c in ["texte", "texte_2", "question",
                                    "choix_a", "choix_b", "choix_c", "choix_d"])

# 2. Vérification des doublons
dup = df[df.duplicated(["id", "graphie"], keep=False)]
for _, r in dup.iterrows():
    errors.append(f"{r['id']} [{r['graphie']}] : doublon exact trouvé")

# 3. Parcours ligne par ligne
for _, r in df.iterrows():
    tag = f"{r['id']} [{r['graphie']}]"
    
    # Validité des métadonnées de base
    if r["tache"] not in {"qcm", "nli", "conversion"}:
        errors.append(f"{tag} : tache inconnue '{r['tache']}'")
    if r["graphie"] not in {"ar", "lat", "mix"}:
        errors.append(f"{tag} : graphie inconnue '{r['graphie']}'")
    if r["split"] not in {"dev", "test"}:
        errors.append(f"{tag} : split invalide '{r['split']}'")
    if not r["texte"]:
        errors.append(f"{tag} : texte d'entrée vide")

    t = txt(r)

    # Cohérence des alphabets / graphies
    if r["graphie"] == "lat" and ARABIC.search(t):
        errors.append(f"{tag} : présence de caractères arabes dans une ligne arabizi (lat)")
    
    if r["graphie"] == "ar":
        if not ARABIC.search(r["texte"]):
            errors.append(f"{tag} : aucun caractère arabe trouvé dans une ligne arabe (ar)")
        
        # Alerte chiffre (sauf si code-switching justifié)
        if DIGIT.search(t) and r["cs"] == 0:
            warnings.append(f"{tag} : chiffre détecté dans une ligne arabe (règle : privilégier les lettres, sauf si cs=1)")

    # Règles spécifiques par tâche
    if r["tache"] == "qcm":
        if any(not r[c] for c in ["question", "choix_a", "choix_b", "choix_c", "choix_d"]):
            errors.append(f"{tag} : question ou au moins un choix de réponse manquant")
        if r["gold"] not in {"A", "B", "C", "D"}:
            errors.append(f"{tag} : gold QCM doit être strictement 'A', 'B', 'C' ou 'D' (reçu : '{r['gold']}')")

    if r["tache"] == "nli":
        if not r["texte_2"]:
            errors.append(f"{tag} : hypothèse (texte_2) vide")
        if r["gold"] not in NLI_LABELS:
            errors.append(f"{tag} : étiquette NLI invalide '{r['gold']}' (attendu : implication, contradiction ou neutre)")

    if r["tache"] == "conversion":
        if r["graphie"] == "ar" and ARABIC.search(r["gold"] + r["gold_alt"]):
            errors.append(f"{tag} : la cible attendue en arabizi contient des caractères arabes")
        if r["graphie"] == "lat" and not ARABIC.search(r["gold"]):
            errors.append(f"{tag} : la cible attendue en arabe ne contient pas de caractères arabes")

# 4. Cohérence cross-graphies par ID
for id_, g in df.groupby("id"):
    graphies = set(g["graphie"])
    if not {"ar", "lat"} <= graphies:
        missing = {"ar", "lat"} - graphies
        errors.append(f"{id_} : variante manquante -> {list(missing)}")
    if g["split"].nunique() > 1:
        errors.append(f"{id_} : variantes réparties dans des splits différents (risque de fuite)")
    if g["tache"].iloc[0] in {"qcm", "nli"} and g["gold"].nunique() > 1:
        errors.append(f"{id_} : le gold standard diffère entre la version ar et lat")

# 5. Affichage du bilan
print("=" * 60)
print(f"RAPPORT DE VALIDATION : {PATH}")
print(f"Total : {len(df)} lignes | {df['id'].nunique()} identifiants uniques")
print("=" * 60)

print("\nRépartition Tâche x Graphie :")
print(df.groupby(["tache", "graphie"]).size().unstack(fill_value=0))

q = df[(df.tache == "qcm") & (df.graphie == "ar")]
if len(q):
    print("\nÉquilibre des réponses QCM (A/B/C/D) :")
    print(q["gold"].value_counts().to_dict())

n = df[(df.tache == "nli") & (df.graphie == "ar")]
if len(n):
    print("\nÉquilibre des classes NLI :")
    print(n["gold"].value_counts().to_dict())

print("\n" + "-" * 60)
print(f"Résultat : {len(errors)} erreur(s), {len(warnings)} avertissement(s)")

for e in errors:
    print(f"  ❌ ERREUR : {e}")
for w in warnings:
    print(f"  ⚠️  ATTENTION : {w}")

if not errors:
    print("\n✅ Super ! Le jeu de données pilote est 100% valide et prêt pour l'évaluation.")
print("=" * 60)