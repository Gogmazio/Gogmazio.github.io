import json
import requests
import time
import threading
import data_manip

apiKey = "Pm5PQyScdTkDVktXSWP3Ut1oOLyBSeKW"
bigrams = []
charFameDict = {}
start_time = time.time()
classData = data_manip.getClassIds()

# avg 42s per subclass
#alphanum = "abcdefghijklmnopqrstuvwxyz1234567890[]().,~`-_+="
# avg 12s per subclass
alphanum = "acdehilmnorstuykv095"
# avg 2s per subclass
#alphanum = "acd"

for letter in alphanum:
    for secondLetter in alphanum:
        bigrams.append(letter+secondLetter)

total = len(bigrams)

# Searches for players with a specific base class and subclass. Search ranges are used for separating the bigrams.
def search(searchRangeLow, searchRangeHigh, jobId, jobGrowId):
    for elem in range(searchRangeLow, searchRangeHigh - 1):
        response = requests.get("https://api.dfoneople.com/df/servers/cain/characters?characterName="
                                +bigrams[elem]+"&jobId="+jobId+"&jobGrowId="+jobGrowId
                                +"&limit=200&wordType=full&apikey="+apiKey)
        dictionary = response.json()

        for char in dictionary['rows']:
            try:
                if char['fame'] > 1:
                    charFameDict[char['characterName']] = (char['fame'], char['jobGrowName'], char['characterId'])
            except:
                pass

# Creates 10 threads and separates the workload based on the size of the bigrams list.
def startSearch(jobId, jobGrowId):
    upperLimit = int(total / 10)

    x1 = threading.Thread(target=search,args=(0, upperLimit, jobId, jobGrowId))
    x2 = threading.Thread(target=search,args=(upperLimit, upperLimit * 2, jobId, jobGrowId))
    x3 = threading.Thread(target=search,args=(upperLimit * 2, upperLimit * 3, jobId, jobGrowId))
    x4 = threading.Thread(target=search,args=(upperLimit * 3, upperLimit * 4, jobId, jobGrowId))
    x5 = threading.Thread(target=search,args=(upperLimit * 4, upperLimit * 5, jobId, jobGrowId))
    x6 = threading.Thread(target=search,args=(upperLimit * 5, upperLimit * 6, jobId, jobGrowId))
    x7 = threading.Thread(target=search,args=(upperLimit * 6, upperLimit * 7, jobId, jobGrowId))
    x8 = threading.Thread(target=search,args=(upperLimit * 7, upperLimit * 8, jobId, jobGrowId))
    x9 = threading.Thread(target=search, args=(upperLimit * 8, upperLimit * 9, jobId, jobGrowId))
    x10 = threading.Thread(target=search, args=(upperLimit * 9, total, jobId, jobGrowId))

    x1.start()
    x2.start()
    x3.start()
    x4.start()
    x5.start()
    x6.start()
    x7.start()
    x8.start()
    x9.start()
    x10.start()

    x1.join()
    x2.join()
    x3.join()
    x4.join()
    x5.join()
    x6.join()
    x7.join()
    x8.join()
    x9.join()
    x10.join()

api_test = requests.get("https://api.dfoneople.com/df/servers?apikey="+apiKey).status_code

if api_test == 200:
    for baseClass in classData['rows']:
        for subClass in baseClass['rows']:
            print(baseClass['jobName'] + " | " + subClass['jobGrowName'])
            startSearch(baseClass['jobId'], subClass["jobGrowId"])

            data_manip.convertToCSV(charFameDict, baseClass['jobName'] + ' ' + subClass['jobGrowName'][5:])
            charFameDict.clear()
            # if baseClass['jobName'] == "Mage (F)" and subClass['jobGrowName'] == "Neo: Battle Mage":
            #     print(baseClass['jobName'] + " | " + subClass['jobGrowName'])
            #     startSearch(baseClass['jobId'], subClass["jobGrowId"])
            #
            #     data_manip.convertToCSV(charFameDict, baseClass['jobName'] + ' ' + subClass['jobGrowName'][5:])
            #     charFameDict.clear()
else:
    print(api_test)
    exit(0)

print("--- %s seconds ---" % (time.time() - start_time))