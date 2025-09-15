inputData.py is a command line interface that allows a user to import CSV or Excel data into a MongoDB collection, or allows the user to delete all data from a collection. Works as a backend for web-scrapers that generate a large amount of tabular data.

cleanName.py performs data cleaning on usernames stored in a MongoDB collection. It processes each document by removing honorifics and special characters from the "username" field. While this program is hardcoded to clean a database named "Facebook" and a collection named "users", it can be modified to accept any database and collection.  
