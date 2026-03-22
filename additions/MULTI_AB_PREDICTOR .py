#!/usr/bin/env python
# coding: utf-8

# In[1]:


# סקריפט לחישוב קבוצת אבותינו הכי קרובה של אנשים רבים יחד מתוך קובץ פייתון


# יבוא פנדס
import pandas as pd

# משתנים כלליים

# משתנה שאין לשנותו, שקובע שאנו רוצים לקבל רק תוצאה אחת של קבוצת אבותינו אחת כי אנחנו רוצים רק את הקבוצה הקרובה ביותר
NUM_MIN=1

# משתנה שאין לשנותו עבור פונקציית ההדפסה
MAX_DIST=100

# משתנה האם להוסיף מרחק במקרה שאין התאמה במספר האללים של סמן מסויים. כרגע אפס.
MISMATCH_LIVES_DIST=0

# משתנה גלובלי עבור שמירת שם של קבוצת אבותינו הכי קרובה. משתנה זה משנה את ערכו בכל ריצה של פונקציית פרינט להלן
CLOSEST_AB = "CLOSEST_AB"

# פונקצייה לקבלת נתונים מתוך קבצי אקסל
def get_data(path):

    # Load the xlsx file
    excel_data = pd.read_excel(path, engine='openpyxl')

    # Read the values of the file in the dataframe
    data = pd.DataFrame(excel_data)

    return data

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
        str_dist+=MISMATCH_LIVES_DIST
    else:
        for i in range(len(arr_person_item)):
            str_dist+=distance(int(arr_person_item[i]),int(arr_data_item[i]))
    return str_dist


# חישוב המרחקים עבור שורה שלמה של סמנים באמצעות הפונקציות שלעיל אבל למעשה זה נעשה לפי טורים שלמים של סמנים 
def dist_of_rows(person_row,data_row):
    row_dist=0
    
    for item in range(2,len(person_row)):
        person_item=parse_to_int_if_possible(person_row[item])
        data_item=parse_to_int_if_possible(data_row[item])
              
        if not person_item:
            continue;
        
        if (type(person_item)==int and type(data_item)==int):
            row_dist+=distance(person_item,data_item)
            
        elif (type(person_item) == str and type(data_item) == str):
            row_dist+=dist_of_str(person_item,data_item)
            
        else:
            row_dist+=MISMATCH_LIVES_DIST
            
    return row_dist


# חישוב המרחקים עבור כל השורות של קבוצות אבותינו באמצעות הפונקציות שהוגדרו לעיל
def get_distances(row,data):
    # location=Current_location()
    distances=[]
    for i in range(data.shape[0]):
        distances.append(dist_of_rows(row,data.iloc[i]))
    return distances

# פונקצייה לחישוב קבוצת אבותינו הכי קרובה
def print_k_min_match_rows(dist,k,whole_data):
    for i in range(k):
        match_row=min(dist)
        ix=dist.index(match_row)
        #print("The ",i+1," match model is:")
        #print("AB Group: ",whole_data.iloc[ix].iloc[0])
        #print("Description: ",whole_data.iloc[ix].iloc[1])
        #print("The distance is:",match_row)
        #print("")
        # הצהרה על משתנה גלובלי
        global CLOSEST_AB
        # שמירת המשתנה של קבוצת אבותינו הכי קרובה בשם הקבוצה הקרובה אם היא לא גדולה ממרחק של 10 אחרת יש לשמור שזה רחוק מידי
        CLOSEST_AB = whole_data.iloc[ix].iloc[0] if match_row <= 10 else "far"
        
        dist[ix]+=MAX_DIST
        
        
# main
if __name__ == '__main__':
    
    # קבלת קבצי הנתונים של הנבדקים ושל קבוצות אבותינו
    # כל אחד מהקבצים חייב להכיל 32 עמודות: 30 עמודות עבור 37 סמנים ועוד שני עמודות משמאל
    # בקובץ פרסון שני העמודות הללו חייבות להיות קרויות
    # 1: kit, 2: AB predicted
    whole_data = get_data('data37+A.xlsx')
    person_data=get_data('person.xlsx')
    
    # זה כרגע לא עובד ורק משבש, אבל בעקרון נועד שאם בקובץ פרסון אין עמודה עבור חיזוי קבוצת אבותינו אז יש להוסיף עמודה כזו
    #if 'AB predicted' not in person_data.columns:
    #    person_data.insert(-1, 'AB predicted', pd.Series([None] * (len(person_data) -1)))
        
    
    # עבור כל אדם היינו כל שורה בקובץ פרסון יש לחשב את הקבוצה הכי קרובה 
    for person in range(len(person_data)):
    
        dist=get_distances(person_data.iloc[person],whole_data)

        print_k_min_match_rows(dist.copy(),NUM_MIN,whole_data)

        # יש להוסיף את קבוצת אבותינו הקרובה ביותר לעמודה המתאימה בשורה המדוברת 
        person_data.at[person, 'AB predicted'] = CLOSEST_AB
        

# הצגת התוצאות
person_data

# שמירת התוצאות לקובץ        
#person_data.to_excel('person_plus_AB_predicted.xlsx')        

