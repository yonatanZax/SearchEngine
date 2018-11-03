
import os
import Configuration as config
from Indexing.Indexer import Indexer
from ReadFiles.ReadFile import ReadFile
from datetime import datetime
import MyExecutors
import multiprocessing


def initProject():
    print('Create folders')


def main():
    print("***   Main Start   ***")
    startTime = datetime.now()

    corpusPath = config.getAbsolutePathToDataFolderAndFileType('corpus')
    indexer = Indexer()
    fileReader = ReadFile(indexer, corpusPath)
    try:
        fileReader.readAllFiles()
    except:
        finishTime = datetime.now()
        timeItTook = finishTime - startTime
        print(timeItTook.seconds)

    # listOfFolders = os.listdir(corpusPath)
    #
    # for folder in listOfFolders:
    #     print(folder)
    #     folderPath = corpusPath + '\\' + folder
    #     filePath = folderPath + '\\' + folder
    #     myIndexer = Indexer()
    #     readFile = ReadFile(myIndexer, corpusPath)
    #     readFile.readTextFile(filePath=filePath)
    MyExecutors._instance.CPUExecutor.close()
    print("CPU Closed")
    MyExecutors._instance.CPUExecutor.join()
    print("CPU Finished")
    MyExecutors._instance.IOExecutor.close()
    print ("IO Closed")
    MyExecutors._instance.IOExecutor.join()
    print ("IO Finished")

    print(indexer.dictionary)

    finishTime = datetime.now()
    timeItTook = finishTime - startTime
    print(timeItTook.seconds)

    print('***   Done   ***')








if __name__ == "__main__":
    main()