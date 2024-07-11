# To start and stop your mognoDB server: Windows + R; type "services.msc" and look for MongoDB server

# file dataframe management
import pandas as pd     
from pymongo import MongoClient
# import pprint
# used for file type checking - doesn't work on excel files for some reason
import magic            
import csv
#the program also uses openpyxl, make sure you have the module installed

# deletes every document in the database
def deleteData():               
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


def getUserFile():
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
        if wordBreak[-1] == "xlsx" or wordBreak[-1] == "csv":
            print("File accepted")
            break
        else:
            print("Invalid file or file type\nFile type------>", file_type)

    return file


def toCSV(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)      #pandas read excel

    csv_file_path = 'dataInCSV'
    
    df.to_csv(csv_file_path, index=False)       #pandas to csv

    return csv_file_path

# for excel files
# Will use this function
def store___mongo___xcel(CSV_PATH, EXCEL_FILE, website):
    #for mongodatabase
    client = MongoClient("localhost", 27017)
    db = client.facebook_users
    users = db.users

    #for excel sheet
    df = pd.read_excel(EXCEL_FILE)
    df = df.assign(Username='')
    row_to_modify = 0
    col_to_modify = 'Username'   

    # utf8 to accept unicode
    with open(CSV_PATH, newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)

        for doc in reader:
            # for inserting into our collection
            isLink = False            
            for value in doc.values():
                link_parts = value.split("/")        

                try:    #try statement here incase our value isn't split into a bunch of parts (for every cell except link)
                    if link_parts[2] == website:
                        isLink = True            
                except:
                    continue
                
                # is link checks if the row has the required link
                if isLink == True:
                    username = link_parts[3].split("?")
                    if username[0] == "permalink.php":
                        isLink = False
                    else:
                        isLink = True
                        df.loc[row_to_modify, col_to_modify] = username[0]
            
            if isLink == True:
                # value here is all the values in 
                users.insert_one(doc)
                df.to_excel(EXCEL_FILE, index=False)

            row_to_modify += 1

    print("")
    main()

# for CSV files only
# Probably will not use this function    
def store__mongo(CSV_PATH, website):
    #for mongodatabase
    client = MongoClient("localhost", 27017)
    db = client.facebook_users
    users = db.users

    with open(CSV_PATH, newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)

        for doc in reader:
            #for inserting into our collection
            isLink = False            
            for value in doc.values():
                link_parts = value.split("/")        

                try:    #try statement here incase our value isn't split into a bunch of parts (for every cell except link)
                    if link_parts[2] == website:
                        isLink = True            
                except:
                    continue

                if isLink == True:
                    username = link_parts[3].split("?")
                    if username[0] == "permalink.php":
                        isLink = False
                    else:
                        isLink = True
            
            if isLink == True:                   
                users.insert_one(doc)

    print("")
    main()


def simple_copy_to_DB(CSV_PATH):
    #for mongodatabase
    client = MongoClient("localhost", 27017)
    db = client.facebook_users
    users = db.users

    with open(CSV_PATH, newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)

        for doc in reader:            
            users.insert_one(doc)

    print("")
    main()


def getSite():
    website = "www.facebook.com"
    while True:
        while True:
            try:
                choice = int(input("Enter 1 to scan for default website (www.facebook.com).\nEnter 2 to scan for custom website.\n->"))
            except:
                print("Invalid input, only numbers are accepted")
            else:
                break
        if choice == 1:
            return website
        elif choice == 2: 
            website = input("Enter website name: ")
            return website
        else:
            print("Invalid input\n")


# read data from the database and put it back into an excel file
def createExcel():
    client = MongoClient("localhost", 27017)
    db = client.facebook_users
    collec = db.users  

    # incase database is empty
    try:
        cursor = collec.find()
        doc_1 = cursor[1]
    except:
        print("no documents present")
        return
    
    col_names = list(doc_1.keys())
    # removing the _id_ col header
    col_names.pop(0)            
    
    # col_names are now columns
    df = pd.DataFrame(columns=col_names)

    for doc in cursor:
        doc = dict(doc)     # force doc to become a dictionary object
        doc.pop("_id")      # now its dict object, thus pop will always work
        
        df = df._append(doc, ignore_index=True)

    df.to_excel("temp_excel.xlsx", index=False)
        

#action happens here
def execute():     
    # file = 'C:\\Users\\Urdhv\\Desktop\\Python programs\\FileReading - master\\Sample_data_file.xlsx'
    file = getUserFile()
    website = getSite()

    wordBreak = file.split(".")
    if wordBreak[-1] == "xlsx":
        csv_path = toCSV(file)
        store___mongo___xcel(csv_path, file, website)
    elif wordBreak[-1] == "csv":
        store__mongo(file, website)

def execute2():
    file = getUserFile()
    csv_file = toCSV(file)

    simple_copy_to_DB(csv_file)


def main():
    choice = int(input("Insert sheet and add data: 1\nDelete Data: 2\nSimply copy excel data to a DB: 3\nExit Program: 4\n-> "))

    if choice == 1:
        execute()
    elif choice == 2:
        deleteData()
    elif choice == 3:
        execute2()
    elif choice == 4:
        print("Exiting program...")
    else:
        print("Invalid input")


main()
#test
# createExcel()  