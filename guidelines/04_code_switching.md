# 04 — Politique code-switching

Deux facteurs distincts :
- **Graphie** : arabe vs latin (`3jebni had lfilm bzaf` = darija en arabizi)
- **Mélange de langues** : darija + français/anglais (`عجبني ce film بزاف`)

## Quatre conditions possibles

| Condition | Description | Corpus |
|---|---|---|
| ar | darija, écriture arabe | **principal** |
| lat | darija, arabizi | **principal** |
| mix | darija, quelques mots dans l'autre graphie | optionnel |
| cs | darija + mots français/anglais | optionnel |

## Règles du corpus principal (ar, lat)
1. Pas de phrase ou expression entière en français/anglais.
2. **Emprunts intégrés acceptés**, écrits dans la graphie de la variante :
   طوموبيل / tomobil, تيليفون / tilifoun, طوبيس / tobis, سبيطار / sbitar, ماتش / match.
3. Un emprunt présent dans une variante est présent dans l'autre.

## Variantes optionnelles (mix, cs)
- Copie séparée du contenu, 1 à 3 mots modifiés (max ~30 %).
- Même sens, même réponse attendue.

## Marquage dans le dataset
- `graphie` : ar | lat | mix
- `cs` : 0 (pas de mot français/anglais) | 1 (présence)