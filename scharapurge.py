#Create a dataset that goes through every single character in the username
#Then check whether that character is a special character or not. If it is, remove it.
#Making a dataset and comparing every single character to everysingle special character would 
#increase time complexity drastically (n times m; where n is the total number of characters
#of every single string and m is the number of special characters in the database.)


#program to remove special characters and honorifics from names
#Procedure:
#1. Take in a csv or (convert an excel to csv if excel is given).
#2. Go through each column until you reach they key 'name'.
#3. Replace the name containing special characters and honorifics with the truncated name.
# ^To do the above step, truncate every character that isn't in a certain unicode range
#4. Voila


#REDO THIS PROGRAM
#CREATE A DATABSE OF SPECIAL CHARACTERS AND COMPARE STRING ELEMENTS TO THAT DATBASE

#dataframe management
import pandas as pd
import magic 
import csv
# import unicodedata
# import Unicode

def getFile():
    file_path = ''
    fType = ''
    # Data files\Non_Latin_kanji.csv
    # Data files\Latin_Kanji_names.csv

    try:
        file_path = input("Enter file: ")
        #check if file exists (This method actually check file type, but the file needs to exist for it to check type)
        fType = magic.from_file(file_path)
    except Exception as e:
        print(e)
        return
    print("Correct file type")
    return file_path

def is_devanagari_dependent_vowel(char):
    # Unicode range for Devanagari dependent vowel signs
    return '\u093A' <= char <= '\u094F' or char in [
        '\u0900',
        '\u0901',
        '\u0902',
        '\u0903',
        '\u0955',
        '\u0956',
        '\u0957',
        '\u0962',
        '\u0963',
        '\u0964',
        '\u0965',
        '\u0970',
        '\u0971',
    ]

def openFile(file_path):
    # print("Opening reader...")
    with open(file_path, newline='', encoding="utf-8") as file1:
        # print("Reader opened")
        reader = csv.DictReader(file1)

        #iterates through each row
        
        for doc in reader:
            print(doc)
            # print(doc["Username"])
            # deliminator = ""
            remadeString = "".join(ch for ch in doc["Username"] if ch.isalnum() or is_devanagari_dependent_vowel(ch))
            #we join ch to remadeString if ch(an iterable btw) is alpha numerical

            print(remadeString)
            


def execute():
    #why check file type when you check if file exists. 
    # OR you could check file type during in the execute function
    file_path = getFile()
    if file_path == None:
        return
    
    # print("Filel shall be opened")
    openFile(file_path)




def main():
    execute()

main()