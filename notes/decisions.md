# Décisions pour le benchmark

## Manque identifié
Les ressources lues évaluent la darija surtout en écriture arabe (Atlas-Chat,
DarijaMMLU). TerjamaBench contient arabe + arabizi, mais uniquement pour la
traduction. Aucune ressource lue ne compare la compréhension (QCM, NLI) d'un
même contenu écrit en arabe et en arabizi.

## Décisions

| # | Décision | Justification |
|---|---|---|
| D1 | Notation par génération + extraction de la réponse (lettre ou étiquette), pour tous les modèles | La log-vraisemblance (lm-evaluation-harness) est impossible via API ; même méthode = comparaison équitable |
| D2 | QCM à 4 choix, réponse stockée en lettre (A-D), positions équilibrées | Format proche de DarijaMMLU, plus lisible qu'un index |
| D3 | Données rédigées à la main par une locutrice native, pas de traduction automatique | Éviter le biais de traduction et l'influence de l'arabe standard (limite de DarijaMMLU) |
| D4 | Chaque item existe en arabe et en arabizi, avec un ID commun et la même réponse | Comble le manque identifié ; principe multigraphique |
| D5 | Conversion : correspondance exacte (plusieurs références) + CER après normalisation ; pas de BLEU | TerjamaBench montre que BLEU corrèle mal avec le jugement humain quand l'orthographe est libre |
| D6 | Zero-shot, température 0, prompt identique pour toutes les graphies, consigne en français | Isoler l'effet de la graphie |
| D7 | Prompts réglés uniquement sur le dev, puis figés avant le test | Éviter de sur-ajuster sur le test |
| D8 | Documenter modèle, version, date, prompt et réponse brute | Reproductibilité ; les modèles changent souvent |
| D9 | Comparer à la base aléatoire (25 % QCM, 33 % NLI) et mesurer la cohérence entre variantes | Interpréter les scores correctement |
| D10 | Test « sans texte » sur le pilote QCM | Vérifier que les questions ne sont pas devinables |
| D11 | Ponctuation latine commune aux deux graphies ; chiffres écrits en lettres | Seule différence = l'écriture des mots ; en arabizi 3, 7, 9 sont des lettres |