
def findTablesWrapper(accInstr, dbTbls, server, database, columnsDict):
    ptList = []
    finalTuples = dbTbls[database][server]
    columns = columnsDict[server]

    for tuple in finalTuples:
        ptList.append(tuple[0])

    colorDict = {}

    i = 0
    for tuple in finalTuples:
        if i % 3 == 0:
            colorDict[tuple[0]] = "redrow"
        else:
            colorDict[tuple[0]] = "normrow"
        i += 1

    return ptList, finalTuples, columns, colorDict

def tabTupsToDict(finalTuples):
    myDict = {}
    for tup in finalTuples:
        myDict[tup[0]] = tup[1:]
    return myDict