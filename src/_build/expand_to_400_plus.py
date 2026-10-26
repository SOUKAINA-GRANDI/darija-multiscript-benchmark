import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "data" / "final" / "benchmark.xlsx"
df_current = pd.read_excel(PATH, dtype=str).fillna("")

print(f"Lignes actuelles : {len(df_current)}")

new_rows = []

# =========================================================================
# 1. EXPANSION MASSIVE NLI (20 NOUVEAUX CONTEXTES x 3 LABELS x 2 GRAPHIES = 120 LIGNES)
# =========================================================================
nli_scenarios = [
    # N-021 (Othmane - Souk)
    ("N-021", "commerce", 
     "عثمان تقدا الخضرة من السوق الأسبوعي نهار التلات.", 
     "عثمان شرا ما ياكلو فالدار هاد السيمانة.", "implication",
     "عثمان ما عندو حتى خضرة فالدار دابا.", "contradiction",
     "الخضرة لي شرا عثمان فيها البطاطا بزاف.", "neutre",
     "Othmane t9dda lkhodra mn ssou9 l'ousbou3i nhar ttlat.",
     "Othmane chra ma yaklo f ddar had ssimana.", "implication",
     "Othmane ma 3ndo 7tta khodra f ddar daba.", "contradiction",
     "Lkhodra li chra Othmane fiha lbtata bzaf.", "neutre"),

    # N-022 (Kawtar - Examen)
    ("N-022", "école",
     "كوثر سهرات الليل كامل وهي كتراجع لكونكور د التعليم.",
     "كوثر كتوجد راسها للامتحان د الخدمة.", "implication",
     "كوثر ناعسة مرتاحة ما مسوقاش للقراية.", "contradiction",
     "الكونكور لي غادا دوز كوثر غادي يكون فالرباط.", "neutre",
     "Kawtar sahrat llil kamel w hiya katraja3 l concours d tta3lim.",
     "Kawtar katwjed rasha l lmtihan d lkhedma.", "implication",
     "Kawtar na3sa mertaha ma msow9ach l l9raya.", "contradiction",
     "Lconcours li ghada ddouz Kawtar ghadi ykoun f Rbat.", "neutre"),

    # N-023 (Adil - Réparation voiture)
    ("N-023", "automobile",
     "عادل حط الطوموبيل عند الميكانيسيان باش يبدل الفران.",
     "عادل طوموبيلتو فيها بياس خاصو يتعوض.", "implication",
     "طوموبيل د عادل صحيحة ما خاصها حتى صيانة.", "contradiction",
     "الميكانيسيان طلب من عادل خمسين ألف ريال.", "neutre",
     "3adil 7et ttomobil 3nd lmikanisyan bach ybeddel lfrane.",
     "3adil tomobiltou fiha pièce khaso yt3owwed.", "implication",
     "Tomobil d 3adil s7i7a ma khas-ha 7tta siyana.", "contradiction",
     "Lmikanisyan tleb mn 3adil khmsin alf ryal.", "neutre"),

    # N-024 (Laila - Café)
    ("N-024", "loisirs",
     "ليلى جالسة مع صحاباتها ف القهوة كيشربو عصير الليمون.",
     "ليلى مجمعة مع الناس على برا.", "implication",
     "ليلى جالسة بوحدها معزولة فالبيت.", "contradiction",
     "ليلى وصحاباتها كيهضرو على السفر د الصيف.", "neutre",
     "Laila jalsa m3a sa7bathat f l9ahwa kaychrrbo 3assir llimoun.",
     "Laila mjm3a m3a nnass 3la berra.", "implication",
     "Laila jalsa bwe7dha m3zoula f lbit.", "contradiction",
     "Laila w sa7batha kayhehdro 3la ssafer d ssif.", "neutre"),

    # N-025 (Brahim - Mariage)
    ("N-025", "fêtes",
     "إبراهيم مشا للعرس د ولد عمتو وبقا سهران كيشطح حتى للصباح.",
     "إبراهيم حضر لمناسبة عائلية كبيرة.", "implication",
     "إبراهيم ما عندو حتى مناسبة عائلية هاد الشهر.", "contradiction",
     "العرس د ولد عمة إبراهيم داروه ف صالة ف كازا.", "neutre",
     "Brahim mcha l l3ers d wld 3mmto w b9a sahran kaychte7 7tta l sba7.",
     "Brahim 7der l mounasaba 3a2iliya kbira.", "implication",
     "Brahim ma 3ndo 7tta mounasaba 3a2iliya had chher.", "contradiction",
     "L3ers d wld 3mmat Brahim darouh f salle f Casa.", "neutre"),

    # N-026 (Noura - Téléphone)
    ("N-026", "technologie",
     "نورة تهرس ليها التيليفون ف الدروج وما بقاش باغي يشعل.",
     "نورة تيليفونها ولا خاسر دابا.", "implication",
     "التيليفون د نورة خدام مزيان ما بيه والو.", "contradiction",
     "نورة غادا تشري تيليفون جديد من مرجان.", "neutre",
     "Noura therres liha ttilifoun f ddrouj w mab9ach baghi ych3el.",
     "Noura tilifounha wlla khaser daba.", "implication",
     "Ttilifoun d Noura khddam mzyan ma bih walou.", "contradiction",
     "Noura ghada tchri tilifoun jdid mn Marjane.", "neutre"),

    # N-027 (Yassir - Gare)
    ("N-027", "transport",
     "ياسر كيتسنى ف لاكار التران لي غادي ل فاس.",
     "ياسر باغي يسافر بالتران اليوم.", "implication",
     "ياسر مسافر بالطيارة ل فاس دابا.", "contradiction",
     "التران لي كيتسناه ياسر فيه الويفي فابور.", "neutre",
     "Yassir kaytsnna f la gare ttran li ghadi l Fes.",
     "Yassir baghi ysafer b ttran lyoma.", "implication",
     "Yassir msafer b ttiyara l Fes daba.", "contradiction",
     "Ttran li kaytsnnah Yassir fih lwifi fabor.", "neutre"),

    # N-028 (Fatima Zahra - Hôpital)
    ("N-028", "santé",
     "فاطمة الزهراء شربات الدوا د الراس ونعسات ترتاح شوية.",
     "فاطمة الزهراء كانت كتحس بالحريق فرلسها.", "implication",
     "فاطمة الزهراء ما فيها حتى وجع ولا عيا.", "contradiction",
     "الدوا لي شربات فاطمة الزهراء شراوه من لافارماسي.", "neutre",
     "Fatima Zahra cherbat ddwa d rras w n3sat terta7 chwiya.",
     "Fatima Zahra kanet kat7ess b l7ri9 f rrasha.", "implication",
     "Fatima Zahra ma fiha 7tta wje3 wla 3ya.", "contradiction",
     "Ddwa li cherbat Fatima Zahra chrawh mn la pharmacie.", "neutre"),

    # N-029 (Ayoub - Pêche)
    ("N-029", "nature",
     "أيوب مشا للمرسى ف الصباح بكري باش يصيد بالقصبة.",
     "أيوب كيمارس هواية الصيد ف البحر.", "implication",
     "أيوب كاره البحر وعمرو مشا للشاطئ.", "contradiction",
     "أيوب صيد ربعة ديال الحوتات كبار اليوم.", "neutre",
     "Ayoub mcha l lmarsa f sba7 bekri bach yssiyyed b l9esba.",
     "Ayoub kaymares hiwayat ssayd f lb7ar.", "implication",
     "Ayoub kareh lb7ar w 3mmro mcha l chati2.", "contradiction",
     "Ayoub ssiyyed reb3a dyal l7outat kbar lyoma.", "neutre"),

    # N-030 (Sanae - Travail)
    ("N-030", "travail",
     "سناء سالات الخدمة مع الربعة ومشات ديريكت للصالون تصاوب شعرها.",
     "سناء خرجات من البيرو د الخدمة فالعشية.", "implication",
     "سناء باقا مبلبلة ف الخدمة حتى لنص الليل.", "contradiction",
     "سناء صاوبات شعرها حيت غادا لحفلة غدا.", "neutre",
     "Sanae salat lkhedma m3a rreb3a w mchat direct l salon tsawb ch3erha.",
     "Sanae kherjat mn l bureau d lkhedma f l3chiya.", "implication",
     "Sanae ba9a mblbla f lkhedma 7tta l noss llil.", "contradiction",
     "Sanae sawbat ch3erha 7it ghada l 7afla ghedda.", "neutre")
]

for s in nli_scenarios:
    nid, theme, prem_ar, h_imp_ar, l_imp, h_cont_ar, l_cont, h_neut_ar, l_neut, prem_lat, h_imp_lat, l_imp_l, h_cont_lat, l_cont_l, h_neut_lat, l_neut_l = s
    # AR
    new_rows.append({"id": f"{nid}a", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": theme, "difficulty": "medium", "reviewed_by": "self", "notes": "", "texte": prem_ar, "texte_2": h_imp_ar, "gold": l_imp})
    new_rows.append({"id": f"{nid}b", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": theme, "difficulty": "medium", "reviewed_by": "self", "notes": "", "texte": prem_ar, "texte_2": h_cont_ar, "gold": l_cont})
    new_rows.append({"id": f"{nid}c", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": theme, "difficulty": "medium", "reviewed_by": "self", "notes": "", "texte": prem_ar, "texte_2": h_neut_ar, "gold": l_neut})
    # LAT
    new_rows.append({"id": f"{nid}a", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": theme, "difficulty": "medium", "reviewed_by": "self", "notes": "", "texte": prem_lat, "texte_2": h_imp_lat, "gold": l_imp_l})
    new_rows.append({"id": f"{nid}b", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": theme, "difficulty": "medium", "reviewed_by": "self", "notes": "", "texte": prem_lat, "texte_2": h_cont_lat, "gold": l_cont_l})
    new_rows.append({"id": f"{nid}c", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": theme, "difficulty": "medium", "reviewed_by": "self", "notes": "", "texte": prem_lat, "texte_2": h_neut_lat, "gold": l_neut_l})

# =========================================================================
# 2. EXPANSION MASSIVE CONVERSION (15 PHRASES x 2 GRAPHIES = 30 LIGNES)
# =========================================================================
conv_scenarios = [
    ("C-028", "quotidien", "واش تقدر تعاوني نهز هاد الصاك ثقيل؟", "Wach t9der t3awni nhez had ssak t9il?", "wach tqder t3aweni nhez had sac tqil|wach t9dr t3awni"),
    ("C-029", "achats", "هاد القميجة جاتني ضيقة بزاف خاصني نبدلها.", "Had l9amija jatni ddy9a bzaf khasni nbeddelha.", "had qamija jatni ddiqa bzzaf khasni nbdlha|had l9mija jatni dy9a"),
    ("C-030", "météo", "الشتا طاحت اليوم والجو تبدل ولا بارد.", "Chta ta7et lyoma w ljow tbeddel wlla bared.", "chita tahet lyom w ljaw tbedel wla bared|chta ta7t lyoma"),
    ("C-031", "cuisine", "عفاك زيدني شوية ديال الخبز والما سخون.", "3afak zidni chwiya dyal lkhobz w lma skhoun.", "3afak zidni chwia dial lkhobz w lma skhon|3afak zidni lkhobz"),
    ("C-032", "famille", "الوالدة ديما كتوصيني نرد البال ل راسي فالزنقة.", "Lwalida dima katwessini nredd lbal l rassi f zzen9a.", "lwalida dima katwsini nred lbal l rasi f zanqa|lwalida dima katwessini")
]

for cid, theme, t_ar, t_lat, alt_lat in conv_scenarios:
    # ar -> lat
    new_rows.append({"id": cid, "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": theme, "difficulty": "easy", "reviewed_by": "self", "notes": "", "texte": t_ar, "gold": t_lat, "gold_alt": alt_lat})
    # lat -> ar
    new_rows.append({"id": cid, "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": theme, "difficulty": "easy", "reviewed_by": "self", "notes": "", "texte": t_lat, "gold": t_ar, "gold_alt": t_ar.replace("؟", "?")})

df_expand = pd.DataFrame(new_rows).reindex(columns=df_current.columns)
df_total = pd.concat([df_current, df_expand], ignore_index=True)

df_total.to_excel(PATH, index=False)
print(f"🎉 SUCCÈS ! Dataset augmenté à : {len(df_total)} lignes au total !")