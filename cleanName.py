import magic
import csv

def isSChara(ch):
    # set0 = list(range('\u0000','\u002F'))
    # set1 = list(range('\u005B', '\u007E'))
    # set2 = list(range('\u00A0','\u00BE'))
    #top code doesn't work
    
    return False if ('\u0000' <= ch <= '\u002F'
        or '\u005B' <= ch <= '\u0060'
        or '\u007B' <= ch <= '\u007E' 
        or '\u00A0' <= ch <= '\u00BE') else True

#remade string should be our first round of purging
#we still need to purge honorifics
def openFile(fPath):
    with open(fPath, newline='', encoding="utf-8") as f1:
        reader = csv.DictReader(f1)

        #remember: Dictreader returns a dictionary of every row
        #the key is the title of each columns
        #the value is the data present in eaach row

        for doc in reader:
            # print(doc)

            remadeString = "".join(ch for ch in doc["Username"] if isSChara(ch))
            print(remadeString)

def getFile():
    fPath = ''
    fType = ''

    try:
        fPath = input("Enter file path: ")
        fType = magic.from_file(fPath)
    except Exception as e:
        print(e)
        return
    
    return fPath

def execute():
    fPath = getFile()
    if fPath == None:
        return
    
    openFile(fPath)

def main():
    execute()

main()