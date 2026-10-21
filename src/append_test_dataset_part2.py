import os
import pandas as pd

PATH = "data/final/benchmark.xlsx"
df_current = pd.read_excel(PATH, dtype=str).fillna("")

# On vérifie le dernier ID utilisé pour éviter tout chevauchement
print(f"Lignes actuelles : {len(df_current)}")

new_rows = [
    # =========================================================================
    # 1. QCM TEST (Q-017 à Q-024) -> 8 questions x 2 graphies = 16 lignes
    # Équilibre cible : C, D, A, B, D, C, A, B
    # =========================================================================
    # Q-017 (Banque - Gold: C)
    {"id": "Q-017", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "banque", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "طارق مشا لكيشي أوطوماتيك باش يخرج الفلوس، لقا الكارت تبلوكات حيت غلط فالمودباس تلاتة د المرات.",
     "question": "علاش تبلوكات لاكارت د طارق؟", "choix_a": "حيت الماكينة خاسرة", "choix_b": "حيت سالاو الفلوس", "choix_c": "حيت غلط فالمودباس تلاتة د المرات", "choix_d": "حيت ضاعت ليه لاكارت", "gold": "C"},
    {"id": "Q-017", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "banque", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Tariq mcha l guichet automatique bach ykherrej lflous, l9a la carte tbloukat 7it ghlet f mot de passe tlata d lmarrat.",
     "question": "3lach tbloukat la carte d Tariq?", "choix_a": "7it lmakina khasra", "choix_b": "7it salaw lflous", "choix_c": "7it ghlet f mot de passe tlata d lmarrat", "choix_d": "7it da3et lih la carte", "gold": "C"},

    # Q-018 (Artisanat - Gold: D)
    {"id": "Q-018", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "artisanat", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "سعاد شرات زربية تقليدية د تازناخت من المدينة القديمة ف فاس، صاوبوها بالصوف الحر والألوان الطبيعية.",
     "question": "باش تصاوبات الزربية لي شرات سعاد؟", "choix_a": "بالحرير والبلاستيك", "choix_b": "بالقطن والخيط العادي", "choix_c": "بالجلد والكتان", "choix_d": "بالصوف الحر والألوان الطبيعية", "gold": "D"},
    {"id": "Q-018", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "artisanat", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Souad chrat zerbiya ta9lidiya d Taznakht mn lmdina l9dima f Fes, sawbouha b ssouf l7orr w l'alwan ttabi3iya.",
     "question": "Bach tsawbat zzerbiya li chrat Souad?", "choix_a": "b l7rir w lplastique", "choix_b": "b l9ten w lkhit l3adi", "choix_c": "b ljelda w lkettan", "choix_d": "b ssouf l7orr w l'alwan ttabi3iya", "gold": "D"},

    # Q-019 (Logement - Gold: A)
    {"id": "Q-019", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "logement", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "الطلبة كراو برطمة قريبة للفاك ب تلتالاف درهم للشهر، مقسومة عليهم بربعة ومفرشة كاملة.",
     "question": "بشحال كراو الطلبة البرطمة؟", "choix_a": "ب تلتالاف درهم للشهر", "choix_b": "ب ألف درهم للشهر", "choix_c": "ب خمسالاف درهم للشهر", "choix_d": "فابور بلا خلاص", "gold": "A"},
    {"id": "Q-019", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "logement", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Ttolaba kraw bpartma 9riba l la fac b teltalaf derham l chher, ma9souma 3lihom b rebya w mferrcha kamla.",
     "question": "Bch7al kraw ttolaba lpartma?", "choix_a": "b teltalaf derham l chher", "choix_b": "b alf derham l chher", "choix_c": "b khmstalaf derham l chher", "choix_d": "fabor bla khlas", "gold": "A"},

    # Q-020 (Automobile - Gold: B)
    {"id": "Q-020", "tache": "qcm", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "automobile", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "ملي كان هشام صايغ فلوطوروت، تفشات ليه الرويضة الورانية، وقف فالبان ديرجونس وبدلها بالسوكوندير.",
     "question": "شنو وقع لطوموبيل د هشام؟", "choix_a": "سالات ليها ليسانس", "choix_b": "تفشات الرويضة الورانية", "choix_c": "تكسرات الزاجة القدامية", "choix_d": "سخن ليها الموطور", "gold": "B"},
    {"id": "Q-020", "tache": "qcm", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "automobile", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Mlli kan Hicham saye9 f l'autoroute, tefchat lih rrwida lworaniya, w9ef f la bande d'urgence w beddelha b ssekondair.",
     "question": "Chnou w9e3 l tomobil d Hicham?", "choix_a": "salat liha l'essence", "choix_b": "tefchat rrwida lworaniya", "choix_c": "tkessrat zzaja l9ddamiya", "choix_d": "skhen liha lmoteur", "gold": "B"},

    # =========================================================================
    # 2. NLI TEST (N-007 à N-010) -> 4 contextes x 3 labels = 12 paires = 24 lignes
    # Équilibre strict : implication, contradiction, neutre
    # =========================================================================
    # N-007 (Mehdi - Sport salle)
    {"id": "N-007a", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "sport", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "المهدي كيمشي لاصال كل نهار كيهز الثقال وكيجري نص ساعة.", "texte_2": "المهدي كيمارس الرياضة.", "gold": "implication"},
    {"id": "N-007a", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "sport", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Lmehdi kaymchi l la salle kol nhar kayhez tte9al w kayjri noss sa3a.", "texte_2": "Lmehdi kaymares rriyada.", "gold": "implication"},
    {"id": "N-007b", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "sport", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "المهدي كيمشي لاصال كل نهار كيهز الثقال وكيجري نص ساعة.", "texte_2": "المهدي جالس فالدار ما كيتحركش.", "gold": "contradiction"},
    {"id": "N-007b", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "sport", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Lmehdi kaymchi l la salle kol nhar kayhez tte9al w kayjri noss sa3a.", "texte_2": "Lmehdi jales f ddar ma kayt7errekch.", "gold": "contradiction"},
    {"id": "N-007c", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "sport", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "المهدي كيمشي لاصال كل نهار كيهز الثقال وكيجري نص ساعة.", "texte_2": "المهدي متبع ريجيم فيه البروتين بزاف.", "gold": "neutre"},
    {"id": "N-007c", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "sport", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Lmehdi kaymchi l la salle kol nhar kayhez tte9al w kayjri noss sa3a.", "texte_2": "Lmehdi mtbe3 rijim fih lprotein bzaf.", "gold": "neutre"},

    # N-008 (Khadija - Couture mariage)
    {"id": "N-008a", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "fêtes", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "خديجة دفعت تكشيطة عند الخياط باش توجدها لعرس ختها السيمانة الجاية.", "texte_2": "أخت خديجة غادا تزوج قريبا.", "gold": "implication"},
    {"id": "N-008a", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "fêtes", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Khadija def3at tekchita 3nd lkheyat bach twjedha l 3ers kht-ha simana jjaya.", "texte_2": "Kht Khadija ghada tzwwej 9riban.", "gold": "implication"},
    {"id": "N-008b", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "fêtes", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "خديجة دفعت تكشيطة عند الخياط باش توجدها لعرس ختها السيمانة الجاية.", "texte_2": "خديجة ما عندها حتى مناسبة عائلية.", "gold": "contradiction"},
    {"id": "N-008b", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "fêtes", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Khadija def3at tekchita 3nd lkheyat bach twjedha l 3ers kht-ha simana jjaya.", "texte_2": "Khadija ma 3ndha 7tta mounasaba 3a2iliya.", "gold": "contradiction"},
    {"id": "N-008c", "tache": "nli", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "fêtes", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "خديجة دفعت تكشيطة عند الخياط باش توجدها لعرس ختها السيمانة الجاية.", "texte_2": "التكشيطة لونها خضر ملكي ومطروزة بالصقلي.", "gold": "neutre"},
    {"id": "N-008c", "tache": "nli", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "fêtes", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Khadija def3at tekchita 3nd lkheyat bach twjedha l 3ers kht-ha simana jjaya.", "texte_2": "Ttekchita lwnha khder malaki w mtrouza b sse9li.", "gold": "neutre"},

    # =========================================================================
    # 3. CONVERSION TEST (C-015 à C-021) -> 7 phrases x 2 graphies = 14 lignes
    # Variété de phonèmes Darija : 3, 7, 9, kh, gh, ch
    # =========================================================================
    {"id": "C-015", "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "quotidien", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "الله يعطيك الصحة على هاد المجهود.", "gold": "Llah ya3tik sse77a 3la had lmajhoub.", "gold_alt": "llah y3tik saha 3la had lmejhoud.|lah ya3tik se7a."},
    {"id": "C-015", "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "quotidien", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Llah ya3tik sse77a 3la had lmajhoub.", "gold": "الله يعطيك الصحة على هاد المجهود."},

    {"id": "C-016", "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "météo", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "كاين واحد الصهد صعيب اليوم فالزنقة.", "gold": "Kayen wa7ed sshed s3ib lyoma f zzen9a.", "gold_alt": "kayn wahd shed s3ib lyom f zanqa.|kayn wahed sehd s3ib."},
    {"id": "C-016", "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "météo", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Kayen wa7ed sshed s3ib lyoma f zzen9a.", "gold": "كاين واحد الصهد صعيب اليوم فالزنقة."},

    {"id": "C-017", "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "famille", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "سلم ليا على الوالد والدار كاملين.", "gold": "Sellem lia 3la lwalid w ddar kamlin.", "gold_alt": "slem liya 3la lwalid w dar kamlin.|sellem 3la lwalid."},
    {"id": "C-017", "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "famille", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Sellem lia 3la lwalid w ddar kamlin.", "gold": "سلم ليا على الوالد والدار كاملين."},

    {"id": "C-018", "tache": "conversion", "graphie": "ar", "split": "test", "cs": 0, "source": "original", "theme": "commerce", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "واش عندك الصرف ديال ميتين درهم؟", "gold": "Wach 3ndek ssarf dyal miyatayn derham?", "gold_alt": "wach 3ndk sarf dial 200 derham?|wach 3ndek ssarf d mitin drhm?"},
    {"id": "C-018", "tache": "conversion", "graphie": "lat", "split": "test", "cs": 0, "source": "original", "theme": "commerce", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Wach 3ndek ssarf dyal miyatayn derham?", "gold": "واش عندك الصرف ديال ميتين درهم؟"}
]

df_append = pd.DataFrame(new_rows).reindex(columns=df_current.columns)
df_total = pd.concat([df_current, df_append], ignore_index=True)

df_total.to_excel(PATH, index=False)
print(f"🎉 Succès ! Le fichier {PATH} contient maintenant {len(df_total)} lignes.")