


def writeDataframeToFile(dataFrame, path):
    try:
        dataFrame.to_csv(path,sep='|')
        return True
    except:
        print('Error in BasicMethods, writeDataframeToFile')
        return False



def getDataFrameFromFile(path, sep):
    import pandas as pd
    try:
        df = pd.read_csv(path,sep, index_col=0)
    except:
        # print('Error in BasicMethods, getDataFrameFromFile')
        return None

    return df




def addColumnToDataFrame(oldDataFrame, colName, colAsVector):
    import pandas as pd
    df = oldDataFrame
    newColumn = pd.Series(colAsVector)
    df[colName] = newColumn.values

    return df


def createDataFrameByColumns(columnNamesAsArray, listOfColumns):
    import pandas as pd
    df = pd.DataFrame()
    for i in range(0, len(columnNamesAsArray)):
        colAsSeries = pd.Series(listOfColumns[i])
        df[columnNamesAsArray[i]] = colAsSeries

    return df



def getColumnAsVectorFromDataframe(dataFrame, columnName):

    try:
        columnAsVector = dataFrame[columnName].tolist()
        return columnAsVector
    except:
        print('Error in method getColumnFromDataframe')
        return None



# valuesAsArray = [['Date',int(date)],['Time',time]]
def getSubDataFrame(dataFrame, valuesAsArray):
    try:
        if valuesAsArray[1] == 'TRUE':
            return dataFrame
        subDataFrame = dataFrame.loc[dataFrame[valuesAsArray[0]] == valuesAsArray[1]]
    except TypeError as e:
        print(e)
        print(dataFrame,valuesAsArray)
    return subDataFrame
