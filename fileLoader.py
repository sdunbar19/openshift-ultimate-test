import json

fileName = 'json/allInfo.json'

def openJSONFile():
    with open(fileName) as jsonFile:
        return json.load(jsonFile)

def writeToJSONFile(item):
    itemDump = json.dumps(item)
    fdFile = open(fileName, 'w')
    fdFile.write(itemDump)
    fdFile.close()

def createInfoDicts():
    infoDict = {}
    columns = ["Name", "Age", "Star sign"]
    tables = ["Geoff", "Nancy", "Emma", "Sarah"]
    rows = []
    rows.append(["Geoff", 50, "Scorpio"])
    rows.append(["Nancy", 49, "Virgo"])
    rows.append(["Sarah", 21, "Taurus"])
    rows.append(["Emma", 17, "Leo"])
    schema = "Family"
    currDate = "jeff bezos"
    irregTimesDict = {"Emma": 1}
    infoDict["database"] = {}
    infoDict["database"]["family"] = (columns, tables, rows, schema, currDate, irregTimesDict)
    columns = ["Name", "Age", "Star sign"]
    tables = ["Anna", "Alexandra", "Krissy", "Annabel", "Iris"]
    rows = []
    rows.append(["Anna", 20, "Libra"])
    rows.append(["Alexandra", 20, "Scorpio"])
    rows.append(["Krissy", 20, "Aries"])
    rows.append(["Annabel", 20, "Taurus"])
    rows.append(["Iris", 20, "Aquarius"])
    schema = "Friends"
    currDate = "bugs life"
    irregTimesDict = {"Krissy": 1}
    infoDict["database"]["friends"] = (columns, tables, rows, schema, currDate, irregTimesDict)
    writeToJSONFile(infoDict)

def getAllInfoDict():
    return openJSONFile()

def refresh():
    infoDict = openJSONFile()
    for database, serverDict in infoDict.items():
        for server, tup in serverDict.items():
            rows = tup[2]
            for row in rows:
                row[1] = int(row[1]) + 1
    writeToJSONFile(infoDict)
            

def refreshSpecific(database, server):
    infoDict = openJSONFile()
    rows = infoDict[database][server][2]
    for row in rows:
        row[1] = int(row[1]) + 1
    writeToJSONFile(infoDict)

if __name__ == "__main__":
    createInfoDicts()