import json

def writeJSON(dictionary, id): 
    fileName = id + ".json"
    jsonObject = json.dumps(dictionary, indent = 4) 
    with open(fileName, "w") as file: 
        file.write(jsonObject)
    print("json successfully created")
