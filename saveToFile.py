import json
from scraper import http

def saveImage(dictionary, id):
    #download will take a few seconds so notify user what is happening
    print("downloading image...")
    
    fileName = "data/image/" + id + ".jpeg"
    imageURL = dictionary["imageURL"]
    try:
        response = http.request('GET', imageURL)
        with open(fileName, "wb") as image: # w = write mode, b = binary mode for images
            image.write(response.data)
        print("image saved successfully")
    except:
        print("image could not be saved")

    del(dictionary["imageURL"]) #as we no longer need the image source

def writeJSON(dictionary, id): 
    fileName = "data/json/" + id + ".json"
    jsonObject = json.dumps(dictionary, indent = 4) 

    with open(fileName, "w") as file: 
        file.write(jsonObject)

    print("json successfully created")