#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# חוץ מזה לא ברור למה הוא לא מדפיס את מיסמטש כשיש מיסמטש
# כל העניין של מיסמטש לא תמיד עובד. לדוגמא אם הוספתי עוד אלל ל 464 הוא לא הוסיף 3 אלא 2. ולגבי 14-20 הוא הוסיף רק 1 ואולי חוץ מזה אם מחקתי אלל אחד ממקום שיש בו שניים הוא לא הוסיף 3


'''Welcome to AB Group Predictor

you need to click on: "Run cell" (Ctrl + Enter) to run the code.
This will open a box where the user's STR markers need to be entered.
Enter the markers and press enter.
Scroll to the bottom of the page to see the results.


credit:
The code of this software was written by Yehudit Bohrer, and improved by Dr. Simcha Gershon Bohrer.
Any use of this software will be made non-profit, and with appropriate credit.
All the data on AB Groups and their modals were taken from the published data on the "Jewish DNA" website at the following address:
https://jewishdna.net/ModalsAB.html

What does the software do?
This software receives an input of the first 37 STR markers (according to their order in FTDNA format) , and compares it against the first 37 STR markers in the AB Groups STR model.

The result obtained: 5 AB Groups to which the person is most compatible.
Usually, the person fits the first group in the list of results, but sometimes he fits the second or third match, etc.
For example: if the person matches the first result with a difference of 5 and the second result with a difference of 20, it is clear that he belongs to the first group. However, if the person matches the first result with a difference of 5 and the second result with a difference of 6, the person may belong to the second group.
This software gives excellent results, but still the results should be treated with a little suspicion.

Additional instructions, and additional details:
You can enter more than 37 markers, but the result will only refer to the first 37 markers.
You can enter less than 37 markers, but the match will be less good.
For example: if you only use the first 12 markers, you can use the software as usual.
But, if you want to use only markers 13-24, you must put a zero (0) in place of each of the first 12 markers for this software to calculate correctly.

The markers must be inserted in FTDNA format from left to right, with each marker separated from the marker before it by a tab. For example: 12 23 14 10/
Markers that have several alleles (such as the DYS464 marker which usually contains 4 alleles), each allele should be separated from the next allele by a middle dash. For example: 12-14-16-17.

In the event that the subject has a marker that contains an unusual number of alleles (such as 6 alleles for the DYS464 marker), or a marker that contains an incomplete number (such as 12.3), this marker will not be calculated at all in the measurement of matching to any group. Instead, the software will go away this person from the model arbitrarily, in three steps.
In the event that the subject has a deletion of a certain marker [such as having nool or 0] the comparison will not refer to this marker.

In the list of results, the groups that have Ashkenazim are marked as follows:

(A) = Ashkenazi group
(A+S) = a group that has Ashkenazim and Sephardim

Therefore, if you enter the results of a completely Ashkenazi person, and get a first match to a group that does not contain Ashkenazim, this person probably belongs to the second match and not to the first match.'''







# pandas for read_csv
import pandas as pd

###################################################################

# csv AB-DATA from google drive
url = "https://drive.google.com/file/d/1oe1uKeDMTd3_x-EBRgdXrusolYoI4Q7j/view?usp=sharing"
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]

###################################################################3

# global variables

# number of groops to print minimal distance
####NAM_MIN = len(whole_data) 

# for use def print_k (possible number > 100)
MAX_DIST = 100

# to send away person from modal wen namber of alels in singel str marker is mismatch 
MISMATCH_MARKER_DIST = 3

################################################################

# read_csv from computer OR from google drive
def get_data(path):
    # Load the csv file
    csv_data = pd.read_csv(path)
    # Read the values of the file in the dataframe
    data = pd.DataFrame(csv_data)
    return data

#########################################################
    
# calculations of distances from AB-MODALS (=data37)

# try to change to int
def parse_to_int_if_possible(unknoun_type):
    try:
        int_type=int(unknoun_type)
        return int_type
    except:
        return unknoun_type

# calculate distance for singel marker
def distance(num1,num2):
    return(abs(num1-num2))

# calculate distance for str (example: 12-14-16-17)
def dist_of_str(person_item,data_item):
    str_dist=0
    arr_person_item=person_item.split('-')
    arr_data_item = data_item.split('-')
    if not(len(arr_person_item)==len(arr_data_item)):
        str_dist+=MISMATCH_MARKER_DIST
#        print: ("MISMATCH_MARKER_DIST for:",str_dist)
    else:
        for i in range(len(arr_person_item)):
            str_dist+=distance(int(arr_person_item[i]),int(arr_data_item[i]))
    return str_dist

# calculate summing distance for complete row in data37
def dist_of_rows(person_row,data_row):
    row_dist=0
    
    for item in range(2,len(person_row)):
        # location.set_column(j)
        person_item=parse_to_int_if_possible(person_row[item])
        data_item=parse_to_int_if_possible(data_row[item])
        
        # If the item is deleted or not tested - calculate nothing         
        if person_item in [0,'0',"0-0","0-0-0-0","0-0-0-0-0","0-0-0-0-0-0","0-0-0-0-0-0-0","null","NULL"]:
            # report_deleted_item(item)
            continue;
        
        if (type(person_item)==int and type(data_item)==int):
            row_dist+=distance(person_item,data_item)
            
        elif (type(person_item) == str and type(data_item) == str):
            row_dist+=dist_of_str(person_item,data_item)
            
        else:
            row_dist+=MISMATCH_MARKER_DIST
#            print: ("MISMATCH_MARKER_DIST for:",row_dist)
            
    return row_dist

# def calculate distances for complete rows in data37 through the functions be defined aforementioned
def get_distances(person,whole):
    # location=Current_location()
    distances=[]
    for i in range(whole.shape[0]):
        distances.append(dist_of_rows(person,whole.iloc[i]))
    return distances

##################################################################################

# def print calculations of distances from AB-MODALS (=data37) - manipulate solution

def print_min_match_rows(dist,whole_data,person_data):
    print(f'FOR STR MARKERS\n {person_data[2:]}\n')
    for i in range(len(whole_data)):
        match_row=min(dist)
        ix=dist.index(match_row)
        print("")
        print("")
        print("The ",i+1," match model is:")
        print("AB Group: ",whole_data.iloc[ix].iloc[0])
        print("Haplogroup (SNP): ",whole_data.iloc[ix].iloc[1])
        print("The distance is:",match_row)
        dist[ix]+=MAX_DIST

################################################################################

# main

if __name__ == '__main__':

# get AB-DATA locality or from web 
    try:
        whole_data = get_data('data37+A.csv')
    except:
        whole_data = get_data(path)

# get person data (37 markers) from input    
    person = input("Please enter STR data in FTDNA format (separated by tab, for example: 13	24	13	10	17-18	11):\n\n") 
    if "\t" in person:
        arr_person = person.split('\t')
    elif "\t" not in person:
        arr_person = person.split(" ")
# Added 2 positions to Person, so that Person's item is equal to Data's item    
    pm = ["person","markers"]
    person_data = pm + arr_person[0:30]
    
    if person_data[2] != "":
        # calculate distances for complete rows in data37
        dist=get_distances(person_data,whole_data)

        # print calculations of minimal distances from AB-MODALS
        print_min_match_rows(dist.copy(),whole_data,person_data)
    

