#!/usr/bin/env python
# coding: utf-8

# In[34]:


#!/usr/bin/env python
# coding: utf-8

# In[201]:


#!/usr/bin/env python
# coding: utf-8

# In[42]:


Description ='''\nThis Software Receives First 37 Y-STR Markers for Any Subject, and Examines What Is the Distance between It 
And The First 37 STR Markers of Each of the Models of "Avotainu": https://jewishdna.net/modalsab.html
The Subject Is Expected To Belong To One Of The groups That Is Closest To Them.
Usually, For More Than 12 Markers, the Prediction Is Very Accurate
it is also possible to calculate the distance between the First 37 STR markers of one person, and markers of another person
note! In case there is no match in the number of alleles for any marker, the calculation will skip this marker.
'''

credit='''This software was written by Yehudit and Dr. Simcha Gershon Bohrer'''

Instructions = '''Enter or paste STR Markers, separated by tab or comma 
Exactly According to the following order of markers, and the following examples 
If any marker is missing it is *before* the markers you have, you must put zero (0) in place'''

# לצורך רזולוציית המסך
import ctypes

# לצורך אייקון ועוד
import os
import sys

# לקריאת הנתונים מקובץ
import csv

# יבוא טקינטר
import tkinter as tk
import tkinter.font
from tkinter import messagebox as tkMessageBox
from tkinter import *
# שמירה לקובץ
from tkinter.filedialog import asksaveasfile, askopenfilename
    
import clipboard

# פתיחת קישור אינטרנט
from urllib.request import urlopen


#---------------------------
# פונקצייה לקבל מיקום מוחלט של קובץ שאמור להיות כלול בתוכנה
# ראו: https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/44352931#44352931
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
#----------------------------------------------


###################################################################

# משתנים כלליים

# לשימוש פונקציית ההדפסה ניתן להשתמש במספר גדול ממאה
MAX_DIST = 100

# כמה להרחיק אדם מהמודל אם מספר האללים בסמן פולימרפי שלו שונה ממספר האללים הרגיל של סמן זה
# בתחילה יהודית עשתה את זה 3 אבל לדעתי אין כל טעם בדבר.
# אני עשיתי אפס ולכן אם אין התאמה במספר האללים עבור סמן מסויים, פשוט לא מחשבים אותו, כאילו שהוא לא קיים. הוא לא מקריב ולא מרחיק מהמודל
MISMATCH_MARKER_DIST = 0

#########################################################
    
# חישוב המרחקים  בין האדם לבין כל קבוצות אבותינו

# פונקצייה שמחזירה מידע האם ניתן להפוך סטרינג מסויים - למספר שלם
def parse_to_int_if_possible(unknoun_type):
    try:
        int_type=int(unknoun_type)
        return int_type
    except:
        return unknoun_type

# חישוב מרחק בין סמן בודד לסמן מקביל באמצעות הפרש אבסולוטי
def distance(num1,num2):
    return(abs(num1-num2))

# חישוב מרחק בין סמן בודד שיש בו כמה אללים לסמן המקביל באמצעות ספליט על מקף המחבר בין האללים
def dist_of_str(person_item,data_item):
    str_dist=0
    arr_person_item=person_item.split('-')
    arr_data_item = data_item.split('-')
    if not(len(arr_person_item)==len(arr_data_item)):
        str_dist+=MISMATCH_MARKER_DIST
    else:
        for i in range(len(arr_person_item)):
            str_dist+=distance(int(arr_person_item[i]),int(arr_data_item[i]))
    return str_dist

# חישוב המרחקים עבור שורה שלמה של סמנים באמצעות הפונקציות שלעיל אבל למעשה זה נעשה לפי טורים שלמים של סמנים 
def dist_of_rows(person_row,data_row,markers_names,column_markers_start):
    
    # חשוב מאוד!! אם כפתור הבחירה מורה על השוואה לקבוצות אבותינו    
    if person2_or_all.get() == 1:
        # שורת דאטה עבור החישובים צריכה להתחיל מהמיקום השתיים, כי טורים אפס ואחד בקובץ של קבוצות אבותינו מכילים מידע שאינו שייך לסמני אס.טי אר
        data_row_for_calculats = data_row[column_markers_start:]
    # בכל מקרה אחר, כלומר מתי שמשווים בין שני אנשים, לא צריך להוריד טורים
    else:
        data_row_for_calculats = data_row
        
    # בתחילה המרחק של השורה שווה לאפס
    row_dist=0
    
    # # עבור כל סמן ברשימת הסמנים של הנבדק, החל מהמיקום השתיים, כי בשני המיקומים הראשונים אפס ואחד אין סמני אס.טי.אר
    for item in range(len(person_row)):
        
        # בדיקה באמצעות פונקצייה שלעיל על נתוני הנבדק וגם על נתוני קבוצות אבותינו האם אפשר להפוך אותם למספר שלם
        person_item=parse_to_int_if_possible(person_row[item])
        data_item=parse_to_int_if_possible(data_row_for_calculats[item])
        
        # אם יש מחיקה בסמן מסויים, או שהסמן הזה לא נבדק - אין לחשב כלום עבור סמן זה     
        if person_item in [0,'0',"0-0","0-0-0-0","0-0-0-0-0","0-0-0-0-0-0","0-0-0-0-0-0-0","null","NULL"]:
            # report_deleted_item(item)
            continue;
        
        # אם הסוג של סמן מסויים והסמן המקביל לו מאפשרים הפיכה למספר שלם, אז יש לחשב את המרחק ביניהם באמצעות פונקציית חישוב מרחק בודד
        if (type(person_item)==int and type(data_item)==int):
            row_dist+=distance(person_item,data_item)
        
        # אם מדובר בסוג שאי אפשר להפוך אותו למספר שלם, כגון סמן פולימרפי, טיפול בו ע"י פונקצייה ייעודית שלעיל באמצעות ספליט ואז חישוב מרחק    
        elif (type(person_item) == str and type(data_item) == str):
            row_dist+=dist_of_str(person_item,data_item)
              
        # בכל מקרה אחר, יש חוסר התאמה עבור סמן זה, ואז יש להוסיף מספר קבוע של מרחק מהמודל (מספר שהוגדר לעיל) 
        else:
            row_dist+=MISMATCH_MARKER_DIST
            
    return row_dist

# חישוב המרחקים עבור כל השורות של קבוצות אבותינו באמצעות הפונקציות שהוגדרו לעיל
def get_distances(person,whole,markers_names,column_markers_start):
    distances=[]
# אם כפתור הבחירה מורה על השוואה לאדם שני ולא לקבוצות אבותינו אז יש ב: הול-דאטא רק שורה אחת    
    if person2_or_all.get() == 2:
        distances.append(dist_of_rows(person,whole,markers_names,column_markers_start))
    else:
        for i in range(len(whole)):        
            distances.append(dist_of_rows(person,whole[i],markers_names,column_markers_start))
    return distances

##################################################################################

# def print calculations of distances from AB-MODALS (=data37) - manipulate solution

def print_min_match_rows(dist,person_data,whole_data,markers_names):
    
    # אם ההשוואה היא בין אדם 1 לאדם 2
    if person2_or_all.get() == 2:
        match_row=min(dist)
        txt.insert("end", f'\nThe distance between one person and another person is: {match_row}')
        
    # בכל מקרה אחר ההשוואה היא לכל קבוצות אבותינו
    else:   
        txt.insert("end", f'\nNOTE: (A) = Ashkenazi group, (A+S) = a group with Ashkenazim and Sephardim\n')
        txt.insert("end", f'\nFor the following STR markers:')
        txt.insert("end", f'\n {",".join(str(i) for i in person_data)}\n\n')

        # עשיתי מינוס שתיים כי אחרת רשימת ההשוואות לא נגמרת אלא מתחילה מחדש בסוף הרשימה של קבוצות אבותינו
        for i in range(len(whole_data)- 2):
            match_row=min(dist)
            ix=dist.index(match_row)
        
            # עשיתי איי פלוס אחד כדי שהספירה לא תתחיל מאפס אלא מאחד
            txt.insert("end", f'The {i+1} match model is:')
            txt.insert("end", f'\nAB Group: {whole_data[ix][0]} ---- ')
            txt.insert("end", f'Haplogroup (SNP): {whole_data[ix][1]} ---- ')
            txt.insert("end", f'The distance is: {match_row}')
            txt.insert("end", "\n")
            txt.insert("end", "\n")
    # לאחר שמצאנו את האינדקס של המספר המינימלי, הופכים אותו למספר גבוה על ידי הגדלתו במאה וכדומה, כדי ששוב פעם נוכל לחפש מה המספר המינימלי שיש במערך
            dist[ix]+=MAX_DIST

    # הגדרת העיצוב של הטקסט בתיבת הטקסט שיהיה ממורכז
    txt.tag_configure("center", justify='center')
    txt.tag_add("center", 1.0, "end")

    # סגירת תיבת הטקסט לקריאה בלבד
    txt.configure(state="disabled")

############  כל ההדפסות ###############

# פונקצייה לבדיקה האם להשתמש בקובץ קבוצות אבותינו ברירת מחדל או להשתמש בקובץ שהמשתמש יבחר
def get_file():
    if Check_file.get()==1:
        file = askopenfilename(title = "Select csv file",filetypes = (("CSV Files","*.csv"),))
    else:
        file = '2data37+A.csv'
    return file

# פונקצייה לקבלת הנתונים מתוך קובץ סי אס וי
def get_AB_data():
    file = get_file()
    csv_path = resource_path(file)
    with open(csv_path, 'r') as myFile:
        reader = csv.reader(myFile)
        whole_data = list(reader)
    return whole_data
    
# פונקציית מיין: סיכום סופי והדפסות עם הגדרות מיוחדות עבור ממשק משתמש גרפי של טקינטר
# פונקצייה זו מופעלת באמצעות הכפתור "חשב נתונים"
def main_result():
    
    # פתיחת תיבת הטקסט לעריכה ומחיקת מה שיש בה והוספת שורה ריקה
    # זה נעשה כבר כאן כדי שבכל מקרה - גם כשיש שגיאה - כל לחיצה חדשה על כפתור חישוב הנתונים תמחק את הנתונים הקודמים
    txt.configure(state="normal")
    txt.delete(1.0, END)
    #txt.insert("end", "\n")
    
    # הגדרת משתנה עם שמות כל 37 הסמנים הראשונים - לפי הסדר
    markers_names = ['DYS393', 'DYS390', 'DYS19', 'DYS391', 'DYS385', 'DYS426', 'DYS388', 'DYS439', 'DYS389i', 'DYS392', 'DYS389ii', 'DYS458', 'DYS459', 'DYS455', 'DYS454', 'DYS447', 'DYS437', 'DYS448', 'DYS449', 'DYS464', 'DYS460', 'Y-GATA-H4', 'YCAII', 'DYS456', 'DYS607', 'DYS576', 'DYS570', 'CDY', 'DYS442', 'DYS438']
    
# get person data (37 markers) from input    
    person = input_person_data.get().replace(" ","")
    if "\t" in person:
        arr_person = person.split('\t')
    elif "\t" not in person:
        arr_person = person.split(",")
    # בכוונה עד המיקום השלושים כי זה מכיל את 37 סמנים ראשונים
    person_data = arr_person[:30]
    
# אם כפתור הבחירה מורה על השוואה לאדם שני ולא לקבוצות אבותינו, קבלת נתוני האדם השני וחישוב ההפרש בינו לבין האדם הראשון    
    if person2_or_all.get() == 2:
        
        person2 = input_person_2.get().replace(" ","")
        
        if "\t" in person2:
            arr_person2 = person2.split('\t')
        elif "\t" not in person2:
            arr_person2 = person2.split(",")
        
        # בכוונה עד המיקום השלושים כי זה מכיל את 37 סמנים ראשונים
        person2_data = arr_person2[:30]
        
        # ניסיון לבדוק האם יש מספר במיקום הראשון שבתיבות קלט הסימנים של הנבדק
        try:
            is_person_int = int(person_data[0])
            is_person2_int = int(person2_data[0])
        except:
            is_person_int = "str"
            is_person2_int = "str"
        
        # אם שתי תיבות קלט הסמנים מתחילות במספר אז יש לבצע את כל החישובים
        if type(is_person_int) == int and type(is_person2_int) == int:
              
            # הטור הראשון הוא הסמן הראשון כי אין מידע נוסף לפני הזנת הסמן הראשון, בניגוד לקובץ קבוצות אבותינו שיש בו טורי מידע נוספים קודם לכן
            column_markers_start = 0

            # calculate distances for complete rows in data37
            dist=get_distances(person_data,person2_data,markers_names,column_markers_start)

            # print calculations of minimal distances from AB-MODALS
            print_min_match_rows(dist.copy(),person_data,person2_data,markers_names)
            
        # אם אחת מתיבות קלט הסמנים לא מתחילה במספר אז יש לכתוב הודעת שגיאה
        else:
            txt.insert("end", "\nERROR: There are no numbers in the inputs boxs")

    # בכל שאר המקרים ההשוואה תהיה לכל קבוצות אבותינו
    else:
        
        # ניסיון לבדוק האם יש מספר במיקום הראשון שבתיבת הסימנים של הנבדק
        try:
            is_person_int = int(person_data[0])
        except:
            is_person_int = "str"
        
        # אם תיבת הסמנים של האדם מתחילה במספר אז יש לבצע את כל החישובים
        if type(is_person_int) == int:
            
            #try:
            # קבלת כל המידע כל כל קבוצות אבותינו
            whole_data = get_AB_data()
            #except FileNotFoundError as q:
                
            #txt.insert("end", f"\nERROR: {q}")
            
            # מציאת מספר הטור שבו מתחילים הסמנים, לפי השורה הראשונה שבקובץ שבה בראש הטור של הסמן הראשון מופיע DYS393
            column_markers_start=whole_data[0].index("DYS393")
            
            # מכאן והלאה הסרתי מהחישוב את השורה הראשונה של הול-דאטא שהיא מכילה את שורת שמות הסמנים ולכן החישוב הוא רק מהמקום האחד במערך 
            whole_data = whole_data[1:] 

            # חישוב המרחקים מכל השורות של אבותינו באמצעות פונקצייה
            dist=get_distances(person_data,whole_data,markers_names,column_markers_start)

            # הדפסת המרחק מהמודל עבור כל שורה בקבוצות אבותינו באמצעות פונקצייה
            print_min_match_rows(dist.copy(),person_data,whole_data,markers_names)
        
        # אם תיבת הסמנים של האדם לא מתחילה במספר אז יש לכתוב הודעת שגיאה
        else:
            txt.insert("end", "\nERROR: There are no numbers in the input box")
            

#-----------------------------------------

# פונקצייה עבוק לחצן "נקה נתונים" לניקוי תיבות קלט התאריך
def clear_Entry():
    input_person_data.delete(0, END)
    
# פונקצייה עבוק לחצן "הדבק" להדבקת נתונים
def paste():
    input_person_data.delete(0, END)
    
    # Get the data from the clipboard
    cliptext = wnd.clipboard_get().replace("\t",",").replace(" ","")
    
    input_person_data.insert(0, cliptext[:350])
    
    
# פונקצייה עבוק לחצן "הדבק" להדבקת נתונים
def paste_example():
    input_person_data.delete(0, END)
    
    clipboard.copy(str(example)[2:-2])
    
    # Get the data from the clipboard
    cliptext = wnd.clipboard_get().replace("\t",",").replace(" ","")
    
    input_person_data.insert(0, cliptext[:120])

    # פונקצייה עבוק לחצן "הדבק" להדבקת נתונים
def paste_example_dys464():
    input_person_data.delete(0, END)
    
    clipboard.copy(str(example_dys464)[2:-2])
    
    # Get the data from the clipboard
    cliptext = wnd.clipboard_get().replace("\t",",").replace(" ","")
    
    input_person_data.insert(0, cliptext[:120])


#------------------------------------------------------------

# פונקצייה לכפתור העתקת הנתונים של קובץ הטקסט
# פונקצייה זו מופעלת על ידי כפתור "העתק תוצאות ללוח"
def copy_txt_to_clipboard():
    C = txt.get(1.0, END)
    clipboard.copy(C)


# פונקצייה לשמירה בשם של קובץ התוצאות    
def save_txt_to_path():
    C = txt.get(1.0, END)
    file = asksaveasfile(defaultextension=".txt")
    try:
        file.write(C)
        # במקרה שסוגרים את חלון שמירה בשם במקום ללחוץ על שמור יש שגיאת ארטיבוט
    except AttributeError:
        pass
    
    

#-----------------------------------------

if __name__ == '__main__':

    # מכאן והלאה עיצוב גרפי של ממשק המשתמש

    # התוכנית עצמה בתוך טקינטר וכל מה שקשור לטקינטר

    # הגדרת משתנה ששומר חלון טקינטר, והגדרת כותרת החלון ומינימום גודל החלון
    wnd=Tk()
    # הגדרה שה- די פי איי יתאים גם כשרזולוציית המסך מוגדלת (במקום טרו, אפשר גם להגדיר 1 או 2)
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    wnd.title("AB Group Predictor By Avotaynu and JewishDNA - written by Yehudit and Dr. Simcha Gershon Bohrer (ver. 29/1/2023)")
    wnd.minsize(200,200)
    wnd.geometry('820x680+0+0')
    # הגדרת האייקון לתוכנה במקרה שסוגרים בקובץ אחד כי צריך מיקום יחסי משתמש בפונקצייה שהובאה לעיל
    icon_path = resource_path("dna_icon.ico")
    wnd.iconbitmap(icon_path)
    # אם רוצים לעשות שהחלון הזה יהיה מעל כל החלונות שבמחשב. זה חשוב בעיקר כאשר רזולוציית המסך מוגדלת
    #wnd.attributes('-topmost',True)
    

    # הגדרת משתנה ששומר הגדרות כלליות לפונט שיהיה בשימוש
    font_buttons = tkinter.font.Font(wnd, family='narkisim', size=12, weight='bold')
    font_ = tkinter.font.Font(wnd, family='david', size=12)


    # כותרות לתוכנה
    #Label(wnd, text="Welcome to AB Group Predictor By Avotaynu and JewishDNA", font= "david 18 bold", wraplength=1000).pack()
    Label(wnd, text=Description, font= font_, wraplength=1000).pack()
    
    


    # תווית כותרת שאומרת למשתמש מה לעשות, והצבה שלה לתוך החלון
    Label(wnd, text=Instructions , font = "david 15 bold").pack()
    
    
    #---------------------------------------------

    # אזור נפרד להזנת סמנים
    input_heb = PanedWindow()

    Markers = ["DYS393, DYS390, DYS19, DYS391, DYS385, DYS426, DYS388, DYS439, DYS389i, DYS392, DYS389ii, DYS458, DYS459, DYS455, DYS454, \nDYS447, DYS437, DYS448, DYS449, DYS464, DYS460, Y-GATA-H4, YCAII, DYS456, DYS607, DYS576, DYS570, CDY, DYS442, DYS438"]
    example = ["14, 24, 14, 10, 17-18, 11, 12, 12, 12, 11, 29, 16, 09-09, 11, 11, 25, 14, 20, 33, 14-15-16-18, 11, 11, 19-23, 15, 12, 20, 19, 34-36, 11, 10"]
    example_dys464 = ["0, 0, 0, 0, 0-0, 0, 0, 0, 0, 0, 0, 0, 0-0, 0, 0, 0, 0, 0, 0, 14-15-16-18"]
    
    # הגדרת משתנה ששומר תיבת קלט טקסט שבה המשתמש מזין את תאריך הלידה הלועזי
    Label(input_heb, justify = 'left', text=Markers).grid(column=1, row=1)
    Label(input_heb, justify = 'left', text=f'EXAMPLE:          {str(example)[2:-2]}').grid(column=1, row=2)
    Label(input_heb, justify = 'left', text=f'EXAMPLE USE DYS464 ONLY:          {str(example_dys464)[2:-2]}').grid(column=1, row=3)
    input_heb.pack()
    
    Label(wnd, text="" , font = "david 5").pack()
    
    # פונקצייה לניהול האם יהיה קלט של אדם שני או לא
    def manager_person2_input():
        if person2_or_all.get() == 2:
            input_person_2.grid(column=0, row=2, columnspan=3)
        else:
            input_person_2.grid_forget()


    # איזור לכפתורי בחירה רדיו
    Rd_PW = PanedWindow()
    person2_or_all = IntVar()
    R1 = Radiobutton(Rd_PW, text=" Compare to AB groups     ", variable=person2_or_all, value=1, font = "david 13 bold", command=manager_person2_input).grid(column=0, row=1)
    R2 = Radiobutton(Rd_PW, text="Compare to 37 STR markers of another person", variable=person2_or_all, value=2, command=manager_person2_input).grid(column=1, row=1)
    # בדיקה האם להשתמש בקובץ נתונים אחר
    Check_file = IntVar()
    C1 = Checkbutton(Rd_PW, text = "Use an alternate AB groups file (csv)", variable = Check_file, onvalue = 1, offvalue = 0, width = 35).grid(column=2, row=1)
    person2_or_all.set(1)
    input_person_data = Entry(wnd, justify = 'left', width=110, font="david 12 bold")
    # איזור להכנסת נתונים של אדם שני. הגריד של זה נעשה באמצעות פונקצייה רק כאשר המשתמש מבקש להשוות בין שני אנשים ולא לקבוצות אבותינו
    input_person_2 = Entry(Rd_PW, justify = 'left', width=110, font="david 12 bold")
    Rd_PW.pack()

    
    # חלון להזנת סמני המשתמש
    input_person_data = Entry(wnd, justify = 'left', width=110, font="david 12 bold")
    input_person_data.pack()
    
    
    # אזור נפרד לכפתורים 
    Buttons1 = PanedWindow()

    Button(Buttons1, justify = 'right', text="Clear input box", command=clear_Entry).grid(column=3, row=0)
    
    # זה רק בשביל העיצוב
    Label(Buttons1, text="     ", justify = 'right', font = font_buttons).grid(column=2, row=0)
    
    Button(Buttons1, justify = 'right', text="paste from clipboard", command=paste).grid(column=1, row=0)
    
    # זה רק בשביל העיצוב
    Label(Buttons1, text="     ", justify = 'right', font = font_buttons).grid(column=4, row=0)
    
    Button(Buttons1, justify = 'right', text="insert_example", command=paste_example).grid(column=5, row=0)
    
    # זה רק בשביל העיצוב
    Label(Buttons1, text="     ", justify = 'right', font = font_buttons).grid(column=6, row=0)
    
    Button(Buttons1, justify = 'right', text="insert_example_DYS464", command=paste_example_dys464).grid(column=7, row=0)
    
    # אריזת האיזור הנפרד לתוך החלון הראשי
    Buttons1.pack()
    

    #--------------------------------------------------

    
    # אזור נפרד לכפתורים 
    Buttons2 = PanedWindow()
    
    # זה רק בשביל העיצוב
    Label(Buttons2, text="                                                     ", justify = 'right', font = font_buttons).grid(column=1, row=1)

    # הגדרת משתנה ששומר כפתור שכותרתו "חשב תאריך" והפעולה שהוא מבצע היא קריאה לפונקציית פרינט אאוטפוט
    nameButton= Button(Buttons2, text="Calculate data", font = "david 18 bold", width=12,command=main_result)
    # הצבה של משתנה כפתור "לחץ" לתוך החלון בצדו השמאלי של החלון ובמיקום ספציפי
    nameButton.grid(column=2, row=2)
    
    # זה רק בשביל העיצוב
    Label(Buttons2, text="                              ", justify = 'right', font = font_buttons).grid(column=3, row=1)

    # הגדרת משתנה ששומר כפתור שכותרתו "העתק את התוצאה ללוח" והפעולה שהוא מבצע היא קריאה לפונקציית קופי
    nameButton= Button(Buttons2, text="save results to file",width=15,command=save_txt_to_path)
    # הצבה של משתנה כפתור "לחץ" לתוך החלון בצדו השמאלי של החלון ובמיקום ספציפי
    nameButton.grid(column=4, row=2)

    # אריזת האיזור הנפרד לתוך החלון הראשי
    Buttons2.pack()


    #-----------------------------------------------
    # הגדרת משתנה ששומר תווית כותרת לתוצאה, והצבה שלה לתוך החלון
    #lbl=Label(wnd, text="התוצאות כדלהלן", justify = 'right', font = font_buttons).pack()
    #------------------------------------------------------

    # אזור נפרד לטקסט התוצאות
    output_text = PanedWindow()


    # ברי גלילה לאיזור התוצאות
    # גלילה למעלה ולמטה
    Y_scrollbar = Scrollbar(output_text, orient = 'vertical')
    Y_scrollbar.pack( side = RIGHT, fill = Y )

    # גלילה לימין ושמאל כרגע לא צריכה להיות בשימוש כי תיבת הטקסט עצמה לא מאפשרת חריגה של הטקסט לימין ושמאל
    X_scrollbar = Scrollbar(output_text, orient = 'horizontal')
    X_scrollbar.pack( side = BOTTOM, fill = X )

    # חלון טקסט להצגת התוצאות
    txt = Text(output_text, height=25, width=98, borderwidth=0, yscrollcommand = Y_scrollbar.set, xscrollcommand = X_scrollbar.set, font= "david 13")
    #txt.insert("end", f"\n\n חישוב הסיכויים באחוזים נעשה לפי טבלת שכיחות סימני השנה בספר \nע' מרצבך ו-ע' רביב, הלוח העברי הקבוע, הוצאת כרמל, ירושלים תשפא")

    # הגדרת העיצוב של הטקסט בתיבת הטקסט: שיהיה ממורכז
    txt.tag_configure("center", justify='center')
    txt.tag_add("center", 1.0, "end")   

    # סגירה של תיבת הטקסט לקריאה בלבד ואריזה לתוך החלון
    txt.configure(state="disabled")
    
    # חסימת כל תגובה לעכבר וכו של תיבת הטקסט
    #txt.bindtags(("txt", "wnd", "all"))
    
    # לחילופין, חסימת שתי תגובות ספציפיות לעכבר עבור תיבת הטקסט
    txt.bind("<Button>", lambda event: "break")
    txt.bind("<Motion>", lambda event: "break")
    

    # אריזת תיבת הטקסט
    txt.pack( side = LEFT, fill = BOTH )

    # הגדרת ברי הגלילה שפעולתם תתבצע על תיבת הטקסט
    Y_scrollbar.config( command = txt.yview )
    X_scrollbar.config( command = txt.xview )

    # אריזת האיזור הנפרד של טקסט התוצאות
    output_text.pack()
    
    #------------------------------------------------------

    # תווית כותרת שאומרת למשתמש מה לעשות, והצבה שלה לתוך החלון
    #Label(wnd, text=credit, font = "david 13 bold").pack()
    
    # הגדרת לולאה אינסופית שמפעילה את חלון טקטינר שיצרנו
    wnd.mainloop()

