
def isInt(value):
  try:
    int(value)
    return True
  except ValueError:
    return False


def isfloat(value):
  """
    Checks if the given value represent float
  :param value:
  :return: True if float
  """
  try:
    float(value)
    return True
  except:
    return False

def getWriteOnly(file_name):
    """
    Get the correct openning flag for files for write only.
    :param file_name: the file name including the end.
    :return: If the file ends with '.txt' will return "w", if its '.bin' return "wb"
    """
    filename = ""
    filename += file_name
    splittedFileName = filename.split(".")
    if splittedFileName[len(splittedFileName)-1] == "txt":
        return "w"
    elif splittedFileName[len(splittedFileName)-1] == "bin":
        return "wb"

def getReadOnly(file_name):
    """
    Get the correct openning flag for files for read only.
    :param file_name: the file name including the end.
    :return: If the file ends with '.txt' will return "r", if its '.bin' return "rb"
    """
    filename = ""
    filename += file_name
    splittedFileName = filename.split(".")
    if splittedFileName[len(splittedFileName)-1] == "txt":
        return "r"
    elif splittedFileName[len(splittedFileName)-1] == "bin":
        return "rb"

def getAppendingOnly(file_name):
    """
    Get the correct openning flag for files for appending only.
    :param file_name: the file name including the end.
    :return: If the file ends with '.txt' will return "a", if its '.bin' return "ab"
    """
    filename = ""
    filename += file_name
    splittedFileName = filename.split(".")
    if splittedFileName[len(splittedFileName)-1] == "txt":
        return "a"
    elif splittedFileName[len(splittedFileName)-1] == "bin":
        return "ab"

def getWritePlusOnly(file_name):
    """
    Get the correct openning flag for files for write and read only.
    :param file_name: the file name including the end.
    :return: If the file ends with '.txt' will return "w+", if its '.bin' return "wb+"
    """
    filename = ""
    filename += file_name
    splittedFileName = filename.split(".")
    if splittedFileName[len(splittedFileName)-1] == "txt":
        return "w+"
    elif splittedFileName[len(splittedFileName)-1] == "bin":
        return "wb+"

def getReadPlusOnly(file_name):
    """
    Get the correct openning flag for files for write and read only.
    :param file_name: the file name including the end.
    :return: If the file ends with '.txt' will return "r+", if its '.bin' return "rb+"
    """
    filename = ""
    filename += file_name
    splittedFileName = filename.split(".")
    if splittedFileName[len(splittedFileName)-1] == "txt":
        return "r+"
    elif splittedFileName[len(splittedFileName)-1] == "bin":
        return "rb+"

def getAppendingPlusOnly(file_name):
    """
    Get the correct openning flag for files for appending plus.
    :param file_name: the file name including the end.
    :return: If the file ends with '.txt' will return "a+", if its '.bin' return "ab+"
    """
    filename = ""
    filename += file_name
    splittedFileName = filename.split(".")
    if splittedFileName[len(splittedFileName)-1] == "txt":
        return "a+"
    elif splittedFileName[len(splittedFileName)-1] == "bin":
        return "ab+"



def checkIfFileExists(path):
    import os.path
    exist = os.path.exists(path)
    return exist



def getColumnIndexFromHeadLline(headlineAsArray, colName):
    colIndex = -1
    for i in range(0, len(headlineAsArray)):
        if headlineAsArray[i] == colName or headlineAsArray[i] == colName + '\n':
            colIndex = i

    return colIndex



def getStringSizeInBytes(string):
    return len(string.encode('utf-8'))



def writeListToFile(path:str,fileName:str,listToWrite:list,useNewLine = True):
    import os

    if not os.path.exists(path) or len(listToWrite) == 0:
        return

    try:
        myFile = open(path + '/' + fileName,'a')

        for line in listToWrite:
            if useNewLine:
                myFile.write('|'.join(line) + '\n')
            else: myFile.write('|'.join(line))

        myFile.close()

    except Exception as ex:
        print(ex)


def get2DArrayFromFile(path, sep = '|'):

    try:
        myFile = open(path,'r')

        with myFile:
            lines = myFile.readlines()
            myFile.close()
            twoDArray = []

            for line in lines:
                line = line.rstrip('\n')
                lineAsArray = line.split(sep)
                twoDArray.append(lineAsArray)

            return twoDArray

    except Exception as ex:
        print("Error while converting file to 2D array, E: ",ex)



def getDicFromFile(path, sep = '|'):

    try:
        myFile = open(path,'r')

        with myFile:
            lines = myFile.readlines()
            myFile.close()
            myDict = {}

            for line in lines:
                lineAsArray = line.split(sep)
                myDict[lineAsArray[0]] = lineAsArray[1:]

            return myDict

    except Exception as ex:
        print("Error while converting file to 2D array, E: ",ex)


def getTagFromText(textAsString,tag1,tag2='\n'):
    find = textAsString.find(tag1)
    if find == -1:
        return ''
    start =  find + len(tag1)
    end = textAsString[start:].find(tag2)
    content = textAsString[start:start+end]
    return content.strip(' ')



def getStringFormatForFloatValue(numOfDigits,valueAsFloat):
    formatString = "{0:.%sf}" % (str(numOfDigits))
    return str(formatString.format(round(valueAsFloat, numOfDigits)))

