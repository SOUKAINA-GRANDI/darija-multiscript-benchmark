import pandas as pd

COLS = ["id", "tache", "graphie", "split", "texte", "texte_2", "question",
        "choix_a", "choix_b", "choix_c", "choix_d", "gold", "gold_alt", "cs", "source"]

rows = [
    # ---------- QCM ----------
    {"id": "Q-001", "tache": "qcm", "graphie": "ar", "split": "dev",
     "texte": "مشا أحمد للحانوت فالصباح، شرا الخبز والحليب. ملي رجع، لقا مو كتسناه باش يفطرو.",
     "question": "شنو شرا أحمد?",
     "choix_a": "اللحم والخضرة", "choix_b": "الخبز والحليب",
     "choix_c": "أتاي والسكر", "choix_d": "الحوت والروز", "gold": "B"},
    {"id": "Q-001", "tache": "qcm", "graphie": "lat", "split": "dev",
     "texte": "Mcha A7med l7anout f sba7, chra lkhobz w l7lib. Mlli rje3, l9a mmo katsnah bach yfetro.",
     "question": "Chnou chra A7med?",
     "choix_a": "l7em w lkhodra", "choix_b": "lkhobz w l7lib",
     "choix_c": "atay w sokkar", "choix_d": "l7out w rrouz", "gold": "B"},

    # ---------- NLI ----------
    {"id": "N-001a", "tache": "nli", "graphie": "ar", "split": "dev",
     "texte": "سارة خدامة فالسبيطار فرملية.", "texte_2": "سارة كتخدم.", "gold": "implication"},
    {"id": "N-001a", "tache": "nli", "graphie": "lat", "split": "dev",
     "texte": "Sara khddama f sbitar fermlia.", "texte_2": "Sara katkhdem.", "gold": "implication"},
    {"id": "N-001b", "tache": "nli", "graphie": "ar", "split": "dev",
     "texte": "سارة خدامة فالسبيطار فرملية.", "texte_2": "سارة ما عندها حتى خدمة.", "gold": "contradiction"},
    {"id": "N-001b", "tache": "nli", "graphie": "lat", "split": "dev",
     "texte": "Sara khddama f sbitar fermlia.", "texte_2": "Sara ma 3ndha 7tta khedma.", "gold": "contradiction"},
    {"id": "N-001c", "tache": "nli", "graphie": "ar", "split": "dev",
     "texte": "سارة خدامة فالسبيطار فرملية.", "texte_2": "سارة كتخلص مزيان.", "gold": "neutre"},
    {"id": "N-001c", "tache": "nli", "graphie": "lat", "split": "dev",
     "texte": "Sara khddama f sbitar fermlia.", "texte_2": "Sara katkhelles mzyan.", "gold": "neutre"},

    # ---------- CONVERSION ----------
    {"id": "C-001", "tache": "conversion", "graphie": "ar", "split": "dev",
     "texte": "عجبني هاد الفيلم بزاف.",
     "gold": "3jebni had lfilm bzaf.", "gold_alt": "3jbni had lfilm bzzaf.|3jebni had l film bzaf."},
    {"id": "C-001", "tache": "conversion", "graphie": "lat", "split": "dev",
     "texte": "3jebni had lfilm bzaf.", "gold": "عجبني هاد الفيلم بزاف."},
]

df = pd.DataFrame(rows).reindex(columns=COLS)
df["cs"] = df["cs"].fillna(0).astype(int)
df["source"] = df["source"].fillna("original")
df.to_excel("data/pilot/pilot.xlsx", index=False)
print(f"Créé : data/pilot/pilot.xlsx ({len(df)} lignes)")