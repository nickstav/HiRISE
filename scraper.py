# coding: utf-8
import urllib3
from bs4 import BeautifulSoup

#require a PoolManager instance to make requests. 
#this object handles all of the details of connection pooling and thread safety.
http = urllib3.PoolManager()


def getDTMInfo(id):
    partial_url = 'https://www.uahirise.org/dtm/dtm.php?ID='
    page_url = partial_url + id

    #obtain all the details from the DTM ID's webpage as a string of text
    webPage = getParsedHtml(page_url)
    
    #get the image source. If no image is found, we can assume the DTM ID was unrecognised by the website
    imageSource = checkImageSource(webPage)
    if not imageSource:
        return None

    #obtain the section of the website with all the required details
    DTMDetails = getDTMDetails(webPage)

    #create a dictionary to store the required info in
    results = {}

    #pick out the title, elevation range & other info from their relevant website sections
    title = getTitle(webPage)
    DTMInfo = parseRequiredInfo(DTMDetails)
    elevationRange = getMinMaxElevation(webPage)

    #add the information to the results dictionary
    results["DTMTitle"] = title
    results["ID"] = id
    results["imageURL"] = imageSource
    results["leftObservation"] = DTMInfo["leftObservation"]
    results["rightObservation"] = DTMInfo["rightObservaton"]
    results["latitude"] = DTMInfo["latitude"]
    results["longitude"] = DTMInfo["longitude"]
    results["minElevationRange"] = elevationRange["minElevation"]
    results["maxElevationRange"] = elevationRange["maxElevation"]

    #replace any blank info with an error message
    checkForIncompleteData(results)
       
    print("DTM Info successfully obtained")
    return results



def getParsedHtml(url):
    try:
        response = http.request('GET', url, timeout=5.0)
        parsedHtml = BeautifulSoup(response.data, 'html.parser')
        return parsedHtml
    except Exception as error:
        print(error)
        return None


#function to check if webpage has failed to load a specific DTM, by analysing the 
#image object and its href link. If an image is found, the img src is returned
#in order to download the image to file
def checkImageSource(parsedwebPage):
    try:
        imageData = parsedwebPage.find(class_='observation-picture')
        hrefData = imageData.find("a").get("href")

        #if no image is loaded, the <img> source will be as below:
        noImageLink = "https://hirise-pds.lpl.arizona.edu/PDS/EXTRAS/DTM/.ca.jpg"

        if hrefData == noImageLink:
            return None
        else: 
            return hrefData

    except Exception as error:
        print(error)
        return None
    #the except catch will also deal with an incorrect url (ie if parsedWebPage= None)



def getTitle(parsedHtml):
    fullTitle = parsedHtml.find(class_= 'observation-id-title')
    return fullTitle.text


#function to obtain all the text from the section of the webpage that contains required info
def getDTMDetails(parsedHtml):
    hiRiseData = parsedHtml.find(class_= 'product-text-gamma')
    relevantDetails = hiRiseData.find_all(text=True)
    return relevantDetails


#function to take the array containing all text from web section and return the next block of
#text after a specific title or subheading
def parseRequiredInfo(details):
    for index, detail in enumerate(details):
        if detail == 'Left observation':
            leftObservation = details[index + 1]
            
        elif detail == 'Right observation':
            rightObservation = details[index + 1]
            
        elif detail == 'Latitude (center)':
            latitude = details[index + 1].strip()[:-1]
        elif detail == 'Longitude (center)':
            longitude = details[index + 1].strip()[:-1]

    DTMInfo = {
        "leftObservation": leftObservation,
        "rightObservaton": rightObservation,
        "latitude": float(latitude),
        "longitude": float(longitude)
    }   
    
    return DTMInfo 



def getMinMaxElevation(parsedHtml):
    #find the href link to open the readMe page containing elevation info
    readMeLink = parsedHtml.find("a", text="Extras Read me")
    href_link = readMeLink.get("href")
    readMeURL = 'https://www.uahirise.org' + href_link[2:] #remove 2 dots from start of the href link

    readMeData = getParsedHtml(readMeURL)
    textString = readMeData.get_text()

    #split the text string into its separate rows
    textStringRows = textString.split("\n")

    #obtain the text from each row that contains "VALID_" and strip any white spaces
    minMax = [text.strip() for text in textStringRows if ("VALID_" in text)]

    #only take numerical values of min/max elevation from the section & turn into a single string
    minElevStringCharacs = [value for value in minMax[0] if (value in "-.0123456789")]
    minElevation = ''.join(minElevStringCharacs)
    maxElevStringCharacs = [value for value in minMax[1] if (value in "-.0123456789")]
    maxElevation = ''.join(maxElevStringCharacs)
  
    range = {
        "minElevation": float(minElevation),
        "maxElevation": float(maxElevation) #convert from a string to a float number
    }
  
    return range



def checkForIncompleteData(dictionary):
    errorMessage = 'this information could not be obtained'
    for item in dictionary:
        if item == '':
            item = errorMessage

