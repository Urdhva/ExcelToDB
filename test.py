#THIS FILE HAS NOTHING TO DO WITH THE PROGRAM
#simply a ground for testing random features

# Sequence of Operation
# ->open the excel file in python
# ->open the mongoDB database in python
# ->copy excel file to database in python
# ->parse all names with a facebook account
# ->store those parsed names in a list
# ->check if each member of that list is present in the database. Delete member if present. Do nothing if member is not present. 
# (Say the member is not present-> you simple skip the list ele.
# Say the member is present, so if present, delete element)
# ->Use final list and add those names to the database in mongoDB

from pymongo import MongoClient
import pprint       #stands for pretty print

client = MongoClient("localhost", 27017)

db = client.facebook_users      #imports the database

users = db.users        #imports the collection

# user_id = users.insert_one({"usrnm": "Carter", "age": 55}).inserted_id        
# print(user_id)

# print(db.list_collection_names())       #we are calling methods of 'db' aka database
print(users.find_one({"usrnm": "Gacha"}))                 #we are calling methods of 'users' aka collection

# for user in users.find({"age": 55}):
#     print(user)

# print(users.count_documents())