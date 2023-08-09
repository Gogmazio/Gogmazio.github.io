import json
import csv

# Converts dictionary with player character data of one subclass into a sorted csv file
def convertToCSV(data, jobName):
    playerDict = []
    field_names = ['No', 'IGN', 'Fame', 'charId']
    placement = 1

    sorted_by_fame = sorted(data.items(), key=lambda x:x[1][0], reverse=True)

    for char in sorted_by_fame:
        playerDict.append({'No':placement, 'IGN':char[0], 'Fame':char[1][0], 'charId':char[1][2]})
        placement += 1

    with open(r'./csv/' + jobName + r".csv", 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(playerDict)

# Returns all base class and subclass names and ids
def getClassIds():
    data = dict()

    with open("classIds.json", 'r') as infile:
        data = json.load(infile)
        infile.close()

    return data
