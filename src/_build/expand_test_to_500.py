import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "data" / "final" / "benchmark.xlsx"
df_current = pd.read_excel(PATH, dtype=str).fillna("")

print(f"Lignes actuelles : {len(df_current)}")

large_test_items = [
    # =========================================================================
    # 1. NOUVEAUX QCM TEST (Distracteurs calibrés de longueurs égales)
    # Équilibre parfait A, B, C, D
    # =========================================================================
    # Q-025 (Gold: C)
    {"id": "Q-025", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "commerce", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "سعيد شرا تلفازة ذكية، ولكن ملي وصل لدار لقا التيليكوموند ناقصة فالكرطونة، فرجع للحانوت يبدلها.",
     "question": "علاش رجع سعيد للحانوت فالبلاصة؟",
     "choix_a": "حيت التلفازة لقاها مهرسة", "choix_b": "حيت الصورة ما واضحاش بزاف", "choix_c": "حيت ناقصة التيليكوموند تما", "choix_d": "حيت بغا يرجع كاع فلوسو دابا", "gold": "C"},
    {"id": "Q-025", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "commerce", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Sa3id chra talvaza dkiya, walakin mlli wsel lddar l9a ttélécommande na9sa f lkartouna, rje3 l l7anout ybeddelha.",
     "question": "3lach rje3 Sa3id l l7anout flblassa?",
     "choix_a": "7it ttalvaza l9aha mherrsa", "choix_b": "7it ssoura ma wadhach bzaf", "choix_c": "7it na9sa ttélécommande tmma", "choix_d": "7it bgha yrje3 ga3 flouso daba", "gold": "C"},

    # Q-026 (Gold: A)
    {"id": "Q-026", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "travail", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "المدير طلب من الموظفين يحبسو الخدمة بكري حيت كاين انقطاع ديال الضو مبرمج فالزنقة مع الجوج.",
     "question": "شنو هو السبب لتوقيف الخدمة؟",
     "choix_a": "حيت الضو غادي يتقطع تماك", "choix_b": "حيت كاين اجتماع طارئ دابا", "choix_c": "حيت سالات ساعات الخدمة رسميا", "choix_d": "حيت الموظفين جاو عيانين اليوم", "gold": "A"},
    {"id": "Q-026", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "travail", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Lmodir tleb mn lmowaddafin y7ebso lkhedma bekri 7it kayn in9ita3 dyal ddow mbermej f zzen9a m3a jjoj.",
     "question": "Chnou houwa ssabab l tw9if lkhedma?",
     "choix_a": "7it ddow ghadi yt9te3 tmmak", "choix_b": "7it kayn ijtima3 tari2 daba", "choix_c": "7it salat sa3at lkhedma rsemiyan", "choix_d": "7it lmowaddafin jaw 3yanin lyoma", "gold": "A"},

    # Q-027 (Gold: D)
    {"id": "Q-027", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "transport", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "يونس كان غادي للمطار، ولكن لقا لوطوروت مبلوكية بحادثة سير، فاضطر يدوز من الطريق الوطنية.",
     "question": "علاش بدل يونس الطريق ديالو؟",
     "choix_a": "حيت سالا ليه المازوط فالطريق", "choix_b": "حيت الطوموبيل سخنات ليه بزاف", "choix_c": "حيت بغا يشوف صاحبو فالطريق", "choix_d": "حيت لوطوروت تبلوكات بحادثة", "gold": "D"},
    {"id": "Q-027", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "transport", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Younes kan ghadi l lmatar, walakin l9a l'autoroute mbloukiya b 7adita d ssir, f dtar ydouz mn tri9 lwataniya.",
     "question": "3lach beddel Younes tri9 dyalo?",
     "choix_a": "7it sala lih lmazot f tri9", "choix_b": "7it ttomobil skhnat lih bzaf", "choix_c": "7it bgha ychouf sa7bo f tri9", "choix_d": "7it l'autoroute tbloukat b 7adita", "gold": "D"},

    # Q-028 (Gold: B)
    {"id": "Q-028", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "santé", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "الطبيب نصح مصطفى يحبس السكر والملحة وينقص من الخبز الأبيض باش يهبط ليه الطانسيو.",
     "question": "شنو خاص يدير مصطفى باش يبرى؟",
     "choix_a": "خاصو يشرب القهوة بزاف ديما", "choix_b": "خاصو ينقص السكر والملحة والخبز", "choix_c": "خاصو ينعس النهار كامل فالدار", "choix_d": "خاصو يسافر للبحر يبدل الجو", "gold": "B"},
    {"id": "Q-028", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "santé", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Ttbib nse7 Mostafa y7bes ssokkar w lmel7a w yn9es mn lkhobz lbyed bach yhbet lih ttansyou.",
     "question": "Chnou khas ydir Mostafa bach ybra?",
     "choix_a": "khaso ychreb l9ahwa bzaf dima", "choix_b": "khaso yn9es ssokkar w lmel7a w lkhobz", "choix_c": "khaso yn3es nnhar kamel f ddar", "choix_d": "khaso ysafer l lb7ar ybeddel ljow", "gold": "B"},

    # Q-029 (Gold: C)
    {"id": "Q-029", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "école", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "الأستاذ لغى الحصة ديال الماط العشية حيت عندو اجتماع عاجل مع الإدارة د الكلية.",
     "question": "علاش تلغات الحصة د الماط؟",
     "choix_a": "حيت القاعة لقاها عامرة بناس", "choix_b": "حيت الطلبة غابو كاملين اليوم", "choix_c": "حيت عندو اجتماع مع الإدارة", "choix_d": "حيت ترونات السيمانة د العطلة", "gold": "C"},
    {"id": "Q-029", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "école", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "L'prof lgha l7essa dyal lmath l3chiya 7it 3ndo ijtima3 3ajil m3a l'idara d lkollia.",
     "question": "3lach tlghat l7essa d lmath?",
     "choix_a": "7it l9a3a l9aha 3amra b nass", "choix_b": "7it ttolaba ghabo kamlin lyoma", "choix_c": "7it 3ndo ijtima3 m3a l'idara", "choix_d": "7it trwnat ssimana d l3otla", "gold": "C"},

    # Q-030 (Gold: A)
    {"id": "Q-030", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "famille", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "العائلة كاملة قررات تعيد ف العروبية عند الجد حيت توحشو اللمة د الحباب والأجواء التقليدية.",
     "question": "فين قررات العائلة تدوز العيد؟",
     "choix_a": "ف العروبية عند الجد الكبير", "choix_b": "ف لوطيل على البحر فالمدينة", "choix_c": "ف دارهم فالمدينة بلا سفر", "choix_d": "ف دار عمهم الصغير فالرباط", "gold": "A"},
    {"id": "Q-030", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "famille", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "L3a2ila kamla 9errrat t3eyyed f l3roubiya 3nd jjdd 7it twa7cho lmma d l7bab w l'ajwa2 tta9lidiya.",
     "question": "Fin 9errrat l3a2ila ddozewez l3id?",
     "choix_a": "f l3roubiya 3nd jjdd lkbir", "choix_b": "f l'hôtel 3la lb7ar f lmdina", "choix_c": "f darhom f lmdina bla safer", "choix_d": "f dar 3mmhom ssghir f Rbat", "gold": "A"},

    # =========================================================================
    # 2. GRAND BLOC NLI TEST (Équilibre strict Implication / Contradiction / Neutre)
    # Plus de 30 nouvelles paires multigraphiques
    # =========================================================================
    # N-013 (Hakim - Train)
    {"id": "N-013a", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "transport", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "حكيم ركب فالتران د الرباط مع العشرة د الصباح.", "texte_2": "حكيم مسافر على برا د مدينتو.", "gold": "implication"},
    {"id": "N-013a", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "transport", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Hakim rkeb f ttran d Rbat m3a l3chra d sba7.", "texte_2": "Hakim msafer 3la berra d mdinto.", "gold": "implication"},
    {"id": "N-013b", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "transport", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "حكيم ركب فالتران د الرباط مع العشرة د الصباح.", "texte_2": "حكيم جالس دابا فدارو كيتفرج.", "gold": "contradiction"},
    {"id": "N-013b", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "transport", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Hakim rkeb f ttran d Rbat m3a l3chra d sba7.", "texte_2": "Hakim jales daba f daro kaytferrej.", "gold": "contradiction"},
    {"id": "N-013c", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "transport", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "حكيم ركب فالتران د الرباط مع العشرة د الصباح.", "texte_2": "حكيم غادي يحضر لعرس ف الرباط.", "gold": "neutre"},
    {"id": "N-013c", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "transport", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Hakim rkeb f ttran d Rbat m3a l3chra d sba7.", "texte_2": "Hakim ghadi ye7der l 3ers f Rbat.", "gold": "neutre"},

    # N-014 (Nadia - Cuisine)
    {"id": "N-014a", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "cuisine", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "نادية شرات الدجاج والحامض مصير والزيتون باش تطيب العشا.", "texte_2": "نادية كتعرف شنو باغا توجد للعشا.", "gold": "implication"},
    {"id": "N-014a", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "cuisine", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Nadia chrat ddjaj w l7amed mssiyer w zzitoun bach ttyeb l3cha.", "texte_2": "Nadia kat3ref chnou bagha twjed l l3cha.", "gold": "implication"},
    {"id": "N-014b", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "cuisine", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "نادية شرات الدجاج والحامض مصير والزيتون باش تطيب العشا.", "texte_2": "نادية معولة تاكل ف الريسطو الليلة.", "gold": "contradiction"},
    {"id": "N-014b", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "cuisine", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Nadia chrat ddjaj w l7amed mssiyer w zzitoun bach ttyeb l3cha.", "texte_2": "Nadia m3ewla takol f rresto llila.", "gold": "contradiction"},
    {"id": "N-014c", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "cuisine", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "نادية شرات الدجاج والحامض مصير والزيتون باش تطيب العشا.", "texte_2": "نادية عارضة على دار عمها كاملين.", "gold": "neutre"},
    {"id": "N-014c", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "cuisine", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Nadia chrat ddjaj w l7amed mssiyer w zzitoun bach ttyeb l3cha.", "texte_2": "Nadia 3arda 3la dar 3mmha kamlin.", "gold": "neutre"},

    # N-015 (Reda - Bourse d'études)
    {"id": "N-015a", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "éducation", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "رضى تقبل ف المنحة الدراسية ف فرنسا وغادي يمشي فالشتنبر.", "texte_2": "رضى عندو فرصة يقرا على برا.", "gold": "implication"},
    {"id": "N-015a", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "éducation", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Reda t9bel f lmin7a ddirasiya f Fransa w ghadi ymchi f septembre.", "texte_2": "Reda 3ndo forsa y9ra 3la berra.", "gold": "implication"},
    {"id": "N-015b", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "éducation", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "رضى تقبل ف المنحة الدراسية ف فرنسا وغادي يمشي فالشتنبر.", "texte_2": "الدوسي د المنحة د رضى ترفض نهائيا.", "gold": "contradiction"},
    {"id": "N-015b", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "éducation", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Reda t9bel f lmin7a ddirasiya f Fransa w ghadi ymchi f septembre.", "texte_2": "Ddossier d lmin7a d Reda trefd nihaiyan.", "gold": "contradiction"},
    {"id": "N-015c", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "éducation", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "رضى تقبل ف المنحة الدراسية ف فرنسا وغادي يمشي فالشتنبر.", "texte_2": "رضى لقا ديجا السكن الجامعي ف باريس.", "gold": "neutre"},
    {"id": "N-015c", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "éducation", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Reda t9bel f lmin7a ddirasiya f Fransa w ghadi ymchi f septembre.", "texte_2": "Reda l9a déja ssakan ljami3i f Paris.", "gold": "neutre"},

    # =========================================================================
    # 3. NOUVELLES CONVERSIONS TEST (avec variantes gold_alt complètes)
    # =========================================================================
    {"id": "C-025", "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "santé", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "راسي كيضرني بزاف خاصني نشرب شي كينة.", 
     "gold": "Rassi kayderni bzaf khasni nchreb chi kina.", 
     "gold_alt": "rasi kiderni bzzaf khassni nchrob kina|rassi kaydrni bzaf khasni kina"},
    {"id": "C-025", "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "santé", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Rassi kayderni bzaf khasni nchreb chi kina.", 
     "gold": "راسي كيضرني بزاف خاصني نشرب شي كينة.", 
     "gold_alt": "راسي كيضرني بزاف خاصني نشرب كينة|راسي كيضرني بزاف خاصني كينة"},

    {"id": "C-026", "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": "travail", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "غدا عندي مقابلة ديال الخدمة مع التسعود الصباح.", 
     "gold": "Ghedda 3ndi mo9abala dyal lkhedma m3a ttss3oud d sba7.", 
     "gold_alt": "ghda 3ndi entretient d lkhedma m3a 9 sba7|ghedda 3ndi moqabala dial lkhdma"},
    {"id": "C-026", "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": "travail", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Ghedda 3ndi mo9abala dyal lkhedma m3a ttss3oud d sba7.", 
     "gold": "غدا عندي مقابلة ديال الخدمة مع التسعود الصباح.", 
     "gold_alt": "غدا عندي مقابلة د الخدمة مع التسعود د الصباح|غدا عندي مقابلة ديال الخدمة مع 9 د الصباح"}
]

df_append = pd.DataFrame(large_test_items).reindex(columns=df_current.columns)
df_total = pd.concat([df_current, df_append], ignore_index=True)

df_total.to_excel(PATH, index=False)
print(f"🎉 Dataset étendu avec succès ! Total : {len(df_total)} lignes (100% split test pour les nouveaux ajouts).")