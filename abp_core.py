# abp_core.py - AB Group Predictor: קבוצת אבותינו לפי 37 סמני Y-STR
# נכתב ע"י יהודית בורר וד"ר שמחה גרשון בורר. https://github.com/sgbmzm/AB-PREDICTOR
# המודלים של קבוצות אבותינו לקוחים מאתר דנ"א-יהודי: https://jewishdna.net/ModalsAB.html
#
# החישוב: לכל קבוצה - סכום ההפרשים (בצעדים) בין הסמנים של הנבדק לסמנים של המודל שלה.
#  - סמן שהנבדק לא נבדק בו (0 / null / ריק) או שחסר במודל - לא נספר.
#  - סמן עם כמה אללים (DYS385, DYS464 וכו'): הפרש לכל אלל. אם מספר האללים שונה (למשל 4 מול 6 ב-DYS464),
#    הסמן מקבל עונש קבוע MISMATCH_STEPS (בגרסה של 2023 הוא קיבל 0, ואז מודלים עם 6 אללים יצאו קרובים מדי).
#  - המרחק מנורמל למספר הסמנים שהנבדק נבדק בהם, כך שמודל שחסר בו סמן לא מקבל יתרון.

import csv
import os
import re
import sys

LANG = "en"


def T(en, he):
    return he if LANG == "he" else en


MODELS_FILE = "2data37+A.csv"
# 37 הסמנים הראשונים בסדר של FTDNA (סמן עם כמה אללים - בעמודה אחת, האללים מופרדים במקף)
MARKERS = ["DYS393", "DYS390", "DYS19", "DYS391", "DYS385", "DYS426", "DYS388", "DYS439", "DYS389i", "DYS392",
           "DYS389ii", "DYS458", "DYS459", "DYS455", "DYS454", "DYS447", "DYS437", "DYS448", "DYS449", "DYS464",
           "DYS460", "Y-GATA-H4", "YCAII", "DYS456", "DYS607", "DYS576", "DYS570", "CDY", "DYS442", "DYS438"]
MISMATCH_STEPS = 2
EXAMPLE = "14,24,14,10,17-18,11,12,12,12,11,29,16,9-9,11,11,25,14,20,33,14-15-16-18,11,11,19-23,15,12,20,19,34-36,11,10"
EXAMPLE_DYS464 = "0,0,0,0,0-0,0,0,0,0,0,0,0,0-0,0,0,0,0,0,0,14-15-16-18"


def find_models_file(extra_dirs=()):
    """הקובץ נמצא בתיקייה required_files ליד הקוד, או בתוך התוכנה המותקנת (PyInstaller)"""
    here = os.path.dirname(os.path.abspath(__file__))
    for d in (*extra_dirs, getattr(sys, "_MEIPASS", ""), here, os.path.join(here, "required_files"),
              os.path.join(os.getcwd(), "required_files")):
        p = os.path.join(d, MODELS_FILE)
        if d and os.path.exists(p):
            return p
    return None


def load_models(path):
    """מחזיר רשימה של (קבוצה, הפלוגרופ, ערכים). הסמנים מתחילים בעמודה DYS393"""
    with open(path, encoding="utf-8-sig") as f:
        rows = [r for r in csv.reader(f) if r]
    start = rows[0].index("DYS393")
    return [(r[0].strip(), r[1].strip(), r[start:start + len(MARKERS)]) for r in rows[1:]]


def parse_markers(text):
    """קלט: ערכים מופרדים בטאב / פסיק / רווח. מחזיר עד 30 ערכים (37 הסמנים הראשונים)"""
    return [x for x in re.split(r"[\t,;\s]+", text.strip()) if x][:len(MARKERS)]


def _alleles(value):
    """'17-18' -> [17.0, 18.0]. None אם לא נבדק (0 / null / ריק). מעלה ValueError על ערך לא תקין"""
    v = (value or "").strip().lower()
    if v in ("", "null", "n/a", "-") or all(c in "0-." for c in v):
        return None
    return [float(a) for a in v.split("-")]


def marker_distance(a, b):
    """הפרש בצעדים בין שני ערכים של אותו סמן, או None אם אחד מהם לא נבדק"""
    pa, pb = _alleles(a), _alleles(b)
    if pa is None or pb is None:
        return None
    if len(pa) != len(pb):
        return MISMATCH_STEPS
    return sum(abs(x - y) for x, y in zip(pa, pb))


def distance(person, other):
    """מרחק בין הנבדק לשורת סמנים אחרת: (מרחק מנורמל, מרחק גולמי, מספר סמנים שהושוו)"""
    tested = [i for i, v in enumerate(person) if _alleles(v) is not None]
    raw, n = 0.0, 0
    for i in tested:
        d = marker_distance(person[i], other[i] if i < len(other) else "")
        if d is not None:
            raw += d
            n += 1
    norm = raw * len(tested) / n if n else float("inf")
    return norm, raw, n


def check_input(person):
    """רשימת שגיאות בקלט (ערך שאינו מספר). ריקה אם הקלט תקין"""
    bad = []
    for i, v in enumerate(person):
        try:
            _alleles(v)
        except ValueError:
            bad.append(f"{MARKERS[i]}={v}")
    return bad


def rank_groups(person, models):
    """כל הקבוצות, מהקרובה לרחוקה: (קבוצה, הפלוגרופ, מרחק מנורמל, מרחק גולמי, סמנים שהושוו)"""
    res = [(g, h, *distance(person, vals)) for g, h, vals in models]
    return sorted(res, key=lambda r: r[2])


def _fmt(x):
    return f"{x:g}" if x == int(x) else f"{x:.1f}"


def result_text(person, ranked, top=10, snp_groups=()):
    """טקסט התוצאה: 10 הקבוצות הקרובות, הפער בין הראשונה לשנייה, והשוואה לתוצאה לפי SNP (אם יש)"""
    n_tested = sum(1 for v in person if _alleles(v) is not None)
    lines = [T(f"Markers tested: {n_tested} of {len(MARKERS)} columns (37 markers)",
               f"סמנים שנבדקו: {n_tested} מתוך {len(MARKERS)} עמודות (37 סמנים)"),
             T("(A) = Ashkenazi group, (A+S) = Ashkenazim and Sephardim", "(A) = קבוצה אשכנזית, (A+S) = אשכנזים וספרדים"), ""]
    for i, (g, h, norm, raw, n) in enumerate(ranked[:top], 1):
        lines.append(T(f"{i}. {g}   {h}   distance {_fmt(norm)}", f"{i}. {g}   {h}   מרחק {_fmt(norm)}")
                     + (T(f" ({n} markers compared)", f" (הושוו {n} סמנים)") if n < n_tested else ""))
    if len(ranked) >= 2:
        gap = ranked[1][2] - ranked[0][2]
        lines += ["", T(f"Gap between 1st and 2nd: {_fmt(gap)}", f"הפער בין הראשונה לשנייה: {_fmt(gap)}")]
        if gap <= 2:
            lines.append(T("Small gap - the 2nd or 3rd group may be the right one. An SNP test decides.",
                           "פער קטן - ייתכן שהקבוצה השנייה או השלישית היא הנכונה. בדיקת SNP תכריע."))
    if n_tested < 12:
        lines.append(T("Few markers - the prediction is weak.", "מעט סמנים - הניבוי חלש."))
    for sg in snp_groups:
        pos = next((i for i, r in enumerate(ranked, 1) if r[0].split(" ")[0] == sg), None)
        if pos:
            lines.append(T(f"The Y-DNA tab (SNP) found {sg}: here it is number {pos}.",
                           f"בלשונית Y-DNA (לפי SNP) נמצאה {sg}: כאן היא במקום {pos}."))
    return "\n".join(lines)


def person_distance_text(p1, p2):
    norm, raw, n = distance(p1, p2)
    if not n:
        return T("No marker was tested in both.", "אין סמן שנבדק אצל שניהם.")
    return T(f"Distance between the two people: {_fmt(raw)} steps in {n} markers",
             f"המרחק בין שני האנשים: {_fmt(raw)} צעדים ב-{n} סמנים")
