"""Verification automatique des CSV du benchmark (bibliotheque standard uniquement).

Usage :  python src/validate_data.py            (verifie data/pilot)
         python src/validate_data.py data/final
"""
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ARABIC = re.compile(r"[\u0600-\u06FF]")
LATIN = re.compile(r"[A-Za-z]")
ARABIC_PUNCT = re.compile(r"[؟،؛]")
DIGIT = re.compile(r"\d")
ALLOWED_DIGITS = set("23679")        # 2 3 6 7 9 : lettres arabizi du guide
GRAPHIES = {"ar", "lat", "mix"}
SPLITS = {"dev", "test"}
NLI_LABELS = {"implication", "contradiction", "neutre"}

errors, warnings = [], []


def err(fichier, ligne, id_, msg):
    errors.append(f"[ERREUR] {fichier}:{ligne} ({id_}) {msg}")


def warn(fichier, ligne, id_, msg):
    warnings.append(f"[ATTENTION] {fichier}:{ligne} ({id_}) {msg}")


def read_csv(path, required):
    if not path.exists():
        errors.append(f"[ERREUR] fichier manquant : {path}")
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in required if c not in (reader.fieldnames or [])]
        if missing:
            errors.append(f"[ERREUR] {path.name} : colonnes manquantes {missing}")
            return []
        rows = list(reader)
    for i, r in enumerate(rows, start=2):
        r["_ligne"] = i
    return rows


def check_text(fichier, ligne, id_, champ, text, graphie):
    """Regles de script : arabe sans latin, arabizi sans arabe, pas de nombres en chiffres."""
    if not text.strip():
        err(fichier, ligne, id_, f"champ vide : {champ}")
        return
    if ARABIC_PUNCT.search(text):
        err(fichier, ligne, id_, f"{champ} : ponctuation arabe (utiliser ? , .)")
    if graphie == "ar":
        if LATIN.search(text):
            err(fichier, ligne, id_, f"{champ} : lettres latines dans une variante arabe")
        if DIGIT.search(text):
            err(fichier, ligne, id_, f"{champ} : chiffre dans une variante arabe (ecrire en lettres)")
    elif graphie == "lat":
        if ARABIC.search(text):
            err(fichier, ligne, id_, f"{champ} : lettres arabes dans une variante arabizi")
        bad = {d for d in text if d.isdigit() and d not in ALLOWED_DIGITS}
        if bad:
            err(fichier, ligne, id_, f"{champ} : chiffres hors convention {sorted(bad)}")
    for tok in text.split():
        t = tok.strip(".,?!;:()\"'")
        if t and t.isdigit():
            err(fichier, ligne, id_, f"{champ} : nombre en chiffres '{t}' (ecrire en lettres)")


def check_common(fichier, r, id_):
    if r.get("split") not in SPLITS:
        err(fichier, r["_ligne"], id_, f"split invalide : {r.get('split')!r} (dev ou test)")
    if r.get("cs") not in {"0", "1"}:
        err(fichier, r["_ligne"], id_, "cs doit valoir 0 ou 1")
    if r.get("relu") not in {"0", "1"}:
        err(fichier, r["_ligne"], id_, "relu doit valoir 0 ou 1")


def check_pairs(fichier, rows, key_fields):
    """Chaque contenu doit exister en 'ar' et 'lat', avec meme split et memes champs cles."""
    groups = defaultdict(dict)
    for r in rows:
        if r["graphie"] in groups[r["id"]]:
            err(fichier, r["_ligne"], r["id"], "doublon (id, graphie)")
        groups[r["id"]][r["graphie"]] = r
    for id_, variantes in groups.items():
        for g in ("ar", "lat"):
            if g not in variantes:
                any_r = next(iter(variantes.values()))
                err(fichier, any_r["_ligne"], id_, f"variante manquante : {g}")
        ref = next(iter(variantes.values()))
        for g, r in variantes.items():
            for f in key_fields:
                if r[f] != ref[f]:
                    err(fichier, r["_ligne"], id_, f"'{f}' differe entre variantes ({r[f]!r} vs {ref[f]!r})")
    return groups


def validate_qcm(d):
    f = "qcm.csv"
    cols = "id,graphie,split,texte,question,choix_a,choix_b,choix_c,choix_d,gold,theme,type_question,cs,relu,source".split(",")
    rows = read_csv(d / f, cols)
    for r in rows:
        id_ = r["id"]
        if r["graphie"] not in GRAPHIES:
            err(f, r["_ligne"], id_, f"graphie invalide : {r['graphie']!r} (ar, lat, mix)")
            continue
        check_common(f, r, id_)
        if r["gold"] not in {"A", "B", "C", "D"}:
            err(f, r["_ligne"], id_, "gold doit etre A, B, C ou D")
        for c in ("texte", "question", "choix_a", "choix_b", "choix_c", "choix_d"):
            check_text(f, r["_ligne"], id_, c, r[c], r["graphie"])
        n = len(r["texte"].split())
        if r["graphie"] != "mix" and not (15 <= n <= 90):
            warn(f, r["_ligne"], id_, f"texte de {n} mots (cible environ 30 a 70)")
    groups = check_pairs(f, rows, ["split", "gold", "cs", "theme"])
    ar = [g["ar"] for g in groups.values() if "ar" in g and g["ar"]["gold"] in "ABCD"]
    if ar:
        pos = Counter(r["gold"] for r in ar)
        print(f"QCM : {len(groups)} contenus ; bonnes reponses {dict(sorted(pos.items()))}")
        if len(ar) >= 12 and max(pos.values()) / len(ar) > 0.40:
            warnings.append("[ATTENTION] qcm.csv : positions de la bonne reponse desequilibrees")
        longest = sum(
            1 for r in ar
            if len(r["choix_" + r["gold"].lower()]) ==
            max(len(r[f"choix_{x}"]) for x in "abcd")
            and sorted(len(r[f"choix_{x}"]) for x in "abcd")[-1] != sorted(len(r[f"choix_{x}"]) for x in "abcd")[-2]
        )
        print(f"QCM : bonne reponse strictement la plus longue dans {longest}/{len(ar)} cas")
        if len(ar) >= 12 and longest / len(ar) > 0.40:
            warnings.append("[ATTENTION] qcm.csv : la bonne reponse est trop souvent la plus longue")
    return rows


def validate_nli(d):
    f = "nli.csv"
    cols = "id,groupe,graphie,split,premisse,hypothese,gold,theme,cs,relu,source".split(",")
    rows = read_csv(d / f, cols)
    for r in rows:
        id_ = r["id"]
        if r["graphie"] not in GRAPHIES:
            err(f, r["_ligne"], id_, f"graphie invalide : {r['graphie']!r}")
            continue
        check_common(f, r, id_)
        if r["gold"] not in NLI_LABELS:
            err(f, r["_ligne"], id_, f"etiquette invalide : {r['gold']!r}")
        for c in ("premisse", "hypothese"):
            check_text(f, r["_ligne"], id_, c, r[c], r["graphie"])
    groups = check_pairs(f, rows, ["split", "gold", "groupe", "cs", "theme"])
    # chaque premisse doit avoir les trois etiquettes, dans chaque graphie
    by_group = defaultdict(set)
    for r in rows:
        by_group[(r["groupe"], r["graphie"])].add(r["gold"])
    for (g, gr), labels in by_group.items():
        if labels != NLI_LABELS:
            warnings.append(f"[ATTENTION] nli.csv : groupe {g} ({gr}) a les etiquettes {sorted(labels)}, il manque {sorted(NLI_LABELS - labels)}")
    ar = [r for r in rows if r["graphie"] == "ar"]
    if ar:
        cnt = Counter(r["gold"] for r in ar)
        print(f"NLI : {len(groups)} paires ; etiquettes {dict(cnt)}")
        for lab in NLI_LABELS:
            lens = [len(r["hypothese"].split()) for r in ar if r["gold"] == lab]
            if lens:
                print(f"NLI : longueur moyenne de l'hypothese ({lab}) = {sum(lens)/len(lens):.1f} mots")
    return rows


def validate_conversion(d):
    f = "conversion.csv"
    cols = "id,direction,split,entree,gold,gold_alt,theme,cs,relu,source".split(",")
    rows = read_csv(d / f, cols)
    seen = set()
    for r in rows:
        id_ = r["id"]
        if id_ in seen:
            err(f, r["_ligne"], id_, "id en double")
        seen.add(id_)
        check_common(f, r, id_)
        if r["direction"] not in {"lat2ar", "ar2lat"}:
            err(f, r["_ligne"], id_, "direction doit etre lat2ar ou ar2lat")
            continue
        g_in, g_out = ("lat", "ar") if r["direction"] == "lat2ar" else ("ar", "lat")
        check_text(f, r["_ligne"], id_, "entree", r["entree"], g_in)
        check_text(f, r["_ligne"], id_, "gold", r["gold"], g_out)
        for alt in filter(None, (a.strip() for a in r["gold_alt"].split("|"))):
            check_text(f, r["_ligne"], id_, "gold_alt", alt, g_out)
    cnt = Counter(r["direction"] for r in rows)
    print(f"Conversion : {len(rows)} lignes ; directions {dict(cnt)}")
    return rows


def main():
    d = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/pilot")
    print(f"Verification du dossier : {d}\n")
    all_rows = validate_qcm(d) + validate_nli(d) + validate_conversion(d)
    print()
    sp = Counter(r.get("split") for r in all_rows)
    rl = Counter(r.get("relu") for r in all_rows)
    ex = sum(1 for r in all_rows if r.get("source") == "exemple")
    print(f"Splits : {dict(sp)} ; relues : {rl.get('1', 0)}/{len(all_rows)} ; lignes 'exemple' : {ex}")
    for m in warnings + errors:
        print(m)
    print(f"\n{len(errors)} erreur(s), {len(warnings)} avertissement(s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
