def getIdFromUser():
    DTM_ID = str(input("Enter a DTM ID (or type 'exit' to quit):\n"))
    validID = checkIdIsValid(DTM_ID)
    if not validID:
        return None

    return DTM_ID


def checkIdIsValid(id):
    if id == 'exit':
        exit()
    elif len(id) < 15 or len(id) > 15:
        print("Error: DTM ID should be 15 characters long")
        return False
    elif id[3] != '_' or id[10] != '_':
        print("Error: ID should be of format XXX_000000_0000")
        return False
    else:
        return True
