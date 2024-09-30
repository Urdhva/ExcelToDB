#read complete data from collection, store it all in a csv file
#clean up the usernames, then delete collection, and rewrite the collection

import magic
import csv
from pymongo import MongoClient
import pandas as pd

def isSChara(ch):
    return False if ('\u0000' <= ch <= '\u002F'
        or '\u005B' <= ch <= '\u0060'
        or '\u007B' <= ch <= '\u007E' 
        or '\u00A0' <= ch <= '\u00BE') else True

def purgeChara(temp):
    remadeString = "".join(ch for ch in temp if isSChara(ch))
    print(remadeString)
    return remadeString

#take in mongoDB as a dataframe and convert it into a csv file
#then follow the steps written on line 1
def main():
    client = MongoClient("localhost", 27017)
    db = client.facebook_users
    colec = db.users

    #check if collection is empty
    try:
        cursor = colec.find()
        doc_1 = cursor[1]
    except:
        print("no documents present")
        return
    
    # for doc in colec:
    #     print(doc)
    
    for document in colec.find():
        if "Username" in document:
            temp = document["Username"]
            temp = purgeChara(temp)
            colec.update_one({"_id": document["_id"]}, {"$set": {"Username": temp}})
        else:
            pass
            # print("No username attribute found in the document.")

main()