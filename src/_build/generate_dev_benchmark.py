import os
import pandas as pd

COLS = [
    "id", "tache", "graphie", "split", "texte", "texte_2", "question",
    "choix_a", "choix_b", "choix_c", "choix_d", "gold", "gold_alt", 
    "cs", "source", "theme", "difficulty", "reviewed_by", "notes"
]

rows = [
    # =========================================================================
    # 1. QCM (Q-001 à Q-010) - 10 questions x 2 graphies = 20 lignes
    # =========================================================================
    # Q-001 (Achats - Gold: B)
    {"id": "Q-001", "tache": "qcm", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "achats", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "مشا أحمد للحانوت فالصباح، شرا الخبز والحليب. ملي رجع، لقا مو كتسناه باش يفطرو.",
     "question": "شنو شرا أحمد؟", "choix_a": "اللحم والخضرة", "choix_b": "الخبز والحليب", "choix_c": "أتاي والسكر", "choix_d": "الحوت والروز", "gold": "B"},
    {"id": "Q-001", "tache": "qcm", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "achats", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Mcha A7med l7anout f sba7, chra lkhobz w l7lib. Mlli rje3, l9a mmo katsnah bach yfetro.",
     "question": "Chnou chra A7med?", "choix_a": "l7em w lkhodra", "choix_b": "lkhobz w l7lib", "choix_c": "atay w sokkar", "choix_d": "l7out w rrouz", "gold": "B"},

    # Q-002 (Santé - Gold: A)
    {"id": "Q-002", "tache": "qcm", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "santé", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "فاطمة عيانة بزاف اليوم، فيها السخانة وراها ناعسة فالدار وممشاتش للخدمة.",
     "question": "علاش فاطمة ممشاتش للخدمة؟", "choix_a": "حيت مريضة وناعسة", "choix_b": "حيت عندها عطلة", "choix_c": "حيت سافرات لمراكش", "choix_d": "حيت تشرات طوموبيل", "gold": "A"},
    {"id": "Q-002", "tache": "qcm", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "santé", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Fatima 3yana bzaf lyoma, fiha skhana wraha na3sa fddar w mamchatx lkhedma.",
     "question": "3lax Fatima mamchatx lkhedma?", "choix_a": "7it mrita w na3sa", "choix_b": "7it 3ndha 3otla", "choix_c": "7it safrat l Merrakch", "choix_d": "7it tchrat tomobil", "gold": "A"},

    # Q-003 (Transport - Gold: C)
    {"id": "Q-003", "tache": "qcm", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "transport", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "ياسين كيقرا فكلية العلوم، كل نهار كياخد الطرامواي مع السبعة باش مايوصلش معطل.",
     "question": "باش كيمشي ياسين للكلية؟", "choix_a": "بالطوبيس", "choix_b": "بالطاكسي صغير", "choix_c": "بالطرامواي", "choix_d": "على رجليه", "gold": "C"},
    {"id": "Q-003", "tache": "qcm", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "transport", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Yassine kay9ra f kollfyat l3ouloum, kol nhar kayakhod ttramway m3a ssb3a bach maywsalch m3ettel.",
     "question": "Bach kaymchi Yassine l lkollia?", "choix_a": "b ttobis", "choix_b": "b ttaxi sghir", "choix_c": "b ttramway", "choix_d": "3la rejlih", "gold": "C"},

    # Q-004 (Loisirs - Gold: D)
    {"id": "Q-004", "tache": "qcm", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "loisirs", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "الجو زوين هاد الويكاند فالرباط، والناس خرجو كاملين يتساراو فلوضاية ويتبرعو بالهوا د البحر.",
     "question": "فين مشاو الناس يتساراو؟", "choix_a": "فمولاي يعقوب", "choix_b": "فجامع الفنا", "choix_c": "فالمطار", "choix_d": "فلوضاية", "gold": "D"},
    {"id": "Q-004", "tache": "qcm", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "loisirs", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Ljow zwin had lweekend f Rbat, w nass kherjo kamlin ytsaraw f Lodayat w ytber3o b lhwa d lb7ar.",
     "question": "Fin mchaw nass ytsaraw?", "choix_a": "f Moulay Ya39oub", "choix_b": "f Jame3 lfna", "choix_c": "f lmatar", "choix_d": "f Lodayat", "gold": "D"},

    # Q-005 (Éducation - Gold: B)
    {"id": "Q-005", "tache": "qcm", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "école", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "كريم عندو امتحان السيمانة الجاية، طفا التلفزة والتلفون وبدا كيراجع دروسو مزيان.",
     "question": "شنو دار كريم باش يراجع؟", "choix_a": "مشا يلعب كورة", "choix_b": "طفا التلفزة والتلفون", "choix_c": "نعس بكري", "choix_d": "سافر مع صحابو", "gold": "B"},
    {"id": "Q-005", "tache": "qcm", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "école", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Karim 3ndo mtihan simana jjaya, tfa ttalvaza w ttilifoun w bda kayraja3 drouso mzyan.",
     "question": "Chnou dar Karim bach yraja3?", "choix_a": "mcha yl3eb koura", "choix_b": "tfa ttalvaza w ttilifoun", "choix_c": "n3es bekri", "choix_d": "safer m3a s7abo", "gold": "B"},

    # Q-006 (École - Gold: B)
    {"id": "Q-006", "tache": "qcm", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "école", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "فاطمة فاقت مع السبعة، وجدت راسها ومشات للمدرسة. ملي وصلات، لقات القسم مسدود حيث الأستاذ مريض.",
     "question": "علاش ما قراوش التلاميذ؟", "choix_a": "حيث فاطمة تأخرات", "choix_b": "حيث الأستاذ مريض", "choix_c": "حيث المدرسة مسدودة بالعطلة", "choix_d": "حيث التلاميذ مشاو للدار", "gold": "B"},
    {"id": "Q-006", "tache": "qcm", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "école", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Fatima fa9t m3a sb3a, wjdat rasha w mchat lmdrassa. Mlli wslat, l9at l9sm msdoud 7it l2ostad mrid.",
     "question": "3lach ma 9rawch ttlamd?", "choix_a": "7it Fatima t2khrat", "choix_b": "7it l2ostad mrid", "choix_c": "7it lmdrassa msdouda b l3otla", "choix_d": "7it ttlamd mchaw ldar", "gold": "B"},

    # Q-007 (Maison - Gold: C)
    {"id": "Q-007", "tache": "qcm", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "maison", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "الباب د الدار تبلوكا وما بغاش يتحل، عيطنا على النجار جا فالصباح صاوب الساقطة.",
     "question": "شكون صاوب الباب؟", "choix_a": "الصباغ", "choix_b": "الميكانيكيان", "choix_c": "النجار", "choix_d": "مول الحانوت", "gold": "C"},
    {"id": "Q-007", "tache": "qcm", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "maison", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Lbab d ddar tblouka w mabghach yt7el, 3eyetna 3la nnejjar ja f sba7 sawb ssa9ta.",
     "question": "Chkoun sawb lbab?", "choix_a": "ssabbagh", "choix_b": "lmikanikyan", "choix_c": "nnejjar", "choix_d": "moul l7anout", "gold": "C"},

    # Q-008 (Fêtes - Gold: D)
    {"id": "Q-008", "tache": "qcm", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "fêtes", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "مريم كتوجد للحفلة د التخرج ديالها، شرات قفطان غوز وطالون باش تبان زوينة.",
     "question": "شنو شرات مريم للحفلة؟", "choix_a": "جلابة كحلة", "choix_b": "كسوة زرقاء", "choix_c": "صاية خضراء", "choix_d": "قفطان غوز وطالون", "gold": "D"},
    {"id": "Q-008", "tache": "qcm", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "fêtes", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Meryem katwjed l l7afla d ttkhorroj dyalha, chrat 9ftan rose w talon bach tban zwina.",
     "question": "Chnou chrat Meryem l l7afla?", "choix_a": "jellaba k7la", "choix_b": "keswa zer9a", "choix_c": "saya khedra", "choix_d": "9ftan rose w talon", "gold": "D"},

    # Q-009 (Voyage - Gold: A)
    {"id": "Q-009", "tache": "qcm", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "voyage", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "القطار د كازا تعطل نص ساعة حيت كان شي عطب تقني فالسكة.",
     "question": "علاش تعطل القطار؟", "choix_a": "حيت كاين عطب تقني", "choix_b": "حيت طاحت الشتا", "choix_c": "حيت كان عامر", "choix_d": "حيت سدو الماحطة", "gold": "A"},
    {"id": "Q-009", "tache": "qcm", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "voyage", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "L9itar d Casa t3ettel noss sa3a 7it kan chi 3atab ti9ni f ssekka.",
     "question": "3lach t3ettel l9itar?", "choix_a": "7it kayn 3atab ti9ni", "choix_b": "7it ta7et chta", "choix_c": "7it kan 3amer", "choix_d": "7it seddou lma7atta", "gold": "A"},

    # Q-010 (Nourriture - Gold: B)
    {"id": "Q-010", "tache": "qcm", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "cuisine", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "ملي دخل البرد، مشات العائلة كلها شربات بصارة سخونة بالزيت البلدية والكامون.",
     "question": "شنو شربات العائلة؟", "choix_a": "حريرة حامضة", "choix_b": "بصارة سخونة", "choix_c": "صوبة د الخضرة", "choix_d": "قهوة كحلة", "gold": "B"},
    {"id": "Q-010", "tache": "qcm", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "cuisine", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Mlli dkhel lberd, mchat l3a2ila kamla cherbat bissara skhouna b zzit lbeldia w lkamoun.",
     "question": "Chnou cherbat l3a2ila?", "choix_a": "7rira 7amda", "choix_b": "bissara skhouna", "choix_c": "soupa d lkhodra", "choix_d": "9ahwa k7la", "gold": "B"},

    # =========================================================================
    # 2. NLI (N-001 à N-004) - 4 contextes x 3 labels = 12 paires x 2 graphies = 24 lignes
    # =========================================================================
    # N-001 (Sara - Métier)
    {"id": "N-001a", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "travail", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "سارة خدامة فالسبيطار فرملية.", "texte_2": "سارة كتخدم.", "gold": "implication"},
    {"id": "N-001a", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "travail", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Sara khddama f sbitar fermlia.", "texte_2": "Sara katkhdem.", "gold": "implication"},
    {"id": "N-001b", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "travail", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "سارة خدامة فالسبيطار فرملية.", "texte_2": "سارة ما عندها حتى خدمة.", "gold": "contradiction"},
    {"id": "N-001b", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "travail", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Sara khddama f sbitar fermlia.", "texte_2": "Sara ma 3ndha 7tta khedma.", "gold": "contradiction"},
    {"id": "N-001c", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "travail", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "سارة خدامة فالسبيطار فرملية.", "texte_2": "سارة كتخلص مزيان.", "gold": "neutre"},
    {"id": "N-001c", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "travail", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Sara khddama f sbitar fermlia.", "texte_2": "Sara katkhelles mzyan.", "gold": "neutre"},

    # N-002 (Omar - Voiture)
    {"id": "N-002a", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "achats", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "عمر شرا طوموبيل جديدة كحلة البارح.", "texte_2": "عمر عندو دابا طوموبيل.", "gold": "implication"},
    {"id": "N-002a", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "achats", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Omar chra tomobil jdida k7la lbare7.", "texte_2": "Omar 3ndo daba tomobil.", "gold": "implication"},
    {"id": "N-002b", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "achats", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "عمر شرا طوموبيل جديدة كحلة البارح.", "texte_2": "عمر ما عمرو كسب طوموبيل.", "gold": "contradiction"},
    {"id": "N-002b", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "achats", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Omar chra tomobil jdida k7la lbare7.", "texte_2": "Omar ma 3mro kseb tomobil.", "gold": "contradiction"},
    {"id": "N-002c", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "achats", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "عمر شرا طوموبيل جديدة كحلة البارح.", "texte_2": "عمر عندو بيرمي قديم.", "gold": "neutre"},
    {"id": "N-002c", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "achats", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Omar chra tomobil jdida k7la lbare7.", "texte_2": "Omar 3ndo permi 9dim.", "gold": "neutre"},

    # N-003 (Tariq - Voyage train)
    {"id": "N-003a", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "transport", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "طارق قطع ورقة ديال البراق باش يسافر لطنجة.", "texte_2": "طارق غادي يسافر فالتران.", "gold": "implication"},
    {"id": "N-003a", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "transport", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Tariq 9te3 wer9a dyal Al Boraq bach ysafer l Tanger.", "texte_2": "Tariq ghadi ysafer f ttran.", "gold": "implication"},
    {"id": "N-003b", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "transport", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "طارق قطع ورقة ديال البراق باش يسافر لطنجة.", "texte_2": "طارق غادي يمشي راكب فكار.", "gold": "contradiction"},
    {"id": "N-003b", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "transport", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Tariq 9te3 wer9a dyal Al Boraq bach ysafer l Tanger.", "texte_2": "Tariq ghadi ymchi rakeb f kar.", "gold": "contradiction"},
    {"id": "N-003c", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "transport", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "طارق قطع ورقة ديال البراق باش يسافر لطنجة.", "texte_2": "طارق شاري هدايا لعائلتو.", "gold": "neutre"},
    {"id": "N-003c", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "transport", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Tariq 9te3 wer9a dyal Al Boraq bach ysafer l Tanger.", "texte_2": "Tariq chari hadaya l 3a2ilto.", "gold": "neutre"},

    # N-004 (Youssef - Travail)
    {"id": "N-004a", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "travail", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "يوسف مشا للخدمة مع السبعة ديال الصباح.", "texte_2": "يوسف خرج من الدار بكري.", "gold": "implication"},
    {"id": "N-004a", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "travail", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Youssef mcha lkhedma m3a sb3a dyal sba7.", "texte_2": "Youssef khrej mn ddar bekri.", "gold": "implication"},
    {"id": "N-004b", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "travail", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "يوسف مشا للخدمة مع السبعة ديال الصباح.", "texte_2": "يوسف بقا ناعس حتى للعشرة.", "gold": "contradiction"},
    {"id": "N-004b", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "travail", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Youssef mcha lkhedma m3a sb3a dyal sba7.", "texte_2": "Youssef b9a na3s 7tta l3chra.", "gold": "contradiction"},
    {"id": "N-004c", "tache": "nli", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "travail", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "يوسف مشا للخدمة مع السبعة ديال الصباح.", "texte_2": "يوسف خدام فشركة كبيرة.", "gold": "neutre"},
    {"id": "N-004c", "tache": "nli", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "travail", "difficulty": "medium", "reviewed_by": "self", "notes": "",
     "texte": "Youssef mcha lkhedma m3a sb3a dyal sba7.", "texte_2": "Youssef khddam f charika kbira.", "gold": "neutre"},

    # =========================================================================
    # 3. CONVERSION (C-001 à C-010) - 10 phrases x 2 graphies = 20 lignes
    # =========================================================================
    {"id": "C-001", "tache": "conversion", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "loisirs", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "عجبني هاد الفيلم بزاف.", "gold": "3jebni had lfilm bzaf.", "gold_alt": "3jbni had lfilm bzzaf.|3jebni had l film bzaf."},
    {"id": "C-001", "tache": "conversion", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "loisirs", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "3jebni had lfilm bzaf.", "gold": "عجبني هاد الفيلم بزاف."},

    {"id": "C-002", "tache": "conversion", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "voyage", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "فين غادي تمشي فهاد العطلة؟", "gold": "Fin ghadi tmchi fhad l3otla?", "gold_alt": "fin ghati tmchi fhad l3otla?|fen ghadi tmchi f had l3otla?"},
    {"id": "C-002", "tache": "conversion", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "voyage", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Fin ghadi tmchi fhad l3otla?", "gold": "فين غادي تمشي فهاد العطلة؟"},

    {"id": "C-003", "tache": "conversion", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "cuisine", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "الماكلة ديال هاد الريسطو بنينة ونقية.", "gold": "Lmakla dyal had rresto bnina w n9iya.", "gold_alt": "lmakla dial had resto bnina w nqiya."},
    {"id": "C-003", "tache": "conversion", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "cuisine", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Lmakla dyal had rresto bnina w n9iya.", "gold": "الماكلة ديال هاد الريسطو بنينة ونقية."},

    {"id": "C-004", "tache": "conversion", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "cuisine", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "ما كرهتش نشرب كاس د أتاي مشحر.", "gold": "Ma krehtch nchreb kas d atay mche77er.", "gold_alt": "makrehtch nchrob kas d atay mche7er."},
    {"id": "C-004", "tache": "conversion", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "cuisine", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Ma krehtch nchreb kas d atay mche77er.", "gold": "ما كرهتش نشرب كاس د أتاي مشحر."},

    {"id": "C-005", "tache": "conversion", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "services", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "سمح ليا، واش كتعرف فين كاين البنك؟", "gold": "Sme7 lia, wach kat3ref fin kayen lbank?", "gold_alt": "sme7liya, wach kat3ref fin kayn lbank?"},
    {"id": "C-005", "tache": "conversion", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "services", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Sme7 lia, wach kat3ref fin kayen lbank?", "gold": "سمح ليا، واش كتعرف فين كاين البنك؟"},

    {"id": "C-006", "tache": "conversion", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "achats", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "بغيت نمشي للسوق بكري.", "gold": "bghit nmchi lssou9 bekri.", "gold_alt": "bghit nmchi l sou9 bekri.|bghit nmchi lsou9 bkri."},
    {"id": "C-006", "tache": "conversion", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "achats", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "bghit nmchi lssou9 bekri.", "gold": "بغيت نمشي للسوق بكري."},

    {"id": "C-007", "tache": "conversion", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "achats", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "شحال كيدير هاد الكيلو ديال التفاح؟", "gold": "Ch7al kaydir had lkilo dyal tteffa7?", "gold_alt": "chhal kaydir had lkilo dial teffah?|ch7al kidir had lkilo d tfa7?"},
    {"id": "C-007", "tache": "conversion", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "achats", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Ch7al kaydir had lkilo dyal tteffa7?", "gold": "شحال كيدير هاد الكيلو ديال التفاح؟"},

    {"id": "C-008", "tache": "conversion", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "travail", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "بغيت نسولك على التوقيت ديال الخدمة غدا.", "gold": "Bghit nsowlek 3la tw9it dyal lkhedma ghedda.", "gold_alt": "bghit nsowlk 3la lwa9t dl khedma ghdda.|bghit nsewlek 3la taw9it dial lkhdma ghda."},
    {"id": "C-008", "tache": "conversion", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "travail", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Bghit nsowlek 3la tw9it dyal lkhedma ghedda.", "gold": "بغيت نسولك على التوقيت ديال الخدمة غدا."},

    {"id": "C-009", "tache": "conversion", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "travail", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "تبارك الله عليك، راك خدمتي مزيان فهاد المشروع.", "gold": "Tbarkellah 3lik, rak khedmeti mzyan fhad lmachrou3.", "gold_alt": "tbarkellah 3lik, rak khdemti mezyan f had lmachro3."},
    {"id": "C-009", "tache": "conversion", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "travail", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Tbarkellah 3lik, rak khedmeti mzyan fhad lmachrou3.", "gold": "تبارك الله عليك، راك خدمتي مزيان فهاد المشروع."},

    {"id": "C-010", "tache": "conversion", "graphie": "ar", "split": "dev", "cs": 0, "source": "original", "theme": "éducation", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "كنتمنى ليك التوفيق والنجاح فالامتحان ديالك.", "gold": "Kantmenna lik ttawfi9 w nnaja7 f lmtihan dyalek.", "gold_alt": "kantmna lik tawfiq w najah f limti7an dialk.|kantmenna lik tawfi9 w naja7."},
    {"id": "C-010", "tache": "conversion", "graphie": "lat", "split": "dev", "cs": 0, "source": "original", "theme": "éducation", "difficulty": "easy", "reviewed_by": "self", "notes": "",
     "texte": "Kantmenna lik ttawfi9 w nnaja7 f lmtihan dyalek.", "gold": "كنتمنى ليك التوفيق والنجاح فالامتحان ديالك."}
]

df = pd.DataFrame(rows).reindex(columns=COLS)
df["cs"] = df["cs"].fillna(0).astype(int)

os.makedirs("data/final", exist_ok=True)
out_path = "data/final/benchmark.xlsx"
df.to_excel(out_path, index=False)

print(f"✅ Créé avec succès : {out_path}")
print(f"Total : {len(df)} lignes (Toutes en split dev, prêtes pour validation !)")