# Benchmark Multigraphique pour l'Évaluation des LLM en Darija Marocaine

Projet de Fin d'Année (PFA) - Master Data Science & Big Data (DSBD)  
**Faculté des Sciences Ben M'Sick - Université Hassan II de Casablanca**  
**Réalisé par :** Soukaina Grandi  
**Encadré par :** M. Zahour Omar  

---

## 📌 Présentation du Projet
La darija marocaine, langue peu dotée, se caractérise par l'absence d'orthographe standardisée et une dualité d'écriture quotidienne :
- **L'alphabet arabe** (ex: *كداير*)
- **L'arabizi** combinant alphabet latin et chiffres phonétiques (ex: *kidayr*, *ki dayr*, *3jebni*).

Ce projet propose un **benchmark multigraphique étalonné** évaluant si le choix de la graphie influence la compréhension et le raisonnement des grands modèles de langage (LLM).

---

## 🏗️ Structure du Corpus (`data/final/benchmark.xlsx`)
Le benchmark comprend **156 items** (78 contenus uniques systématiquement déclinés en arabe `ar` et arabizi `lat`) :
- **Conversion de graphie (48 lignes) :** Arabe $\leftrightarrow$ Arabizi.
- **Compréhension de texte / QCM (48 lignes) :** Choix multiple A, B, C, D équilibré.
- **Inférence textuelle / NLI (60 lignes) :** Implication, Contradiction, Neutre.
- **Cloisonnement strict :** Split `dev` (64 lignes) pour le calibrage des invites et Split `test` (92 lignes) pour l'évaluation finale à l'aveugle.

---

## ⚙️ Environnement Technique
- **Python :** 3.12
- **Installation des dépendances :**
  ```bash
  pip install -r requirements.txt
