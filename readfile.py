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


def findAccounts(EXCEL_FILE):             #goes through the excel sheet for facebook accounts
    df = pd.read_excel(EXCEL_FILE)  #df is a temporary data frame in python made to store our excel sheet's data
    df = df.assign(Username='')     #adds an empty column to the excel sheet if not present by the same name

    row_to_modify = 0
    col_to_modify = 'Username'


    links = df['Link']          #list of the elements in the link collumn
    dates = df['Date of Entry']
    activities = df['Type of Activity']
    districts = df['District']
    orgs = df['Type of Activist (Individual/Organization)']
    
    
    fAccount = []               #list we are going to send to the other function. 
    fDate = []                  #list of dates we are going to send to the main function.
    fActiv = []             #list of activites "        "
    fDist = []              #list of districts "        "
    fOrg = []              #list of activists "        "

    for link, date, activity, district, org in zip(links, dates, activities, districts, orgs):      #go through every link one by one
        link_parts = link.split(sep="/")        #creates smaller words between the slashes
        if link_parts[2] == "www.facebook.com":     #checks if a facebook link is present
            username = link_parts[3].split(sep="?")
            
            if username[0] == "permalink.php":      #remove this string from being considered
                continue
            
            # cellM = df.loc[row_to_modify, col_to_modify]        #find the cell we wanna modify
            df.loc[row_to_modify, col_to_modify] = username[0]

            fAccount.append(username[0])        #add username to accounts list
            fDate.append(date)
            fActiv.append(activity)
            fDist.append(district)
            fOrg.append(org)
        row_to_modify += 1


    for district in fDist:          #prints usernames from the parsed links
        print(district)

    df = df.to_excel(EXCEL_FILE, index=False)
    return fAccount, fDate, fActiv, fDist, fOrg

def addToDB(accounts, dates, activs, dists, orgs):          #add accounts to the database
    client = MongoClient("localhost", 27017)

    db = client.facebook_users          #import database

    users = db.users            #imports collection
    #users here is a COLLECTOIN! NOT A LIST

    for account, date, activ, dist, org in zip(accounts, dates, activs, dists, orgs):    #iterates through the list of usernames
        if users.find_one({"usrnm": account}) == None:      #check if you find an account with the same name
            # print("none found")
            users.insert_one({"DoE": date, "usrnm": account, "Activity": activ, "District": dist, "Organization": org})            #add username to database if not present
        else:
            print("User found, skipped")


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
                    

                
                

def storeInMongo(CSV_PATH):

        # Replace with your connection details
    client = MongoClient("mongodb://localhost:27017/")
    db = client.facebook_users
    users = db.users

    # Open the CSV file
    with open(CSV_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        iter = 0
    # Insert each row as a document in the collection
        for document_dict in reader:         #document is a dictionary. You need to find a way to parse data from a dictionary
            temp_dict = document_dict
            forFacebook = False
            for value in document_dict.values():    #RETURNS ALL KEYS AND VALUES ONE BY ONE (LINK IS A SINGLE KEY IN THE DICTIONARY)
                                                                            #we are technically wasting resources parsing every key, but that's fine for now
                link_parts = value.split("/")            #NOT REALLY, IF WE FIND A STRING WITH LINK, WE PARSE THAT STRING
                                                #THE ADVANTAGE OF THIS BEING WE DON'T NEED TO LOOK FOR A KEY CALLED LINK
                                                #THUS EVEN IF THERE ISN'T A COLUMN CALLED LINK, WE CAN PARSE THE FILE

            
                try:        #if there are no parts of the string (most values won't have parts)
                    if link_parts[2] == "www.facebook.com":      #there should be 15
                        pass
                        
                except:
                    continue

                username = link_parts[3].split(sep="?")
            
                if username[0] == "permalink.php":      #remove this string from being considered
                    continue

                for key in document_dict.keys():
                    print(key)
                users.insert_one(temp_dict)

            iter += 1
            print("Run", iter,"times")



def execute():     #action happens here
    file = 'C:\\Users\\Urdhv\\Desktop\\Python programs\\FileReading - master\\Sample_data_file.xlsx'
    # # file = getExcelFile()
    # # dataLists = findAccounts(file)          #this var is a tuple here because we are returning a tuple of lists
    # # accounts = dataLists[0]
    # # dates = dataLists[1]
    # # activs = dataLists[2]
    # # dists = dataLists[3]
    # # orgs = dataLists[4]

    # addToDB(accounts, dates, activs, dists, orgs)

    # print('')
    # main()

    # excel_file = getExcelFile()
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
    