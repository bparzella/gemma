import os

def processProgramFilename(processProgramScope, processProgramID):
    return os.path.abspath("data/processprogram/" + processProgramScope + "/" + processProgramID)

def getProcessProgram(processProgramScope, processProgramID):
    filename = processProgramFilename(processProgramScope, processProgramID)

    if not os.path.exists(filename):
        return None

    with open(filename, "r") as file:
        data = file.read()    

    return data

def storeProcessProgram(processProgramScope, processProgramID, processProgramData):
    filename = processProgramFilename(processProgramScope, processProgramID)
    filepath = os.path.dirname(filename)

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    with open(filename, "w") as file:
        file.write(processProgramData)    
