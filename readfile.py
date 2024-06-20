import pandas as pd     #file database management
from pymongo import MongoClient

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

def findAccounts():             #goes through the excel sheet for facebook accounts
    EXCEL_FILE = 'C:\\Users\\Urdhv\\Desktop\\Python programs\\FileReading\\Sample_data_file.xlsx'

    df = pd.read_excel(EXCEL_FILE)  #df is a temporary data frame in python made to store our excel sheet's data

    links = df['Link']      #list of the elements in the link collumn
    accounts = []

    for link in links:      #go through every link one by one
        link_parts = link.split(sep="/")        #creates smaller words between the slashes
        if link_parts[2] == "www.facebook.com":     #checks if a facebook link is present
            username = link_parts[3].split(sep="?")
            
            if username[0] == "permalink.php":      #remove this string from being considered
                continue

            accounts.append(username[0])        #add username to accounts list

    # for account in accounts:          #prints usernames from the parsed links
    #     print(account)

    return accounts

def addToDB(accounts):          #add accounts to the database
    client = MongoClient("localhost", 27017)

    db = client.facebook_users          #import database

    users = db.users            #imports collection
    #users here is a COLLECTOIN! NOT A LIST

    for account in accounts:    #iterates through the list of usernames
        if users.find_one({"usrnm": account}) == None:      #check if you find an account with the same name
            # print("none found")
            users.insert_one({"usrnm": account})            #add username to database if not present
        else:
            print("User found, skipped")

    
def main():     #action happens here
    accounts = findAccounts()
    addToDB(accounts)


main()
# deleteData()
    