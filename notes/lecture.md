# Notes de lecture (lecture ciblée)

**But :** copier les bonnes pratiques pour construire le benchmark multigraphique
(conversion, QCM, NLI ; arabe et arabizi). Ce n'est pas un état de l'art rédigé.

**Convention :**
- « Limites reconnues » = ce que les auteurs écrivent eux-mêmes.
- « Manque identifié » = mon analyse, par rapport à mon projet.
- « non précisé » = information non trouvée dans la source.

---

## Fiche 1 : Atlas-Chat (2024)

- **Lien :** https://arxiv.org/abs/2409.17912
- **Modèles :** Atlas-Chat 2B, 9B, 27B (Hugging Face : MBZUAI-Paris)
- **Type :** modèle + suite d'évaluation darija

- **Ce qu'ils évaluent :**
  - Tâches discriminatives : DarijaMMLU, DarijaHellaSwag, Belebele (version darija)
  - Tâches génératives : DarijaAlpacaEval (suivi d'instructions), DarijaBench
    (traduction, résumé, sentiment)
  - Langue : darija marocaine

- **Graphies des données :**
  - Benchmarks d'évaluation : **écriture arabe**
  - L'article mentionne l'arabizi (exemple « kidayr ? » / « كي داير؟ »)
  - Données d'entraînement : contiennent une partie translittération arabe ↔ latin
    (DODa, environ 17k paires — chiffre à vérifier)
  - L'arabizi n'est **pas évalué séparément** en compréhension

- **Format d'un exemple :** QCM (question + choix + bonne réponse), paires
  instruction / réponse, paires de traduction.

- **Extraction / notation :**
  - Zero-shot via **lm-evaluation-harness**
  - QCM : accuracy (normalisée), calculée par **log-vraisemblance** des choix
  - Tâches génératives : win-rate simulé (LLM juge)

- **Métriques :** accuracy (DarijaMMLU, DarijaHellaSwag, Belebele),
  BLEU / chrF (traduction, résumé), win-rate (génération).

- **Qualité :** traduction automatique (Claude 3.5 Sonnet) + filtrage culturel ;
  mélange de données synthétiques, manuelles et de ressources existantes.

- **Limites reconnues (par les auteurs) :** non précisé dans ma lecture
  (à compléter si je trouve la section « Limitations »).

- **Manque identifié (mon analyse) :**
  - Pas de comparaison arabe vs arabizi sur le **même contenu**
  - Pas de tâche NLI en darija
  - Méthode de notation (log-vraisemblance) non applicable aux modèles via API

- **Conséquence pour mon projet :**
  lm-evaluation-harness note les QCM par probabilité de chaque choix.
  C'est impossible avec des API (Groq, Gemini, DeepSeek).
  J'utiliserai **génération + extraction de la lettre / de l'étiquette**,
  pour **tous** les modèles, y compris Atlas-Chat, afin que la comparaison soit équitable.

- **À copier dans mon projet :**
  - Suite multi-tâches (plusieurs tâches complémentaires)
  - QCM noté par accuracy, en zero-shot
  - Comparer un modèle spécialisé darija à des modèles généralistes

- **À éviter :**
  - S'appuyer uniquement sur des données traduites automatiquement
  - Évaluer une seule graphie alors que l'arabizi est très utilisé

---

## Fiche 2 : DarijaMMLU

- **Lien :** https://huggingface.co/datasets/MBZUAI-Paris/DarijaMMLU
- **Licence :** MIT (à vérifier sur la page)
- **Type :** benchmark QCM

- **Ce qu'ils évaluent :** connaissances et raisonnement de type examen,
  environ 44 sujets, en darija.

- **Graphies des données :** **écriture arabe uniquement**.
  Contenu traduit depuis MMLU (anglais) et ArabicMMLU (arabe standard)
  avec Claude 3.5 Sonnet.

- **Format d'une ligne (Dataset viewer) :**
  - `question`
  - `context` (souvent vide)
  - `choices` (liste de 2 à 5 choix)
  - `answer` (index commençant à 0)
  - `subject`, `subject_darija`
  - `source` (mmlu / arabic_mmlu)

- **Notation :** accuracy (choix correct).

- **Métriques :** accuracy.

- **Limites reconnues (par les auteurs) :** certains sujets jugés peu pertinents
  pour le contexte marocain ont été exclus.

- **Manque identifié (mon analyse) :**
  - Traduction automatique → risque de biais de traduction et d'influence
    de l'arabe standard
  - Une seule graphie → **ne mesure pas l'effet de l'écriture**
  - Teste surtout des connaissances, pas la compréhension d'un texte darija

- **À copier :**
  - Format QCM clair : question + choix + bonne réponse
  - Colonne `source` pour tracer l'origine des données
  - Licence ouverte pour une éventuelle publication

- **À éviter :**
  - Traduire massivement sans relecture native
  - Stocker la réponse en index (je stockerai une lettre A-D, plus lisible)
  - Des questions de culture générale (mes réponses doivent être dans le texte)

---

## Fiche 3 : TerjamaBench

- **Lien :** https://huggingface.co/datasets/atlasia/TerjamaBench
- **Blog :** https://huggingface.co/blog/imomayiz/terjama-bench
- **Type :** benchmark de traduction

- **Ce qu'ils évaluent :** traduction anglais ↔ darija (surtout anglais → darija).

- **Graphies des données :** **les deux**.
  Colonnes `English`, `Darija` (écriture arabe) et `Arabizi` (écriture latine).
  C'est la ressource la plus proche de mon projet sur le plan multigraphique.

- **Stockage de l'arabizi :** colonne séparée ; orthographe non normalisée
  (variantes naturelles).

- **Variantes d'écriture / références multiples :** plusieurs formes arabizi
  possibles pour un même sens ; doublons possibles signalés.

- **Métriques :** BLEU, chrF, TER, LLM juge, évaluation humaine (échelle à 4 points).

- **Limites reconnues (par les auteurs) :**
  - Taille modeste (environ 850 exemples, environ 788 après dédoublonnage — à vérifier)
  - Biais régional possible
  - Avec une orthographe libre, les métriques automatiques (surtout BLEU)
    correspondent mal au jugement humain

- **Manque identifié (mon analyse) :**
  - Uniquement la traduction : pas de QCM ni de NLI
  - Ne compare pas la **compréhension** d'un même contenu selon la graphie

- **À copier :**
  - Arabe et arabizi présents **pour le même contenu**
  - Annotation par des locuteurs natifs + relecture
  - Accepter plusieurs écritures arabizi valides (→ colonne `gold_alt`)
  - Méfiance envers BLEU → correspondance exacte + CER pour la conversion

- **À éviter :**
  - Utiliser BLEU seul pour une langue sans orthographe standard
  - Ignorer les variantes orthographiques de l'arabizi

---

## Synthèse

| Ressource | Graphies couvertes | Tâches | Point fort pour mon projet | Manque principal |
|---|---|---|---|---|
| Atlas-Chat | Surtout arabe (translittération dans l'entraînement) | Multi-tâches (QCM, génération, traduction) | Suite d'évaluation + modèle spécialisé darija | Pas de comparaison arabe / arabizi ; notation non utilisable via API |
| DarijaMMLU | Arabe uniquement | QCM de connaissances | Format QCM propre | Une seule graphie ; données traduites |
| TerjamaBench | **Arabe + arabizi** | Traduction | Multigraphique + annotation native | Traduction seulement ; petite taille |

## Conclusion de la lecture

Les ressources lues évaluent la darija surtout en écriture arabe. La seule ressource
qui contient arabe et arabizi (TerjamaBench) se limite à la traduction.
Dans ces trois ressources, aucune ne compare la **compréhension** (QCM, NLI)
d'un **même contenu** écrit en arabe et en arabizi, ni la capacité de conversion
entre les deux graphies sous forme de tâche notée.

Mon benchmark comble ce manque : conversion de graphie + QCM + NLI,
chaque contenu présenté en arabe et en arabizi avec un identifiant commun.

*Remarque : cette conclusion porte sur les trois ressources lues ;
elle reste une hypothèse à confirmer si d'autres travaux sont trouvés.*