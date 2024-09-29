#File that takes in csv or excel data and adds the data to a collection

import pandas as pd
from pymongo import MongoClient
import magic 
import csv

def toColec(file):
    client = MongoClient("localhost", 27017)
    db = client.facebook_users
    colec = db.users

    with open(file, newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)

        #inserts every row into our collection
        for doc in reader:
            colec.insert_one(doc)

def getFile():
    file = ''
    file_type = ''

    while True:
        try:
            file = input("Enter file: ")
            file_type = magic.from_file(file)
            #method from_file returnsf file type
            #and checks if file exists
        except Exception as e:
            print(e)

        return file, file_type

def enteringData():
    file, file_type = getFile()
    wordBreak = file.split(".")
    if wordBreak[-1] == "xlsx":
        df = pd.read_excel(file)      #pandas read excel
        file = 'dataInCSV'
        df.to_csv(file, index=False)       #pandas to csv
    elif wordBreak[-1] == "csv":
        pass
    else:
        print("Wrong file type.Exiting...")
        return
    
    toColec(file)


def deleteData():
    client = MongoClient("localhost", 27017)
    db = client.facebook_users
    colec = db.users
    
    result = colec.delete_many({})

    if result.deleted_count > 0:
        print(f"{result.deleted_count} documents deleted successfull.")
    else:
        print("No documents were deleted (collection might be empty).")

    client.close() 

def main():
    choice = int(input("Entering Data - 1\nDeleting Data - 2\n-> "))

    if choice == 1:
        enteringData()
    elif choice == 2:
        deleteData()
    else:
        print("Wrong Input. Exiting...")

main()