import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()


def getDTMInfo(id):
    partial_url = 'https://www.uahirise.org/dtm/dtm.php?ID='
    page_url = partial_url + id

    webPage = getParsedHtml(page_url)
    DTMDetails = getDTMDetails(webPage)
    results = {}

    title = getTitle(webPage)
    DTMInfo = parseRequiredInfo(DTMDetails)
    elevationRange = getMinMaxElevation(webPage)
    
    results["DTM Title"] = title
    results["Left Observation"] = DTMInfo["leftObservation"]
    results["Right Observation"] = DTMInfo["rightObservaton"]
    results["Latitude"] = DTMInfo["latitude"]
    results["Longitude"] = DTMInfo["longitude"]
    results["Min Elevation Range"] = elevationRange["minElevation"]
    results["Max Elevation Range"] = elevationRange["maxElevation"]

    if title == '':
        return False
    else:
        print("DTM Info successfully obtained")
        return results



def getParsedHtml(url):
    response = http.request('GET', url)
    parsedHtml = BeautifulSoup(response.data, 'html.parser')
    return parsedHtml



def getTitle(parsedHtml):
    fullTitle = parsedHtml.find(class_= 'observation-id-title')
    return fullTitle.text



def getDTMDetails(parsedHtml):
    hiRiseData = parsedHtml.find(class_= 'product-text-gamma')
    relevantDetails = hiRiseData.find_all(text=True)
    return relevantDetails



def parseRequiredInfo(details):
    for index, detail in enumerate(details):
        if detail == 'Left observation':
            leftObservation = details[index + 1]
            
        elif detail == 'Right observation':
            rightObservation = details[index + 1]
            
        elif detail == 'Latitude (center)':
            latitude = details[index + 1]
            
        elif detail == 'Longitude (center)':
            longitude = details[index + 1]
    DTMInfo = {
        "leftObservation": leftObservation,
        "rightObservaton": rightObservation,
        "latitude": latitude,
        "longitude": longitude
    }   
    return DTMInfo 



def getMinMaxElevation(parsedHtml):
    readMeLink = parsedHtml.find("a", text="Extras Read me")
    href_link = readMeLink.get("href")
    readMeURL = 'https://www.uahirise.org' + href_link[2:] #remove 2 dots from start of the href link

    readMeData = getParsedHtml(readMeURL)
    textString = readMeData.get_text()

    searchStringForMin = "VALID_MINIMUM    = "
    searchStringForMax = "VALID_MAXIMUM    = "
    lengthOfRequiredString = 10 #how long the min/max elevation result will be

    startMinimum = textString.index(searchStringForMin) + len(searchStringForMin)
    endMinimum = startMinimum + lengthOfRequiredString
    minElevation = textString[startMinimum:endMinimum]

    startMaximum = textString.index(searchStringForMax) + len(searchStringForMax)
    endMaximum = startMaximum + lengthOfRequiredString
    maxElevation = textString[startMaximum:endMaximum]

    range = {
        "minElevation": minElevation,
        "maxElevation": maxElevation
    }
  
    return range
