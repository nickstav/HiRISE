import json, os
from scraper import http

imageFolderPath = "data/image/"
jsonFolderPath = "data/json/"

def saveImage(dictionary, id):
    #download will take a few seconds so notify user what is happening
    print("downloading image...")
    
    fileName = imageFolderPath + id + ".jpeg"
    imageURL = dictionary["imageURL"]

    #check if required folder exists and create it if not
    if not os.path.exists(imageFolderPath):
        os.makedirs(imageFolderPath)
        print("image folder created")

    try:
        response = http.request('GET', imageURL)
        with open(fileName, "wb") as image: # w = write mode, b = binary mode for images
            image.write(response.data)
        print("image saved successfully")
    except Exception as error:
        print("image could not be saved")
        print(error)

    

def writeJSON(dictionary, id): 
    fileName = jsonFolderPath + id + ".json"
    jsonObject = json.dumps(dictionary, indent = 4) 

    #check if required folder exists and create it if not
    if not os.path.exists(jsonFolderPath):
        os.makedirs(jsonFolderPath)
        print("json folder created")

    with open(fileName, "w") as file: 
        file.write(jsonObject)

    print("json successfully created")


def cleanUpResults(dictionary):
    #remove image URL from results as we no longer need the image source
    del(dictionary["imageURL"])