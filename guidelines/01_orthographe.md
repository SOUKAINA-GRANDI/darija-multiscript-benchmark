# 01 — Guide d'orthographe (arabe et arabizi)

La darija n'a pas d'orthographe officielle. Ce guide fixe la **forme de référence**
du benchmark. D'autres écritures restent valables : pour la tâche de conversion,
elles sont acceptées via la colonne `gold_alt`.

## 1. Règles communes aux deux graphies (décision D11)

- **Ponctuation latine dans les deux graphies** : `?` `,` `.` `!`
  → la seule différence entre variantes est l'écriture des mots.
- **Chiffres écrits en lettres** : جوج / jouj, تلاتة / tlata.
  → en arabizi, 3, 7, 9 sont des lettres : des chiffres créeraient une confusion.
- Pas de voyelles courtes (harakat) en arabe.
- Mêmes mots, même ordre, même sens dans les deux variantes.

## 2. Écriture arabe

| Règle | Choix retenu | Exemple |
|---|---|---|
| Présent | ك / كي collé au verbe | كنخدم، كيقرا |
| Futur | غادي séparé | غادي نمشي |
| Négation | ما + verbe + ش | ما جاش، ما بغيتش |
| Article | ال collé | الفيلم، الدار |
| « à / vers » | ل collé | للدار، للسوق |
| « dans » | ف collé | فالدار |
| Ta marbuta | ة | خدمة، مدرسة |
| Hamza | seulement si prononcée | |

## 3. Écriture arabizi

| Arabe | Référence | Variantes acceptées (`gold_alt`) | Exemple |
|---|---|---|---|
| ع | 3 | — | 3jebni |
| ح | 7 | h | 7lib |
| ق | 9 | q | 9alb |
| خ | kh | 5 | khobz |
| غ | gh | — | ghadi |
| ش | **ch** | sh | chkoun |
| ء | 2 (rare) | — | t2ajjel |
| ص / ط / ض | s / t / d | — | sbitar |
| و (voyelle) | ou | u, o | chnou |
| ي (voyelle) | i | — | fin |

Règles :
- Minuscules, sauf noms propres (A7med, Sara).
- **Article collé** : lfilm, ddar, l7anout.
- Négation : `ma jach` (référence) ; `majach` accepté.
- Voyelles selon la prononciation ; variantes acceptées (3jebni / 3jbni).
- Consonnes doublées acceptées dans les deux formes (bzaf / bzzaf).

## 4. Mots fréquents à orthographe fixée

| Sens | Arabe | Arabizi |
|---|---|---|
| beaucoup | بزاف | bzaf |
| où | فين | fin |
| quoi | شنو | chnou |
| qui | شكون | chkoun |
| pourquoi | علاش | 3lach |
| quand | إمتى | imta |
| maintenant | دابا | daba |
| bien | مزيان | mzyan |
| je veux | بغيت | bghit |
| il est allé | مشا | mcha |
| maison | دار | dar |
| travail | خدمة | khedma |

## 5. Références multiples (tâche de conversion)

1. J'écris la référence selon ce guide (`gold`).
2. Si possible, une ou deux autres personnes écrivent la même phrase en arabizi
   **sans consigne**.
3. Leurs formes différentes et naturelles sont ajoutées dans `gold_alt`
   (séparées par `|`).