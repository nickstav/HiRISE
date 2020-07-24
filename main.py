from saveToFile import saveImage, writeJSON
from scraper import getDTMInfo
from userInput import getIdFromUser

#Test_DTM_ID = "ESP_015943_1390"

def runProject():
    #get the user inputed ID (if incorrect ID was entered, then run function again to request a new one)
    DTM_ID = getIdFromUser()
    if not DTM_ID:
        runProject() #start again to request a new ID value
        return

    #use the ID to fetch all required information from the DTM's webpage
    relevantInfo = getDTMInfo(DTM_ID)

    if relevantInfo is None:
        print("DTM info could not be found")
        runProject()
        return

    #save the image and a JSON file with required info to the local data folder
    saveImage(relevantInfo, DTM_ID)
    writeJSON(relevantInfo, DTM_ID)

    #allow the user to input a new ID once files have been saved
    runProject()

runProject()