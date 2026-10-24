import pandas as pd

COLS = [
    "id", "tache", "graphie", "split", "texte", "texte_2", "question",
    "choix_a", "choix_b", "choix_c", "choix_d", "gold", "gold_alt", "cs", "source"
]

rows = [
    # ==========================================
    # 1. QCM (Q-001 à Q-010) - Équilibre A, B, C, D
    # ==========================================
    # Q-001 (Gold: B)
    {"id": "Q-001", "tache": "qcm", "graphie": "ar", "split": "dev", "cs": 0, "source": "original",
     "texte": "مشا أحمد للحانوت فالصباح، شرا الخبز والحليب. ملي رجع، لقا مو كتسناه باش يفطرو.",
     "question": "شنو شرا أحمد؟",
     "choix_a": "اللحم والخضرة", "choix_b": "الخبز والحليب", "choix_c": "أتاي والسكر", "choix_d": "الحوت والروز", "gold": "B"},
    {"id": "Q-001", "tache": "qcm", "graphie": "lat", "split": "dev", "cs": 0, "source": "original",
     "texte": "Mcha A7med l7anout f sba7, chra lkhobz w l7lib. Mlli rje3, l9a mmo katsnah bach yfetro.",
     "question": "Chnou chra A7med?",
     "choix_a": "l7em w lkhodra", "choix_b": "lkhobz w l7lib", "choix_c": "atay w sokkar", "choix_d": "l7out w rrouz", "gold": "B"},

    # Q-002 (Gold: A)
    {"id": "Q-002", "tache": "qcm", "graphie": "ar", "split": "dev", "cs": 0, "source": "original",
     "texte": "فاطمة عيانة بزاف اليوم، فيها السخانة وراها ناعسة فالدار وممشاتش للخدمة.",
     "question": "علاش فاطمة ممشاتش للخدمة؟",
     "choix_a": "حيت مريضة وناعسة", "choix_b": "حيت عندها عطلة", "choix_c": "حيت سافرات لمراكش", "choix_d": "حيت تشرات طوموبيل", "gold": "A"},
    {"id": "Q-002", "tache": "qcm", "graphie": "lat", "split": "dev", "cs": 0, "source": "original",
     "texte": "Fatima 3yana bzaf lyoma, fiha skhana wraha na3sa fddar w mamchatx lkhedma.",
     "question": "3lax Fatima mamchatx lkhedma?",
     "choix_a": "7it mrita w na3sa", "choix_b": "7it 3ndha 3otla", "choix_c": "7it safrat l Merrakch", "choix_d": "7it tchrat tomobil", "gold": "A"},

    # Q-003 (Gold: C)
    {"id": "Q-003", "tache": "qcm", "graphie": "ar", "split": "dev", "cs": 0, "source": "original",
     "texte": "ياسين كيقرا فكلية العلوم بن مسيك، كل نهار كياخد الطرامواي مع السبعة باش مايوصلش معطل.",
     "question": "باش كيمشي ياسين للكلية؟",
     "choix_a": "بالطوبيس", "choix_b": "بالطاكسي صغير", "choix_c": "بالطرامواي", "choix_d": "على رجليه", "gold": "C"},
    {"id": "Q-003", "tache": "qcm", "graphie": "lat", "split": "dev", "cs": 0, "source": "original",
     "texte": "Yassine kay9ra f kollfyat l3ouloum Ben M'Sick, kol nhar kayakhod ttramway m3a ssb3a bach maywsalch m3ettel.",
     "question": "Bach kaymchi Yassine l lkollia?",
     "choix_a": "b ttobis", "choix_b": "b ttaxi sghir", "choix_c": "b ttramway", "choix_d": "3la rejlih", "gold": "C"},

    # Q-004 (Gold: D)
    {"id": "Q-004", "tache": "qcm", "graphie": "ar", "split": "dev", "cs": 0, "source": "original",
     "texte": "الجو زوين هاد الويكاند فالرباط، والناس خرجو كاملين يتساراو فلوضاية ويتبرعو بالهوا د البحر.",
     "question": "فين مشاو الناس يتساراو؟",
     "choix_a": "فمولاي يعقوب", "choix_b": "فجامع الفنا", "choix_c": "فالمطار", "choix_d": "فلوضاية", "gold": "D"},
    {"id": "Q-004", "tache": "qcm", "graphie": "lat", "split": "dev", "cs": 0, "source": "original",
     "texte": "Ljow zwin had lweekend f Rbat, w nass kherjo kamlin ytsaraw f Lodayat w ytber3o b lhwa d lb7ar.",
     "question": "Fin mchaw nass ytsaraw?",
     "choix_a": "f Moulay Ya39oub", "choix_b": "f Jame3 lfna", "choix_c": "f lmatar", "choix_d": "f Lodayat", "gold": "D"},

    # Q-005 (Gold: B)
    {"id": "Q-005", "tache": "qcm", "graphie": "ar", "split": "dev", "cs": 0, "source": "original",
     "texte": "كريم عندو امتحان السيمانة الجاية، طفا التلفزة والتلفون وبدا كيراجع دروسو مزيان.",
     "question": "شنو دار كريم باش يراجع؟",
     "choix_a": "مشا يلعب كورة", "choix_b": "طفا التلفزة والتلفون", "choix_c": "نعس بكري", "choix_d": "سافر مع صحابو", "gold": "B"},
    {"id": "Q-005", "tache": "qcm", "graphie": "lat", "split": "dev", "cs": 0, "source": "original",
     "texte": "Karim 3ndo mtihan simana jjaya, tfa ttalvaza w ttilifoun w bda kayraja3 drouso mzyan.",
     "question": "Chnou dar Karim bach yraja3?",
     "choix_a": "mcha yl3eb koura", "choix_b": "tfa ttalvaza w ttilifoun", "choix_c": "n3es bekri", "choix_d": "safer m3a s7abo", "gold": "B"},

    # ==========================================
    # 2. NLI (N-001 à N-004) - Implication / Contradiction / Neutre
    # ==========================================
    # N-001 (Sara)
    {"id": "N-001a", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original",
     "texte": "سارة خدامة فالسبيطار فرملية.", "texte_2": "سارة كتخدم.", "gold": "implication"},
    {"id": "N-001a", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original",
     "texte": "Sara khddama f sbitar fermlia.", "texte_2": "Sara katkhdem.", "gold": "implication"},
    {"id": "N-001b", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original",
     "texte": "سارة خدامة فالسبيطار فرملية.", "texte_2": "سارة ما عندها حتى خدمة.", "gold": "contradiction"},
    {"id": "N-001b", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original",
     "texte": "Sara khddama f sbitar fermlia.", "texte_2": "Sara ma 3ndha 7tta khedma.", "gold": "contradiction"},
    {"id": "N-001c", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original",
     "texte": "سارة خدامة فالسبيطار فرملية.", "texte_2": "سارة كتخلص مزيان.", "gold": "neutre"},
    {"id": "N-001c", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original",
     "texte": "Sara khddama f sbitar fermlia.", "texte_2": "Sara katkhelles mzyan.", "gold": "neutre"},

    # N-002 (Omar w tomobil)
    {"id": "N-002a", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original",
     "texte": "عمر شرا طوموبيل جديدة كحلة البارح.", "texte_2": "عمر عندو دابا طوموبيل.", "gold": "implication"},
    {"id": "N-002a", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original",
     "texte": "Omar chra tomobil jdida k7la lbare7.", "texte_2": "Omar 3ndo daba tomobil.", "gold": "implication"},
    {"id": "N-002b", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original",
     "texte": "عمر شرا طوموبيل جديدة كحلة البارح.", "texte_2": "عمر ما عمرو كسب طوموبيل.", "gold": "contradiction"},
    {"id": "N-002b", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original",
     "texte": "Omar chra tomobil jdida k7la lbare7.", "texte_2": "Omar ma 3mro kseb tomobil.", "gold": "contradiction"},
    {"id": "N-002c", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original",
     "texte": "عمر شرا طوموبيل جديدة كحلة البارح.", "texte_2": "عمر عندو رخصة السياقة قديمة.", "gold": "neutre"},
    {"id": "N-002c", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original",
     "texte": "Omar chra tomobil jdida k7la lbare7.", "texte_2": "Omar 3ndo rokhsat siya9a 9dima.", "gold": "neutre"},

    # ==========================================
    # 3. CONVERSION (C-001 à C-005)
    # ==========================================
    {"id": "C-001", "tache": "conversion", "graphie": "ar", "split": "dev", "cs": 0, "source": "original",
     "texte": "عجبني هاد الفيلم بزاف.",
     "gold": "3jebni had lfilm bzaf.", "gold_alt": "3jbni had lfilm bzzaf.|3jebni had l film bzaf."},
    {"id": "C-001", "tache": "conversion", "graphie": "lat", "split": "dev", "cs": 0, "source": "original",
     "texte": "3jebni had lfilm bzaf.", "gold": "عجبني هاد الفيلم بزاف."},

    {"id": "C-002", "tache": "conversion", "graphie": "ar", "split": "dev", "cs": 0, "source": "original",
     "texte": "فين غادي تمشي فهاد العطلة؟",
     "gold": "Fin ghadi tmchi fhad l3otla?", "gold_alt": "fin ghati tmchi fhad l3otla?|fen ghadi tmchi f had l3otla?"},
    {"id": "C-002", "tache": "conversion", "graphie": "lat", "split": "dev", "cs": 0, "source": "original",
     "texte": "Fin ghadi tmchi fhad l3otla?", "gold": "فين غادي تمشي فهاد العطلة؟"},

    {"id": "C-003", "tache": "conversion", "graphie": "ar", "split": "dev", "cs": 0, "source": "original",
     "texte": "الماكلة ديال هاد الريسطو بنينة ونقية.",
     "gold": "Lmakla dyal had rresto bnina w n9iya.", "gold_alt": "lmakla dial had resto bnina w nqiya."},
    {"id": "C-003", "tache": "conversion", "graphie": "lat", "split": "dev", "cs": 0, "source": "original",
     "texte": "Lmakla dyal had rresto bnina w n9iya.", "gold": "الماكلة ديال هاد الريسطو بنينة ونقية."},

    {"id": "C-004", "tache": "conversion", "graphie": "ar", "split": "dev", "cs": 0, "source": "original",
     "texte": "ما كرهتش نشرب كاس د أتاي مشحر.",
     "gold": "Ma krehtch nchreb kas d atay mche77er.", "gold_alt": "makrehtch nchrob kas d atay mche7er."},
    {"id": "C-004", "tache": "conversion", "graphie": "lat", "split": "dev", "cs": 0, "source": "original",
     "texte": "Ma krehtch nchreb kas d atay mche77er.", "gold": "ما كرهتش نشرب كاس د أتاي مشحر."},

    {"id": "C-005", "tache": "conversion", "graphie": "ar", "split": "dev", "cs": 0, "source": "original",
     "texte": "سمح ليا، واش كتعرف فين كاين البنك؟",
     "gold": "Sme7 lia, wach kat3ref fin kayen lbank?", "gold_alt": "sme7liya, wach kat3ref fin kayn lbank?"},
    {"id": "C-005", "tache": "conversion", "graphie": "lat", "split": "dev", "cs": 0, "source": "original",
     "texte": "Sme7 lia, wach kat3ref fin kayen lbank?", "gold": "سمح ليا، واش كتعرف فين كاين البنك؟"}
]

df = pd.DataFrame(rows).reindex(columns=COLS)
df["cs"] = df["cs"].fillna(0).astype(int)
df["source"] = df["source"].fillna("original")
df.to_excel("data/pilot/pilot.xlsx", index=False)
print(f"✅ Mis à jour avec succès : data/pilot/pilot.xlsx ({len(df)} lignes)")