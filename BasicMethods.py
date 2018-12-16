
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




def get2DArrayFromFile(path, sep = '|'):

    try:
        myFile = open(path,'r')

        with myFile:
            lines = myFile.readlines()
            myFile.close()
            twoDArray = []

            for line in lines:
                lineAsArray = line.split(sep)
                lineAsArray[len(lineAsArray)-1] = lineAsArray[len(lineAsArray)-1][:-1]
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
    start = textAsString.find(tag1) + len(tag1)
    end = textAsString[start:].find(tag2)
    content = textAsString[start:start+end]
    return content.strip(' ')



textAsString = '''

<DOC>
<DOCNO> FBIS3-1 </DOCNO>
<HT>  "cr00000011094001" </HT>



<top>

<num> Number: 351 
<title> Falkland petroleum exploration 

<desc> Description: 
What information is available on petroleum exploration in 
the South Atlantic near the Falkland Islands?

<narr> Narrative: 
Any document discussing petroleum exploration in the
South Atlantic near the Falkland Islands is considered
relevant.  Documents discussing petroleum exploration in 
continental South America are not relevant.

</top>
'''

# docNo = getTagFromText(textAsString,tag1='<DOCNO>',tag2='</DOCNO>')
# num = getTagFromText(textAsString, tag1='<num>')
# print(num)
# title = getTagFromText(textAsString, tag1='<title>')
# print(title)

