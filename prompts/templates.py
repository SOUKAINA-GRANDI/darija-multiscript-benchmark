# prompts/templates.py

PROMPT_QCM = """Tu es un système d'évaluation en darija marocaine.
Lis le texte suivant et réponds à la question en choisissant une seule option parmi A, B, C ou D.
Réponds UNIQUEMENT par la lettre de la bonne réponse (A, B, C ou D), sans aucune explication.

Texte : {texte}
Question : {question}
A) {choix_a}
B) {choix_b}
C) {choix_c}
D) {choix_d}

Réponse :"""

PROMPT_NLI = """Tu es un système de raisonnement textuel en darija marocaine.
Étant donné une prémisse et une hypothèse, détermine leur relation logique.
Choisis STRICTEMENT parmi ces 3 options :
- implication (si l'hypothèse est obligatoirement vraie sachant la prémisse)
- contradiction (si l'hypothèse est fausse sachant la prémisse)
- neutre (si on ne peut pas savoir)

Réponds UNIQUEMENT par l'un de ces trois mots : implication, contradiction ou neutre. Ne rajoute rien d'autre.

Prémisse : {texte}
Hypothèse : {texte_2}

Relation :"""

PROMPT_CONV_TO_AR = """Convertis fidèlement cette phrase écrite en darija arabizi (caractères latins et chiffres) vers l'écriture en caractères arabes.
Réponds UNIQUEMENT par la phrase convertie, sans commentaire ni ponctuation superflue.

Phrase en arabizi : {texte}
Phrase en arabe :"""

PROMPT_CONV_TO_LAT = """Convertis fidèlement cette phrase écrite en darija (caractères arabes) vers l'écriture arabizi (caractères latins et chiffres standard : 3 pour ع, 7 pour ح, 9 pour ق).
Réponds UNIQUEMENT par la phrase convertie en arabizi, sans commentaire.

Phrase en arabe : {texte}
Phrase en arabizi :"""