# AB Group Predictor - קבוצת אבותינו לפי 37 סמני Y-STR
# נכתב ע"י יהודית בורר וד"ר שמחה גרשון בורר. הפרויקט: https://github.com/sgbmzm/AB-PREDICTOR
# הקובץ הזה הוא הממשק (tkinter). החישוב נמצא ב-abp_core.py

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tkinter as tk  # noqa: E402
from tkinter import filedialog, messagebox  # noqa: E402

import abp_core as core  # noqa: E402

# גרסה: MAJOR.MINOR.PATCH. MINOR עולה כשתוצאות עלולות להשתנות, PATCH כשלא משתנה כלום בתוצאות
APP_NAME = "ab_predictor"
APP_VERSION = "2.0.0"

RLE, PDF = "‫", "‬"
SETTINGS_FILE = "ab_predictor_settings.json"


def data_dir():
    try:
        from platformdirs import user_data_dir
        return user_data_dir(appname=APP_NAME, appauthor=False, roaming=False)
    except ImportError:
        return os.path.join(os.path.expanduser("~"), "." + APP_NAME)


def load_settings():
    try:
        with open(os.path.join(data_dir(), SETTINGS_FILE), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_settings(settings):
    try:
        os.makedirs(data_dir(), exist_ok=True)
        with open(os.path.join(data_dir(), SETTINGS_FILE), "w", encoding="utf-8") as f:
            json.dump(settings, f)
    except Exception:
        pass


def rtl(text):
    """כל שורה עטופה בסימני כיוון (RLE...PDF), כדי ש-Windows יציג אותה מימין לשמאל"""
    return "\n".join(RLE + x + PDF if x.strip() else x for x in str(text).split("\n"))


TERMS = (
    "The results of this program are estimates only, and may be wrong.\n"
    "They do not prove Jewish (or any other) ancestry, and must not be used alone for any decision.\n"
    "Use them with care, and only if you understand what they mean.\n"
    "All use is at your own responsibility; the authors are not responsible for any result or its use.\n\n"
    "תוצאות התוכנה הן הערכה בלבד, והן עלולות להיות שגויות.\n"
    "הן אינן מוכיחות מוצא יהודי (או כל מוצא אחר), ואין להסתמך עליהן לבדן בשום החלטה.\n"
    "יש להשתמש בהן בזהירות, ורק מי שמבין את משמעותן.\n"
    "כל שימוש הוא על אחריות המשתמש בלבד; לכותבי התוכנה אין אחריות על שום תוצאה או על השימוש בה.\n\n"
    "Do you agree? / האם אתה מסכים?")

HEBREW_WARNING = (
    "The Hebrew display is less good than the English one: tkinter does not fully support right-to-left text,\n"
    "so words and numbers may appear in the wrong place in a line. Check important results in English.\n\n"
    "התצוגה בעברית פחות טובה מהתצוגה באנגלית: tkinter לא תומך באופן מלא בטקסט מימין לשמאל,\n"
    "ולכן מילים ומספרים עלולים לקפוץ למקום הלא נכון בשורה. בדוק תוצאות חשובות באנגלית.\n\n"
    "Switch to Hebrew? / לעבור לעברית?")


def accept_terms(root, settings):
    """תנאי השימוש: פעם אחת לכל גרסה. מי שלא מסכים - התוכנה נסגרת"""
    if os.environ.get("ABP_ACCEPT_TERMS") == "1" or settings.get("terms_accepted") == APP_VERSION:
        return True
    root.withdraw()
    if not messagebox.askyesno("Terms of use / תנאי שימוש", TERMS, parent=root):
        root.destroy()
        return False
    settings["terms_accepted"] = APP_VERSION
    save_settings(settings)
    root.deiconify()
    return True


def main(first=True):
    settings = load_settings()
    lang = settings.get("lang", "en")  # ברירת המחדל: אנגלית
    core.LANG = lang
    he = lang == "he"

    def L(en, he_txt):
        return rtl(he_txt) if he else en

    root = tk.Tk()
    if first and not accept_terms(root, settings):
        return
    root.title(f"AB Group Predictor {APP_VERSION} | by Yehudit and Dr. Simcha Gershon Bohrer (PhD.)")
    root.geometry(f"{min(1000, root.winfo_screenwidth() - 40)}x{min(700, root.winfo_screenheight() - 90)}+10+10")

    path = core.find_models_file()
    models = core.load_models(path) if path else []

    tk.Label(root, font=("Arial", 11), justify="right" if he else "left", text=L(
        "Paste or type the first 37 Y-STR markers (FTDNA order), separated by tab, comma or space.\n"
        "A marker with several values (DYS385, DYS464...) is written with '-', for example 17-18.\n"
        "A missing marker before the ones you have: put 0 in its place.",
        "הדבק או הקלד את 37 סמני ה-Y-STR הראשונים (בסדר של FTDNA), מופרדים בטאב, פסיק או רווח.\n"
        "סמן עם כמה ערכים (DYS385, DYS464...) נכתב עם מקף, לדוגמא 17-18.\n"
        "סמן חסר לפני הסמנים שיש לך: לשים 0 במקומו.")).pack(pady=(8, 2))
    tk.Label(root, text=", ".join(core.MARKERS[:15]) + ",\n" + ", ".join(core.MARKERS[15:]), fg="gray30").pack()

    mode = tk.IntVar(value=1)
    rf = tk.Frame(root)
    rf.pack(pady=4)
    entry = tk.Entry(root, width=110, font=("Arial", 11))
    entry2 = tk.Entry(root, width=110, font=("Arial", 11))

    def set_mode():
        if mode.get() == 2:
            entry2.pack(after=entry, pady=2)
        else:
            entry2.pack_forget()

    tk.Radiobutton(rf, text=L("Compare to the AB groups", "השוואה לקבוצות אבותינו"), variable=mode, value=1,
                   command=set_mode).pack(side="left", padx=6)
    tk.Radiobutton(rf, text=L("Compare to another person (second box)", "השוואה לאדם נוסף (תיבה שנייה)"), variable=mode,
                   value=2, command=set_mode).pack(side="left", padx=6)
    entry.pack(pady=2)

    bf = tk.Frame(root)
    bf.pack(pady=4)
    out = tk.Text(root, height=22, width=100, font=("Arial", 11), wrap="word")
    out.tag_configure("rtl", justify="right")

    def show(text):
        out.config(state="normal")
        out.delete("1.0", "end")
        out.insert("1.0", rtl(text) if he else text, ("rtl",) if he else ())
        out.config(state="disabled")

    def put(text):
        entry.delete(0, "end")
        entry.insert(0, text)

    def calculate():
        p = core.parse_markers(entry.get())
        if not p:
            return show(core.T("Enter STR markers first.", "יש להזין קודם סמני STR."))
        p2 = core.parse_markers(entry2.get()) if mode.get() == 2 else None
        bad = core.check_input(p) + (core.check_input(p2) if p2 else [])
        if bad:
            return show(core.T("Values that are not numbers: ", "ערכים שאינם מספרים: ") + ", ".join(bad))
        if mode.get() == 2:
            return show(core.person_distance_text(p, p2 or []))
        if not models:
            return show(core.T(f"The file {core.MODELS_FILE} is missing.", f"הקובץ {core.MODELS_FILE} חסר."))
        show(core.result_text(p, core.rank_groups(p, models)))

    def save():
        f = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")])
        if f:
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(entry.get() + "\n\n" + out.get("1.0", "end").replace(RLE, "").replace(PDF, ""))

    def paste():
        try:
            put(root.clipboard_get().strip()[:400])
        except tk.TclError:
            pass

    def switch_language():
        if not he and not messagebox.askokcancel("Hebrew display / תצוגה בעברית", HEBREW_WARNING):
            return
        settings["lang"] = "en" if he else "he"
        save_settings(settings)
        root.destroy()
        main(first=False)

    for txt, cmd in ((L("Paste", "הדבק"), paste), (L("Example", "דוגמא"), lambda: put(core.EXAMPLE)),
                     (L("Example: DYS464 only", "דוגמא: DYS464 בלבד"), lambda: put(core.EXAMPLE_DYS464)),
                     (L("Clear", "נקה"), lambda: (entry.delete(0, "end"), entry2.delete(0, "end"), show("")))):
        tk.Button(bf, text=txt, command=cmd).pack(side="left", padx=4)
    tk.Button(bf, text=L("Calculate", "חשב"), font=("Arial", 11, "bold"), command=calculate).pack(side="left", padx=12)
    tk.Button(bf, text=L("Save results to TXT", "שמור תוצאות לקובץ TXT"), command=save).pack(side="left", padx=4)
    tk.Button(bf, text="עברית / English", command=switch_language).pack(side="left", padx=4)
    out.pack(fill="both", expand=True, padx=8, pady=4)
    tk.Label(root, fg="gray30", text=L(
        "Models: JewishDNA (jewishdna.net/ModalsAB.html) with Avotaynu Online - all rights to the data are theirs. "
        "A prediction only - an SNP test decides.",
        "המודלים: JewishDNA ‏(jewishdna.net/ModalsAB.html) עם Avotaynu Online - כל הזכויות בנתונים שלהם. "
        "ניבוי בלבד - בדיקת SNP מכריעה.")).pack(pady=(0, 6))
    root.mainloop()


if __name__ == "__main__":
    main()
