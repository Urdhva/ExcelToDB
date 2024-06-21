import pandas as pd     #file database management
from pymongo import MongoClient
import openpyxl as pyxl

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

            fAccount.append(username[0])        #add username to accounts list
            fDate.append(date)
            fActiv.append(activity)
            fDist.append(district)
            fOrg.append(org)


    for org in fOrg:          #prints usernames from the parsed links
        print(org)

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

    
def main():     #action happens here
    dataLists = findAccounts()          #this var is a tuple here because we are returning a tuple of lists
    accounts = dataLists[0]
    dates = dataLists[1]
    activs = dataLists[2]
    dists = dataLists[3]
    orgs = dataLists[4]

    addToDB(accounts, dates, activs, dists, orgs)



deleteData()
main()


#read and write an excel sheet at the same time:
# open: parameter: w+
    