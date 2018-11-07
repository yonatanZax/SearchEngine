



def createDataFrameByColumns(columnNamesAsArray, listOfColumns):
    import pandas as pd
    df = pd.DataFrame()
    for i in range(0, len(columnNamesAsArray)):
        colAsSeries = pd.Series(listOfColumns[i])
        df[columnNamesAsArray[i]] = colAsSeries

    return df






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


