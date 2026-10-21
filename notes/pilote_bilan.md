# Bilan du Pilote - Évaluation Qwen 3.8-27b

## 1. Taux de validité des formats
- Taux d'invalide : 0% (les consignes strictes sont parfaitement respectées).

## 2. Compréhension (QCM & NLI)
- 100% de réussite en Arabe et en Arabizi.
- Cohérence parfaite entre les deux graphies sur ce petit échantillon.

## 3. Analyse de la conversion (Graphie)
- L'Exact Match est très strict pour la Darija à cause de la variabilité orthographique (ex: `resto` vs `ristaw`).
- Le CER (Character Error Rate) moyen est très bon (< 0.15), montrant que le modèle phonétise bien la langue.
- Ambiguïtés observées :
  - Mauvaise interprétation de certains chiffres arabizi (`7` interprété comme `t` au lieu de `ح` dans C-005).
  - Variations de transcription des voyelles courtes (`3jebni` vs `3jbni`).