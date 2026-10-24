import pandas as pd

PATH = "data/final/benchmark.xlsx"
df_current = pd.read_excel(PATH, dtype=str).fillna("")

part3_rows = [
    # =========================================================================
    # 1. DERNIERS QCM (Q-021 à Q-024) -> Pour égaliser A, B, C, D à 6 chacun
    # Manquants : 1 A, 1 C, 2 D
    # =========================================================================
    # Q-021 (Gold: D)
    {"id": "Q-021", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "achats", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "سلوى مشات لسنتر فيل تشري كادو لعيد ميلاد ختها، لقات صاك جلد كحل واعر وشراتو.",
     "question": "شنو شرات سلوى كادو لختها؟", "choix_a": "خاتم د الذهب", "choix_b": "ساعة يد", "choix_c": "ريحة غالية", "choix_d": "صاك جلد كحل", "gold": "D"},
    {"id": "Q-021", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "achats", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Salwa mchat l centre-ville tchri cadeau l 3id milad kht-ha, l9at sac jeld k7el wa3er w chratou.",
     "question": "Chnou chrat Salwa cadeau l kht-ha?", "choix_a": "khatem d ddheb", "choix_b": "sa3a d lyed", "choix_c": "ri7a ghalya", "choix_d": "sac jeld k7el", "gold": "D"},

    # Q-022 (Gold: A)
    {"id": "Q-022", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "transport", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "الطاكسي كبير وقف فالرونبوان باش يركب الناس، وبقات بلاصة وحدة اللور خاوية.",
     "question": "فين بقات البلاصة الخاوية فالطاكسي؟", "choix_a": "بقات بلاصة وحدة اللور", "choix_b": "القدام حدا الشيفور", "choix_c": "فالملا فالسقف", "choix_d": "الطاكسي كان عامر كلو", "gold": "A"},
    {"id": "Q-022", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "transport", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Ttaxi kbir w9ef f rond-point bach yrkkeb nass, w b9at blassa we7da llour khawya.",
     "question": "Fin b9at lblassa lkhawya f ttaxi?", "choix_a": "b9at blassa we7da llour", "choix_b": "l9ddam 7da chifour", "choix_c": "f lmalla f sse9f", "choix_d": "ttaxi kan 3amer kollou", "gold": "A"},

    # Q-023 (Gold: C)
    {"id": "Q-023", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "météo", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "مشاو الدراري للبحر فالصيف، لقاوه عامر والموج عالي بزاف حيت كان الريح الشرقي.",
     "question": "علاش كان الموج عالي فالبحر؟", "choix_a": "حيت الما كان بارد", "choix_b": "حيت طاحت الشتا", "choix_c": "حيت كان الريح الشرقي", "choix_d": "حيت الليل قرب يطيح", "gold": "C"},
    {"id": "Q-023", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "météo", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Mchaw ddrari l lb7ar f ssif, l9awh 3amer w lmouj 3ali bzaf 7it kan rri7 cher9i.",
     "question": "3lach kan lmouj 3ali f lb7ar?", "choix_a": "7it lma kan bared", "choix_b": "7it ta7et chta", "choix_c": "7it kan rri7 cher9i", "choix_d": "7it llil 9reb yti7", "gold": "C"},

    # Q-024 (Gold: D)
    {"id": "Q-024", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "vie quotidienne", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "جواد نسى السوارت فوق الطابلة فالكوزينة، وملي خرج وسد الباب عاد تفكرهم وبقا واحل.",
     "question": "فين نسى جواد السوارت؟", "choix_a": "فالطوموبيل", "choix_b": "فالجيب د الجاكيتة", "choix_c": "فالخدمة", "choix_d": "فوق الطابلة فالكوزينة", "gold": "D"},
    {"id": "Q-024", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "vie quotidienne", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Jawad nsa sswaret fo9 ttabla f lkouzina, w mlli khrej w sedd lbab 3ad tfekkerhom w b9a wa7el.",
     "question": "Fin nsa Jawad sswaret?", "choix_a": "f tomobil", "choix_b": "f jjib d ljakita", "choix_c": "f lkhedma", "choix_d": "fo9 ttabla f lkouzina", "gold": "D"},

    # =========================================================================
    # 2. DERNIERS NLI (N-011 et N-012) -> 2 contextes x 3 labels = 12 lignes
    # Portant le total NLI à 10 imp / 10 cont / 10 neut
    # =========================================================================
    # N-011 (Imane - Cuisine)
    {"id": "N-011a", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "cuisine", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "إيمان كطيب طاجين ديال الحوت فالفران.", "texte_2": "إيمان كتوجد الماكلة.", "gold": "implication"},
    {"id": "N-011a", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "cuisine", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Imane katyeb tajin dyal l7out f lferran.", "texte_2": "Imane katwjed lmakla.", "gold": "implication"},
    {"id": "N-011b", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "cuisine", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "إيمان كطيب طاجين ديال الحوت فالفران.", "texte_2": "إيمان معمرها دخلات للكوزينة.", "gold": "contradiction"},
    {"id": "N-011b", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "cuisine", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Imane katyeb tajin dyal l7out f lferran.", "texte_2": "Imane m3mmrha dekhlat l lkouzina.", "gold": "contradiction"},
    {"id": "N-011c", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "cuisine", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "إيمان كطيب طاجين ديال الحوت فالفران.", "texte_2": "الحوت لي دارت هو الصول.", "gold": "neutre"},
    {"id": "N-011c", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "cuisine", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Imane katyeb tajin dyal l7out f lferran.", "texte_2": "L7out li daret houwa sole.", "gold": "neutre"},

    # N-012 (Bilal - Études)
    {"id": "N-012a", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "éducation", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "بلال جاب النقطة اللولة فالمات فالقسم كامل.", "texte_2": "بلال كيقرا مزيان الماط.", "gold": "implication"},
    {"id": "N-012a", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "éducation", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Bilal jab nno9ta loullya f lmath f l9ism kamel.", "texte_2": "Bilal kay9ra mzyan lmath.", "gold": "implication"},
    {"id": "N-012b", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "éducation", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "بلال جاب النقطة اللولة فالمات فالقسم كامل.", "texte_2": "بلال هو اللخر فالماط فالقسم.", "gold": "contradiction"},
    {"id": "N-012b", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "éducation", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Bilal jab nno9ta loullya f lmath f l9ism kamel.", "texte_2": "Bilal houwa llekher f lmath f l9ism.", "gold": "contradiction"},
    {"id": "N-012c", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "éducation", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "بلال جاب النقطة اللولة فالمات فالقسم كامل.", "texte_2": "بلال باغي يدير مهندس د لانفورماتيك.", "gold": "neutre"},
    {"id": "N-012c", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "éducation", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Bilal jab nno9ta loullya f lmath f l9ism kamel.", "texte_2": "Bilal baghi ydir ingénieur d l'informatique.", "gold": "neutre"},

    # =========================================================================
    # 3. DERNIÈRES CONVERSIONS (C-019 à C-024) -> 6 phrases x 2 = 12 lignes
    # =========================================================================
    {"id": "C-019", "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "santé", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "ما بقاش فيا الحال، المهم هي الصحة والسلامة.", "gold": "Ma b9ach fiya l7al, lmouhim hiya sse77a w ssalama.", "gold_alt": "mab9ach fia lhal, lmohim hya seha w salama.|ma b9ach fiya lhal."},
    {"id": "C-019", "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "santé", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Ma b9ach fiya l7al, lmouhim hiya sse77a w ssalama.", "gold": "ما بقاش فيا الحال، المهم هي الصحة والسلامة."},

    {"id": "C-020", "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "transport", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "واش هاد الطوبيس كيدوز على جامع الفنا؟", "gold": "Wach had ttobis kaydouz 3la Jame3 lfna?", "gold_alt": "wach had tobis kidouz 3la jama3 lfna?|wach had ttobis kaydoz 3la jame3 lfna?"},
    {"id": "C-020", "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "transport", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Wach had ttobis kaydouz 3la Jame3 lfna?", "gold": "واش هاد الطوبيس كيدوز على جامع الفنا؟"},

    {"id": "C-021", "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "travail", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "الخدمة كاينة ولكن خاص بنادم يصبر ويزير راسو.", "gold": "Lkhedma kayna walakin khas bnadem yssber w yzeyyer rassou.", "gold_alt": "lkhdma kayna walakin khass bnadem ysber.|lkhedma kayna walakin khas bnadm ysber."},
    {"id": "C-021", "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "travail", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Lkhedma kayna walakin khas bnadem yssber w yzeyyer rassou.", "gold": "الخدمة كاينة ولكن خاص بنادم يصبر ويزير راسو."},

    {"id": "C-022", "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "achats", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "نقص ليا شوية فالثمن راني كليان قديم عندك.", "gold": "N9es lia chwiya f ttaman rani klyan 9dim 3ndek.", "gold_alt": "n9es liya chwia f taman rani cliyan qdim 3ndk.|n9es lia chwiya f taman."},
    {"id": "C-022", "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "achats", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "N9es lia chwiya f ttaman rani klyan 9dim 3ndek.", "gold": "نقص ليا شوية فالثمن راني كليان قديم عندك."},

    {"id": "C-023", "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "maison", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "سد الشرجم راه كيدخل البرد بزاف لبيت النعاس.", "gold": "Sedd ccherjem rah kaydkhol lberd bzaf l bit nna3s.", "gold_alt": "sedd cherjam rah kaydkhol lberd bzaf.|sed cherjem rah kidkhol lberd."},
    {"id": "C-023", "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "maison", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Sedd ccherjem rah kaydkhol lberd bzaf l bit nna3s.", "gold": "سد الشرجم راه كيدخل البرد بزاف لبيت النعاس."},

    {"id": "C-024", "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "technologie", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "الويفي تقيل بزاف اليوم، واقيلا خاصنا نروديماريو الروتور.", "gold": "Lwifi t9il bzaf lyoma, wa9ila khasna nredemariw lrouteur.", "gold_alt": "lwifi tqil bzaf lyom, waqila khassna nredemariw routeur.|l wifi t9il bzaf lyoma."},
    {"id": "C-024", "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "technologie", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Lwifi t9il bzaf lyoma, wa9ila khasna nredemariw lrouteur.", "gold": "الويفي تقيل بزاف اليوم، واقيلا خاصنا نروديماريو الروتور."}
]

df_append = pd.DataFrame(part3_rows).reindex(columns=df_current.columns)
df_total = pd.concat([df_current, df_append], ignore_index=True)
df_total.to_excel(PATH, index=False)
print(f"🎉 FÉLICITATIONS ! Le benchmark complet atteint maintenant {len(df_total)} lignes.")
