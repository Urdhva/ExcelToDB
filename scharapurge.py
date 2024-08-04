#program to remove special characters and honorifics from names
#Procedure:
#1. Take in a csv or (convert an excel to csv if excel is given).
#2. Go through each column until you reach they key 'name'.
#3. Replace the name containing special characters and honorifics with the truncated name.
#4. Voila

#dataframe management
import pandas as pd
import magic 

def getFile():
    file = ''
    fType = ''

    try:
        file = input("Enter file: ")
        #check if file exists (This method actually check file type, but the file needs to exist for it to check type)
        fType = magic.from_file(file)
    except Exception as e:
        print(e)
        return

    return file

def openFile(file):
    pass

def execute():
    #why check file type when you check if file exists. 
    # OR you could check file type during in the execute function
    file = getFile()
    if file == None:
        return
    
    openFile(file)


def main():
    execute()

main()