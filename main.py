from saveToJSON import writeJSON
from scraper import getDTMInfo
from userInput import getIdFromUser

#Test_DTM_ID = "ESP_015943_1390"

def runProject():
    DTM_ID = getIdFromUser()
    relevantInfo = getDTMInfo(DTM_ID)

    if not relevantInfo:
        print("DTM info could not be found")
        print("type 'python main.py' to run again")
    else:
        writeJSON(relevantInfo, DTM_ID)
        print("type 'python main.py' to run again")

runProject()