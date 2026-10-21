# Bilan Méthodologique et Résultats du Benchmark

## 1. Pipeline et Exécution
- Pipeline entièrement automatisé et reproductible (`run_eval.py`, `score.py`).
- Taux de réponses invalides : 0% sur l'ensemble des tâches et graphies.

## 2. Analyse par Tâche (Split Test)

### Conversion de Graphie
- **Métrique `script_ok` :** 
  - Qwen 3.8-27B respecte l'alphabet cible (100% en ar->lat, 92.9% en lat->ar).
  - ALLaM-2-7B échoue en ar->lat (0.0% de respect du script cible), recopiant quasi-systématiquement l'arabe avec vocalisation.
- **Limites du CER et de l'Exact Match :**
  - L'Exact Match à 0% s'explique à la fois par la multiplicité orthographique naturelle de la Darija et par des erreurs de conversion.
  - Le CER seul est insuffisant : un CER bas peut masquer un glissement sémantique critique (ex: `7da` [à côté] converti en `hada` [ce/cette] par Qwen).
  - Une analyse qualitative humaine à l'aveugle est nécessaire pour discriminer variantes légitimes et erreurs réelles.

### Inférence Textuelle (NLI)
- Tendance observée : dégradation des performances en arabizi (Qwen: 88.9% -> 77.8% ; ALLaM: 66.7% -> 38.9%).
- **Significativité statistique :** Le test exact de McNemar (ALLaM: $p = 0.125$, Qwen: $p = 0.625$) indique que sur cet échantillon de test ($N=18$), l'écart n'est pas statistiquement significatif au seuil standard $\alpha = 0.05$. Il s'agit d'une tendance empirique exploratoire nécessitant confirmation sur un échantillon élargi.

### Compréhension Écrite (QCM)
- Plafond de performance atteint pour Qwen (100%).
- **Contrôle sans texte (blind test sur dev) :** Le modèle obtient 45.0% sans le texte d'appui (hasard = 25%, test binomial $p \approx 0.04$). Cela indique que certaines options contiennent des indices de surface (notamment longueur/détail des choix) permettant une déduction partielle sans compréhension du contexte.

## 3. Statut Méthodologique du Split Test
- Le split test ayant été évalué et consulté lors de ces diagnostics préliminaires sans modification des références `gold`, ces scores constituent une première évaluation exploratoire documentée.
- Pour garantir une évaluation finale rigoureusement aveugle, un ensemble `test2` de QCM rééquilibrés et d'échantillons élargis est préconisé pour les travaux futurs.