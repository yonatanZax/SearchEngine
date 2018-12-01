
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


def getDataFrameFromFile(path, sep):
    import pandas as pd
    try:
        df = pd.read_csv(path,sep, index_col=0)
    except:
        # print('Error in BasicMethods, getDataFrameFromFile')
        return None

    return df







