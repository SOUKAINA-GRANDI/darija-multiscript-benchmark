# Protocole d'Évaluation Officiel du Benchmark Multigraphique Darija

Ce document décrit les spécifications exactes de l'environnement d'évaluation afin d'assurer une reproductibilité à 100 %.

---

## 1. Paramètres d'Inférence Déterministe
Tous les modèles sont interrogés selon les hyperparamètres stricts suivants :
* **Mode :** Zero-shot (aucune démonstration préalable fournie dans l'invite).
* **Température :** `0.0` (mode déterministe strict).
* **Max Output Tokens :** `1024` (évite toute coupure des modèles de raisonnement comme GPT-OSS).
* **Top-p :** `1.0`.

---

## 2. Définition des Rôles et des Graphies
* La colonne `graphie` dans `benchmark.xlsx` désigne systématiquement la **graphie de l'entrée** :
  * `ar` : Entrée en caractères arabes $\rightarrow$ Sortie attendue en Arabizi pour la conversion.
  * `lat` : Entrée en Arabizi $\rightarrow$ Sortie attendue en caractères arabes pour la conversion.
* Pour QCM et NLI, le label de référence (`gold`) est rigoureusement identique quelle que soit la graphie.

---

## 3. Justification du Choix des Modèles
Conformément aux ajustements documentés dans `decisions.md` (D12) :
1. **Qwen 3.8 (27B)** : Représentant de pointe des LLMs multilingues ouverts (Open-Weights).
2. **GPT-OSS (120B)** : Modèle massif (120 milliards de paramètres) servant de plafond de compétence occidentale.
3. **ALLaM-2 (7B)** : Modèle régional arabophone souverain (SDAIA).

---

## 4. Politique Linguistique Documentée
* **Code-Switching (`cs=0`) :** Le corpus principal est conservé sans mélange de langues (français/espagnol) afin d'**isoler l'impact pur de la graphie** de la Darija.
* **Variante mixte (`mix`) :** Non incluse dans cette version initiale pour préserver la symétrie binaire Arabe vs Arabizi.