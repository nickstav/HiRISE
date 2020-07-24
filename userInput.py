def getIDFromUser():
    DTM_ID = input("Enter a DTM ID (or type 'exit' to quit):\n")
    if not checkIDIsValid(DTM_ID):
        return None

    return DTM_ID


def checkIDIsValid(ID):
    if ID == 'exit':
        exit()
    elif len(ID) < 15 or len(ID) > 15:
        print("Error: DTM ID should be 15 characters long")
        return False
    elif ID[3] != '_' or ID[10] != '_':
        print("Error: ID should be of format XXX_000000_0000")
        return False
    else:
        return True
