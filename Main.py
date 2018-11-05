
import os
import Configuration as config
from Indexing.Indexer import Indexer
from ReadFiles.ReadFile import ReadFile
from datetime import datetime
import MyExecutors
import Indexing.MyDictionary
import multiprocessing


def initProject():
    import shutil
    import os
    savedFilesPath = config.savedFilePath
    shutil.rmtree(savedFilesPath)
    if not os.path.exists(savedFilesPath):
        os.mkdir(savedFilesPath)
    print('Project was created successfully..')


def main():
    print("***   Main Start   ***")
    initProject()

    indexer = Indexer()
    fileReader = ReadFile(indexer, config.corpusPath)
    # try:
        # fileReader.readAllFiles()
    listOfFolders = os.listdir(config.corpusPath)
    counter = 0
    thisRunFolderResult = []
    startTime = datetime.now()
    for folder in listOfFolders:
        if counter < 10:
            result = MyExecutors._instance.CPUExecutor.apply_async(fileReader.readTextFile, (folder,))
            counter += 1
            thisRunFolderResult.append(result)
        else:
            for result in thisRunFolderResult:
                result.get()
            indexer.flushMemory()
            indexer = Indexer()
            fileReader = ReadFile(indexer, config.corpusPath)
            counter = 0
    for result in thisRunFolderResult:
        result.get()
    indexer.flushMemory()

    # except Exception:
    #     finishTime = datetime.now()
    #     timeItTook = finishTime - startTime
    #     print(timeItTook.seconds)

    # listOfFolders = os.listdir(corpusPath)
    #
    # for folder in listOfFolders:
    #     print(folder)
    #     folderPath = corpusPath + '\\' + folder
    #     filePath = folderPath + '\\' + folder
    #     myIndexer = Indexer()
    #     readFile = ReadFile(myIndexer, corpusPath)
    #     readFile.readTextFile(filePath=filePath)
    # MyExecutors._instance.CPUExecutor.close()
    # print("CPU Closed")
    # MyExecutors._instance.CPUExecutor.join()
    # print("CPU Finished")
    # MyExecutors._instance.IOExecutor.close()
    # print ("IO Closed")
    # MyExecutors._instance.IOExecutor.join()
    # print ("IO Finished")

    finishTime = datetime.now()
    timeItTook = finishTime - startTime

    # indexer.myDictionary.print()

    finishTime = datetime.now()
    # timeItTook2 = finishTime - startTime

    # # Write dictionary to file
    # from Indexing import FileWriter
    #
    # headLineAsArray = ['Term', 'Posting']
    # FileWriter.writeDictionaryToFile('dictionaryAsFile', headLineAsArray, dictionaryToWrite=indexer.myDictionary)

    print(str(timeItTook.seconds) + " seconds" )
    # print(str(timeItTook2.seconds) + " seconds after sorting")

    print('***   Done   ***')








if __name__ == "__main__":
    main()