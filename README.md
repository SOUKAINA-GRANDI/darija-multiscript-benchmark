---

### Étape 3 : Documenter les écarts dans `notes/decisions.md`

Complétez votre fichier **`notes/decisions.md`** pour formaliser les réponses aux remarques de l'audit :

```markdown
# Registre des Décisions Méthodologiques (D1 à D15)

## D12 : Écart sur le panel des modèles
- **Cahier des charges initial :** Mentionnait ChatGPT, Gemini, DeepSeek et Atlas-Chat.
- **Réajustement expérimental :** 
  - Gemini a rencontré une indisponibilité d'accès API (erreur 403 / restriction de projet).
  - Atlas-Chat-9B/2B est sous accès restreint (gated repository 401 sur Hugging Face).
  - En substitution, nous avons évalué **GPT-OSS-120B** (très grand modèle de pointe), **Qwen 3.8-27B** (modèle multilingue de référence) et **ALLaM-2-7B** (modèle arabe régionalisé), assurant une comparaison représentative à 3 échelles de paramètres (7B, 27B, 120B).

## D13 : Normalisation de la ponctuation et de la graphie
- Remplacement systématique de la ponctuation arabe (، ؟ ؛) par la ponctuation standard (, ? ;) dans le benchmark conformément à la directive D11.
- Conservation des majuscules initiales en arabizi reconnues comme naturelles dans l'usage quotidien.

## D14 : Métrique de Conversion et limites du CER
- L'Exact Match à 0% en conversion découle de la multiplicité orthographique naturelle de la darija.
- Le CER est complété par la métrique `script_ok` (respect de l'alphabet cible) et par `cer_sans_espace` pour neutraliser les variations d'espacement des prépositions (ex: *lfilm* vs *l film*).

## D15 : Analyse critique des biais de surface
- **QCM :** Détection d'un biais de longueur (la bonne réponse est la plus longue dans 42% des cas). Le modèle obtient 45% sans texte d'appui, confirmant que le split actuel sert d'évaluation préliminaire documentée.
- **NLI :** Le test exact de McNemar montre que la baisse en arabizi chez ALLaM (-27.8 pts) est une tendance exploratoire nécessitant un échantillon élargi pour atteindre la significativité formelle au seuil $\alpha=0.05$.
