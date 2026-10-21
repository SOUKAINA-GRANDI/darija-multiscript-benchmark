# 03 — Règles de la tâche NLI (inférence textuelle)

## Format
- Une **prémisse** et une **hypothèse**, dans la même graphie.
- Étiquette : `implication`, `contradiction` ou `neutre`.

## Définitions
- **Implication** : si la prémisse est vraie, l'hypothèse est forcément vraie.
- **Contradiction** : si la prémisse est vraie, l'hypothèse est forcément fausse.
- **Neutre** : la prémisse ne permet ni de confirmer ni de rejeter l'hypothèse.

## Construction
Pour chaque prémisse, écrire **les trois hypothèses** → étiquettes équilibrées.
Les trois paires ont des ID distincts mais la même prémisse (ex. N-001a, N-001b, N-001c).

## Pièges à éviter
1. Juger uniquement à partir de la prémisse (pas de connaissance extérieure).
2. Ne pas réserver la négation aux contradictions : varier
   (contradiction sans négation, neutre ou implication avec négation).
3. Ne pas rendre l'implication systématiquement plus courte.
4. Une seule information par hypothèse.
5. Si deux personnes peuvent hésiter → supprimer la paire.

## Exemple 1 (N-001)
Prémisse : سارة خدامة فالسبيطار فرملية. / Sara khddama f sbitar fermlia.

| Étiquette | Arabe | Arabizi |
|---|---|---|
| implication | سارة كتخدم. | Sara katkhdem. |
| contradiction | سارة ما عندها حتى خدمة. | Sara ma 3ndha 7tta khedma. |
| neutre | سارة كتخلص مزيان. | Sara katkhelles mzyan. |

## Exemple 2 (N-002)
Prémisse : الماتش تأجل حيت الشتا كانت كتصب بزاف. / Lmatch t2ajjel 7it chta kant katsob bzaf.

| Étiquette | Arabe | Arabizi |
|---|---|---|
| implication | الماتش ما تلعبش فوقتو. | Lmatch ma tl3bch f w9tou. |
| contradiction | الماتش تلعب فوقتو. | Lmatch tl3eb f w9tou. |
| neutre | الجمهور كان كثير فالملعب. | Ljoumhour kan ktir f lmal3ab. |