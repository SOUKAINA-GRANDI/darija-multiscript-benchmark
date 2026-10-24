import os
import pandas as pd

PATH = "data/final/benchmark.xlsx"
df_current = pd.read_excel(PATH, dtype=str).fillna("")

test_rows = [
    # =========================================================================
    # 1. NOUVEAUX QCM (Q-011 à Q-026) -> 16 questions x 2 graphies = 32 lignes
    # Équilibre : A, B, C, D
    # =========================================================================
    # Q-011 (Santé - Gold: C)
    {"id": "Q-011", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "santé", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "حميد ضرّاتو ضرسة العقل، مشا عند دونتيست فالعشية حيدها ليه وعطاه الدوا.",
     "question": "شنو دار حميد عند الطبيب؟", "choix_a": "دار راديو لرجلو", "choix_b": "عبر الطانسيو", "choix_c": "حيد ضرسة العقل", "choix_d": "دار عملية على عينو", "gold": "C"},
    {"id": "Q-011", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "santé", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "7mid derrato dersat l39el, mcha 3nd dentiste f l3chiya 7yedha lih w 3tah ddwa.",
     "question": "Chnou dar 7mid 3nd tbib?", "choix_a": "dar radio l rejlou", "choix_b": "3ber ttansyou", "choix_c": "7yed dersat l39el", "choix_d": "dar 3amaliya 3la 3aynou", "gold": "C"},

    # Q-012 (Administration - Gold: A)
    {"id": "Q-012", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "administration", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "رشيد مشا للمقاطعة باش يصادق على العقد، لقا الزحام بزاف وتسنى نوبتو حتى لتماش.",
     "question": "علاش مشا رشيد للمقاطعة؟", "choix_a": "باش يليزالي العقد", "choix_b": "باش يجدد الباسبور", "choix_c": "باش يشري طوموبيل", "choix_d": "باش يدفع للفيزا", "gold": "A"},
    {"id": "Q-012", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "administration", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Rachid mcha l lmo9ata3a bach yssade9 3la l3a9d, l9a zze7am bzaf w tsenna noubto 7tta ltmmach.",
     "question": "3lach mcha Rachid l lmo9ata3a?", "choix_a": "bach ylegaliser l3a9d", "choix_b": "bach yjedded lbasspor", "choix_c": "bach ychri tomobil", "choix_d": "bach ydfa3 l visa", "gold": "A"},

    # Q-013 (Sport - Gold: D)
    {"id": "Q-013", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "sport", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "المنتخب المغربي ربح الماتش بجوج لواحد، وسجل النصيري هدف واعر بالراس فالشوط الثاني.",
     "question": "كيفاش تسجل الهدف ديال النصيري؟", "choix_a": "ببيلانتي", "choix_b": "بتير من بعيد", "choix_c": "ضد مرماه", "choix_d": "بالراس", "gold": "D"},
    {"id": "Q-013", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "sport", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Lmontakhab lmoghribi rbe7 lmatch b jouj l wa7ed, w sejjel En-Nesyri hadaf wa3er b rras f chawt ttani.",
     "question": "Kifach tsejjel lhadaf dyal En-Nesyri?", "choix_a": "b penalty", "choix_b": "b tir mn b3id", "choix_c": "dedd marmatou", "choix_d": "b rras", "gold": "D"},

    # Q-014 (Cuisine - Gold: B)
    {"id": "Q-014", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "cuisine", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "نهار الجمعة، جمعات الوالدة العائلة كلها ودارت ليهم قصعة د كسكسو بالسبع خضاري واللبن.",
     "question": "شنو وجدات الوالدة نهار الجمعة؟", "choix_a": "طاجين د الحوت", "choix_b": "قصعة د كسكسو باللبن", "choix_c": "بسطيلة د الدجاج", "choix_d": "رفيسة بالحلية", "gold": "B"},
    {"id": "Q-014", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "cuisine", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Nhar jjomo3a, jem3at lwalida l3a2ila kamla w daret lihom 9es3a d ksekso b sbe3 khdari w lben.",
     "question": "Chnou wejdat lwalida nhar jjomo3a?", "choix_a": "tajin d l7out", "choix_b": "9es3a d ksekso b lben", "choix_c": "pastilla d ddjaj", "choix_d": "rfissa b l7elba", "gold": "B"},

    # Q-015 (Météo - Gold: A)
    {"id": "Q-015", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "météo", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "طاحت الشتا خيط من السما، الشوارع فايضين والناس هازين المظلات كيجريو للديور.",
     "question": "كيفاش كان الحال على برا؟", "choix_a": "الشتا خيط من السما", "choix_b": "الصهد والشمس حارة", "choix_c": "الثلج كيطيح بزاف", "choix_d": "العجاج والغبرة", "gold": "A"},
    {"id": "Q-015", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "météo", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Ta7et chta khit mn ssma, chawari3 faydin w nass hazin lmdallat kayjriw l ddyour.",
     "question": "Kifach kan l7al 3la berra?", "choix_a": "chta khit mn ssma", "choix_b": "sshed w chems 7arra", "choix_c": "ttelj kayti7 bzaf", "choix_d": "l3jaj w lghobra", "gold": "A"},

    # Q-016 (Technologie - Gold: C)
    {"id": "Q-016", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "technologie", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "التلفون ديال أنس طاح ليه فالما وتطفى، داه للمصلح بدّل ليه لافيشور ورجع خدام.",
     "question": "شنو بدّل المصلح فالتلفون؟", "choix_a": "الباتري", "choix_b": "الباف د الصوت", "choix_c": "لافيشور", "choix_d": "الكاميرا", "gold": "C"},
    {"id": "Q-016", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "technologie", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Ttilifoun dyal Anass ta7 lih f lma w ttfa, ddah l lmosli7 beddel lih l'afficheur w rje3 khddam.",
     "question": "Chnou beddel lmosli7 f ttilifoun?", "choix_a": "lbattrie", "choix_b": "lbaf d ssawt", "choix_c": "l'afficheur", "choix_d": "lkamera", "gold": "C"},

    # =========================================================================
    # 2. NOUVEAU NLI (N-005 à N-008) -> 4 contextes x 3 labels = 12 paires = 24 lignes
    # Équilibre strict : implication, contradiction, neutre
    # =========================================================================
    # N-005 (Amine - Baccalauréat)
    {"id": "N-005a", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "école", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "أمين جاب الباك بميزة حسن جدا وفرحات العائلة.", "texte_2": "أمين نجح فالامتحان د الباك.", "gold": "implication"},
    {"id": "N-005a", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "école", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Amine jab lbac b mizat 7assan jiddan w fer7at l3a2ila.", "texte_2": "Amine nje7 f lmtihan d lbac.", "gold": "implication"},
    {"id": "N-005b", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "école", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "أمين جاب الباك بميزة حسن جدا وفرحات العائلة.", "texte_2": "أمين سقط فهاد العام.", "gold": "contradiction"},
    {"id": "N-005b", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "école", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Amine jab lbac b mizat 7assan jiddan w fer7at l3a2ila.", "texte_2": "Amine s9et f had l3am.", "gold": "contradiction"},
    {"id": "N-005c", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "école", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "أمين جاب الباك بميزة حسن جدا وفرحات العائلة.", "texte_2": "أمين غادي يدير كلية الطب العام الجاي.", "gold": "neutre"},
    {"id": "N-005c", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "école", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Amine jab lbac b mizat 7assan jiddan w fer7at l3a2ila.", "texte_2": "Amine ghadi ydir kolliyat ttibb l3am jjay.", "gold": "neutre"},

    # N-006 (Salma - Voyage Turquie)
    {"id": "N-006a", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "voyage", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "سلمى ركبات فالطيارة متوجهة لتركيا باش تدوز العطلة.", "texte_2": "سلمى مسافرة خارج المغرب.", "gold": "implication"},
    {"id": "N-006a", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "voyage", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Salma rekbat f ttiyara motawajjiha l Tourkia bach ddozewez l3otla.", "texte_2": "Salma msafra kharij lmoghrib.", "gold": "implication"},
    {"id": "N-006b", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "voyage", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "سلمى ركبات فالطيارة متوجهة لتركيا باش تدوز العطلة.", "texte_2": "سلمى باقا كالسة فدارهم فكازا.", "gold": "contradiction"},
    {"id": "N-006b", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "voyage", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Salma rekbat f ttiyara motawajjiha l Tourkia bach ddozewez l3otla.", "texte_2": "Salma ba9a galsa f darhom f Casa.", "gold": "contradiction"},
    {"id": "N-006c", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "voyage", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "سلمى ركبات فالطيارة متوجهة لتركيا باش تدوز العطلة.", "texte_2": "سلمى كتعرف تهضر بالتركية مزيان.", "gold": "neutre"},
    {"id": "N-006c", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "voyage", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Salma rekbat f ttiyara motawajjiha l Tourkia bach ddozewez l3otla.", "texte_2": "Salma kat3ref thder b ttourkia mzyan.", "gold": "neutre"},

    # =========================================================================
    # 3. NOUVELLE CONVERSION (C-011 à C-018) -> 8 phrases x 2 graphies = 16 lignes
    # =========================================================================
    {"id": "C-011", "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "vie courante", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "فين وصلتي، راني كنتسناك حدا المحطة.", "gold": "Fin wselti, rani kantsnak 7da lma7atta.", "gold_alt": "fin wsliti, rani kantsenak 7da lmahata.|fen wselti rani kantsnak."},
    {"id": "C-011", "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "vie courante", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Fin wselti, rani kantsnak 7da lma7atta.", "gold": "فين وصلتي، راني كنتسناك حدا المحطة."},

    {"id": "C-012", "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "santé", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "خاصك تشرب الدوا فوقتو وتبع الريجيم.", "gold": "Khassek tchreb ddwa f we9to w ttebbe3 rrijim.", "gold_alt": "khasek tchrob dwa f weqto w tebe3 rijim.|khask tchreb ddwa."},
    {"id": "C-012", "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "santé", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Khassek tchreb ddwa f we9to w ttebbe3 rrijim.", "gold": "خاصك تشرب الدوا فوقتو وتبع الريجيم."},

    {"id": "C-013", "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "travail", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "صيفط ليا الإيميل باش نشوف الدوسي اليوم.", "gold": "Seyfet lia l'email bach nchouf ddossier lyoma.", "gold_alt": "sift liya l email bach nchof dossier lyom.|sayfet lia l'email."},
    {"id": "C-013", "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "travail", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Seyfet lia l'email bach nchouf ddossier lyoma.", "gold": "صيفط ليا الإيميل باش نشوف الدوسي اليوم."},

    {"id": "C-014", "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "achats", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "عفاك شحال الحساب كامل؟", "gold": "3afak ch7al l7ssab kamel?", "gold_alt": "3afak chhal lhesab kamel?|3afak ch7al le7ssab kamel?"},
    {"id": "C-014", "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "achats", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "3afak ch7al l7ssab kamel?", "gold": "عفاك شحال الحساب كامل؟"}
]

df_append = pd.DataFrame(test_rows).reindex(columns=df_current.columns)
df_total = pd.concat([df_current, df_append], ignore_index=True)

# Vérifier qu'il n'y a pas d'écrasement ou doublon
df_total.to_excel(PATH, index=False)
print(f"✅ Ajout terminé dans {PATH} !")
print(f"Total actuel : {len(df_total)} lignes (Ancien : {len(df_current)}, Ajoutés : {len(df_append)})")