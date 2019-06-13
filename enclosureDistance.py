import csv

# Searches through the AlaskaTA construction reports text file
# for Enclosure Type and prints output to csvfile test.csv
def main():
    namesFile = 'AlaskaTA-StationList.csv' # file of names
    fileName = 'AlaskaTA-ConstructionReports.txt' # text file of reports
    names = getStationList(namesFile) # makes list of needed station names
    file = open(fileName,'r') # opens report file for reading
    # blockList = makeBlocks((file.read()[0:10000])) sub blocks -- for testing purposes
    blockList = makeBlocks(file.read()) # seperetes reports into discrete sections
    myDict = createDict(names) # makes baseline dictionary of all wanted names

    # string parsing of blocks
    for block in blockList:
        station = validBlock(block, names)
        if(station is not None): # checks whether block is for TA station
            ind = block.find('Distance from BB casing:')
            if(ind != -1):
                ind += len('Distance from BB casing:') + 1
                end = block.find('\n', ind)
                myDict[station].add(block[ind:end]) # adds condition entry
    makeCSV(myDict) # writes answers to csv file

# makes blocks out of text file
def makeBlocks(input):
    blocks = []
    ind = input.find("_______________________________________________")
    while(ind != -1):
        block = input[0:(ind+47)]
        blocks.append(block)
        input = input[(ind+47):len(input)]
        ind = input.find("_______________________________________________")
    return blocks

# make list of valid station names
def getStationList(nameFile):
    names = []
    with open(nameFile, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            names.append((', '.join(row))[0:4])
        # remove header and blankline
        del names[0]
        del names[193]
        return(names)

# checks if block is in alaska TA, returns the station of block
def validBlock(bl, names):
    for substring in names :
        if(bl.count(substring) > 1):
            return substring
    return None

# creates dicttionary of relevant TA station with empty values
def createDict(names):
    myDict = {}
    for name in names:
        myDict[name] = set()
    return myDict

# Creates csv files with relevant columns/ answers
def makeCSV(dict):
    with open('output.csv', 'w') as csvfile:
        fieldnames = ['Station', 'Distance from BB casing:']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key in dict.keys():
            writer.writerow({'Station': key, 'Distance from BB casing:': (", ".join(dict[key]))})

# runs main
main()
