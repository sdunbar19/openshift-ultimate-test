def tabTupsToDict(finalTuples):
    myDict = {}
    for tup in finalTuples:
        myDict[tup[0]] = tup[1:]
    return myDict