import pandas as pd
from pymongo import MongoClient
import csv
import magic

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
    
    #find the column we want to match
    query = {"Username"}

    update = {
        "$set": {"Username": "The World"}
    }

    result = collec.update_many(query, update)

    print(f"Updated {result.matched_count} documents.")


def main():
    createExcel()


main()


#another way I could solve this is using a temporary csv file
