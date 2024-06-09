import pandas as pd
import tempfile
import csv


def test():             #use this for trying out things
    # phrase = 'https://music.youtube.com/watch?v=fYBQJfPBmRg&list=RDAMVMRWFW1OSlMkM'
    # words = phrase.split(sep='/')
    # print(words)

    with tempfile.TemporaryFile() as fp:
        fp.write(b'Hello World')
        fp.seek(0)
        print(fp.read())


def writeToEXCEL():     #use a loop to go through every cell, check if the link has music.com, add creater to creators.csv
    pass


def writeCSVdefault(df):     #writes data not present into a CSV file
    with open('C:\\Users\\Urdhv\\Desktop\\Python programs\\FileReading\\creators.csv', 'a', newline='') as csv_file:
        write = csv.writer(csv_file)        #creates a writer object that goes through the CSV file line by line
    
        links = df['Link']
        usernames = df['Username']

        for link, username in zip(links, usernames):    #separate each cell in both columns
            link_bd = link.split(sep='/')               #link_breakdown: contains parts of a link separated by '/'
            if link_bd[2] == 'music.youtube.com':
                write.writerow([username])


# def writeCSVpandas(df_excel):
#     # df_csv = pd.read_csv('C:\\Users\\Urdhv\\Desktop\\Python programs\\FileReading\\creators.csv')   #create a dataframe
#     #remember, we create a dataframe when we want to edit that dataframe.
#     #we use to_csv to add to a csv file


#     links = df_excel['Link']
#     usernames = df_excel['Username']

#     for link, username in zip(links, usernames):
#         link_bd = link.split(sep='/')
#         if link_bd[2] == 'music.youtube.com':
            

def erase_CSV():        #truncates all data in a csv file
    file = open('C:\\Users\\Urdhv\\Desktop\\Python programs\\FileReading\\creators.csv', 'w')
    file.truncate()
    file.close()


def main():
    EXEC_FILE = 'C:\\Users\\Urdhv\\Desktop\\Python programs\\FileReading\\Internet_Data.xlsx'
    # CSV_FILE = 'C:\\Users\\Urdhv\\Desktop\\Python programs\\FileReading\\creators.csv'

    df = pd.read_excel(EXEC_FILE)   #creates a data frame for our excel file
    writeCSVdefault(df) 
    # erase_CSV()


# test()
main()

