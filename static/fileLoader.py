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
    columns = ["Name", "Date"]
    tables = ["Test"]
    rows = []
    rows.append(["Test", "Testdate"])
    schema = "schema"
    currDate = "date"
    irregTimesDict = {}
    infoDict["database"] = {}
    infoDict["database"]["server"] = (columns, tables, rows, schema, currDate, irregTimesDict)
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