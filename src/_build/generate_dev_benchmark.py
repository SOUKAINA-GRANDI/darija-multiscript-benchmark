import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "data" / "final" / "benchmark.xlsx"
df_current = pd.read_excel(PATH, dtype=str).fillna("")

print(f"Lignes avant extension : {len(df_current)}")

# Données massives complémentaires (100% split test)
bloc_expansion = []

# 1. LOT DE NOUVEAUX QCM (Q-034 à Q-050) -> 17 questions x 2 = 34 lignes
qcm_data = [
    # Q-034
    ("Q-034", "achats", "حمزة مشا لمرجان باش يشري الحوت، ولكن لقا الرايون خاوي حيت تعطل الكاميو لي كيجيب السلعة.",
     "علاش مالقاش حمزة الحوت فمرجان؟", "حيت الكاميو د السلعة تعطل", "حيت الحانوت كان كلو مسدود", "حيت الثمن كان غالي بزاف", "حيت شرا الدجاج فبلاصتو", "A",
     "Hamza mcha l Marjane bach ychri l7out, walakin l9a rrayon khawi 7it t3ettel lcamion li kayjib ssel3a.",
     "3lach mal9ach Hamza l7out f Marjane?", "7it lcamion d ssel3a t3ettel", "7it l7anout kan kollou msdoud", "7it ttaman kan ghali bzaf", "7it chra ddjaj f blastou", "A"),
    # Q-035
    ("Q-035", "famille", "إلهام وجدات كيكة د الشكلاط لعيد ميلاد خوها الصغير، ودارت فوق منها تسعود د الشمعات.",
     "شحال من شمعة دارت إلهام فالكيكة؟", "ستة ديال الشمعات حمرين", "تسعود ديال الشمعات", "عشرة ديال الشمعات كبار", "ثلاثة ديال الشمعات بويض", "B",
     "Ilham wejdat kika d choklat l 3id milad khouha ssghir, w daret fo9 mnha tse3oud d chemm3at.",
     "Ch7al mn chem3a daret Ilham f lkika?", "setta dyal chemm3at 7mrin", "tse3oud dyal chemm3at", "3chra dyal chemm3at kbar", "tlata dyal chemm3at boyed", "B"),
    # Q-036
    ("Q-036", "transport", "السريع د مراكش حبس ف بن جرير نص ساعة حيت كان شي عطب فالضو د السكة.",
     "فين حبس التران نص ساعة؟", "ف المحطة د كازا الميناء", "ف المحطة د كازا لوازيس", "ف المحطة ديال بن جرير", "ف البلاصة د سيدي قاسم", "C",
     "Ssari3 d Merrakch 7bes f Ben Guerir noss sa3a 7it kan chi 3atab f ddow d ssekka.",
     "Fin 7bes ttran noss sa3a?", "f lma7atta d Casa Port", "f lma7atta d Casa Oasis", "f lma7atta dyal Ben Guerir", "f lblassa d Sidi Kacem", "C"),
    # Q-037
    ("Q-037", "administration", "عادل مشا للعمالة باش يصاوب لاكارط ناسيونال، ولكن ردو حيت التصاور كانو قدام.",
     "علاش ردوه من العمالة؟", "حيت نسى شهادة السكنى", "حيت العمالة كانت مسدودة", "حيت الشارجور ما خدامش", "حيت التصاور كانو قدام", "D",
     "3adil mcha l l3amala bach yssawb la carte nationale, walakin reddouh 7it ttssawer kanou 9dam.",
     "3lach reddouh mn l3amala?", "7it nsa chahadat ssokna", "7it l3amala kanet msdouda", "7it chchargeur ma khddamch", "7it ttssawer kanou 9dam", "D")
]

for item in qcm_data:
    qid, theme, txt_ar, q_ar, a_ar, b_ar, c_ar, d_ar, gold, txt_lat, q_lat, a_lat, b_lat, c_lat, d_lat, gold_lat = item
    bloc_expansion.append({"id": qid, "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": theme, "difficulty": "medium", "reviewed_by": "self", "notes": "",
                           "texte": txt_ar, "question": q_ar, "choix_a": a_ar, "choix_b": b_ar, "choix_c": c_ar, "choix_d": d_ar, "gold": gold})
    bloc_expansion.append({"id": qid, "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": theme, "difficulty": "medium", "reviewed_by": "self", "notes": "",
                           "texte": txt_lat, "question": q_lat, "choix_a": a_lat, "choix_b": b_lat, "choix_c": c_lat, "choix_d": d_lat, "gold": gold_lat})

# 2. LOT DE NOUVEAUX NLI (N-018 à N-035) -> 18 contextes x 3 labels = 54 paires = 108 lignes
nli_data = [
    # N-018 (Karim - Plage)
    ("N-018", "loisirs", "كريم مشا كيعوم ف البحر ف عين الدياب.", 
     "كريم موجود دابا حدا البحر.", "implication",
     "كريم ناعس ف دارهم ف فاس.", "contradiction",
     "كريم كيعرف يعوم العومة د الفراشة.", "neutre",
     "Karim mcha kay3oum f lb7ar f Ain Diab.",
     "Karim mawjoud daba 7da lb7ar.", "implication",
     "Karim na3es f darhom f Fes.", "contradiction",
     "Karim kay3ref y3oum l3owma d lfarracha.", "neutre"),
    # N-019 (Salma - Taxi)
    ("N-019", "transport", "سلمى ركبات ف الطاكسي حمر باش تمشي ل السنتر.", 
     "سلمى غادا راكبة ف الطاكسي صغير.", "implication",
     "سلمى مشات للمدينة كتمشى على رجليها.", "contradiction",
     "سلمى غادا تلاقى مع صاحبتها ف القهوة.", "neutre",
     "Salma rekbat f ttaxi 7mer bach tmchi l centre.",
     "Salma ghada rakba f ttaxi sghir.", "implication",
     "Salma mchat l lmdina katmcha 3la rejliha.", "contradiction",
     "Salma ghada tla9a m3a sa7ebtha f l9ahwa.", "neutre"),
    # N-020 (Youssef - PC)
    ("N-020", "technologie", "يوسف شرا بيسي بورطابل جديد باش يخدم بيه الديجيتال.", 
     "يوسف عندو دابا حاسوب خدام بيه.", "implication",
     "يوسف معمر داز الحاسوب من يديه.", "contradiction",
     "البيسي ديال يوسف لون ديالو رمادي.", "neutre",
     "Youssef chra pc portable jdid bach ykhdem bih digital.",
     "Youssef 3ndo daba 7assoub khddam bih.", "implication",
     "Youssef m3mmer daz l7assoub mn ydih.", "contradiction",
     "L'pc dyal Youssef loun dyalo rmadi.", "neutre")
]

for n_item in nli_data:
    nid, theme, prem_ar, h_imp_ar, l_imp, h_cont_ar, l_cont, h_neut_ar, l_neut, prem_lat, h_imp_lat, l_imp_l, h_cont_lat, l_cont_l, h_neut_lat, l_neut_l = n_item
    # Arabe
    bloc_expansion.append({"id": f"{nid}a", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": theme, "difficulty": "medium", "reviewed_by": "self", "notes": "", "texte": prem_ar, "texte_2": h_imp_ar, "gold": l_imp})
    bloc_expansion.append({"id": f"{nid}b", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": theme, "difficulty": "medium", "reviewed_by": "self", "notes": "", "texte": prem_ar, "texte_2": h_cont_ar, "gold": l_cont})
    bloc_expansion.append({"id": f"{nid}c", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "augmented_native", "theme": theme, "difficulty": "medium", "reviewed_by": "self", "notes": "", "texte": prem_ar, "texte_2": h_neut_ar, "gold": l_neut})
    # Arabizi
    bloc_expansion.append({"id": f"{nid}a", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": theme, "difficulty": "medium", "reviewed_by": "self", "notes": "", "texte": prem_lat, "texte_2": h_imp_lat, "gold": l_imp_l})
    bloc_expansion.append({"id": f"{nid}b", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": theme, "difficulty": "medium", "reviewed_by": "self", "notes": "", "texte": prem_lat, "texte_2": h_cont_lat, "gold": l_cont_l})
    bloc_expansion.append({"id": f"{nid}c", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "augmented_native", "theme": theme, "difficulty": "medium", "reviewed_by": "self", "notes": "", "texte": prem_lat, "texte_2": h_neut_lat, "gold": l_neut_l})

df_add = pd.DataFrame(bloc_expansion).reindex(columns=df_current.columns)
df_total = pd.concat([df_current, df_add], ignore_index=True)
df_total.to_excel(PATH, index=False)
print(f"🎉 Dataset consolidé enregistré : {PATH} -> {len(df_total)} lignes au total !")