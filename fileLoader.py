def getAllInfoDict():
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
    infoDict["database"]["server"] = (columns, tables, rows, schema, currDate, irregTimesDict)

def refresh():
    pass

def refreshSpecific():
    pass