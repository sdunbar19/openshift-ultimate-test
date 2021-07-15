dbTbls = {}
dbTbls['sample'] = {}
listLists = []

dbTbls['sample']['database'] = listLists
for i in range(5):
    listLists.append(["name_" + str(i), "date" + str(50 - i)])
accInstr = {}
dbTbls['sample']['mello yello'] = listLists
dbTbls['sample']['green bean'] = listLists
accInstr['database'] = ['sample', 'sample', 'user']

columnsDict = {}
columnsDict['database'] = ['reporting date']

def createDictionaries():
    return dbTbls, accInstr, columnsDict

if __name__ == "__main__":
    createDictionaries()