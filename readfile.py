# To start and stop your mognoDB server: Windows + R; type "services.msc" and look for MongoDB server

import pandas as pd     #file dataframe management
from pymongo import MongoClient
# import pymongo
import magic            #used for file type checking - doesn't work on excel files for some reason
import csv

def deleteData():               #deletes every document in the database
    client = MongoClient("localhost", 27017)

    db = client.facebook_users          #import database

    users = db.users

    result = users.delete_many({})

    if result.deleted_count > 0:
        print(f"{result.deleted_count} documents deleted successfully!")
    else:
        print("No documents were deleted (collection might be empty).")

    # Close the connection (optional, good practice)
    client.close()

    print('')
    main()


def getExcelFile():
    #try except statement won't work here because it's used to catch run-time errors
    #we won't reach our run time error for rinputing the wrong file until much late

    file = ''
    file_type = ''

    while True:
        try:
            file = input("Enter an excel file: ")
            file_type = magic.from_file(file)       
            #the method 'from_file' returns the file type, but I'm using it here to make sure the file entered exists
        except:
            print("-----file doesn't exist-------")
        
        wordBreak = file.split(".")
        if wordBreak[-1] == "xlsx":
            print("Correct file type")
            break
        else:
            print("Invalid file or file type\nFile type------>", file_type)

    return file


def toCSV(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)      #pandas read excel

    csv_file_path = 'dataInCSV'
    
    df.to_csv(csv_file_path, index=False)       #pandas to csv

    return csv_file_path


def store___Mongo(CSV_PATH):
    client = MongoClient("localhost", 27017)
    db = client.facebook_users
    users = db.users


    with open(CSV_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for doc in reader:
            forCollec = False       #for inserting into our collection
            for value in doc.values():
                link_parts = value.split("/")       #split the link into parts 

                try:    #try statement here incase our value isn't split into a bunch of parts (for every cell except link)
                    if link_parts[2] == "www.facebook.com":
                        forCollec = True        #try putting this in a 'finally' statement
                except:
                    continue

                if forCollec == True:
                    username = link_parts[3].split("?")
                    if username[0] == "permalink.php":
                        forCollec = False
                    else:
                        forCollec = True
            
            if forCollec == True:
                users.insert_one(doc)
                    

def execute():     #action happens here
    file = 'C:\\Users\\Urdhv\\Desktop\\Python programs\\FileReading - master\\Sample_data_file.xlsx'
    csv_path = toCSV(file)
    store___Mongo(csv_path)


def main():
    choice = int(input("Insert sheet and add data: 1\nDelete Data: 2\nExit Program: 3\n-> "))

    if choice == 1:
        execute()
    elif choice == 2:
        deleteData()
    elif choice == 3:
        print("Exiting program...")
    else:
        print("Invalid input")


# main()
execute()

#read and write an excel sheet at the same time:
# open: parameter: w+
    