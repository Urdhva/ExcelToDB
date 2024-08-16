#program to remove special characters and honorifics from names
#Procedure:
#1. Take in a csv or (convert an excel to csv if excel is given).
#2. Go through each column until you reach they key 'name'.
#3. Replace the name containing special characters and honorifics with the truncated name.
# ^To do the above step, truncate every character that isn't in a certain unicode range
#4. Voila

#dataframe management
import pandas as pd
import magic 
import csv

def getFile():
    file_path = ''
    fType = ''

    try:
        file_path = input("Enter file: ")
        #check if file exists (This method actually check file type, but the file needs to exist for it to check type)
        fType = magic.from_file(file_path)
    except Exception as e:
        print(e)
        return
    print("Correct file type")
    return file_path


def openFile(file_path):
    with open(file_path, newline='', encoding="utf8") as file1:
        reader = csv.DictReader(file1)

        #iterates through each row
        
        for doc in reader:
            # print(doc["Username"])
            deliminator = ""
            remadeString = "".join(ch for ch in doc["Username"] if ch.isalnum())
            #we join ch to remadeString if ch(an iterable btw) is alpha numerical

            print(remadeString)
            
                
        


def execute():
    #why check file type when you check if file exists. 
    # OR you could check file type during in the execute function
    file_path = getFile()
    if file_path == None:
        return
    
    openFile(file_path)


def main():
    execute()

main()