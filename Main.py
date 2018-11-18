
import os
import Configuration as config
from Indexing.Indexer import Indexer
from ReadFiles.ReadFile import ReadFile
from datetime import datetime
from Manager import MyManager
import multiprocessing as mp

def initProject():
    import shutil
    import os
    savedFilesPath = config.savedFilePath
    if os.path.exists(savedFilesPath):
        shutil.rmtree(savedFilesPath + "//")
    while 1:
        try:
            os.mkdir(savedFilesPath)
            break
        except PermissionError:
            continue


    print('Project was created successfully..')


def main():
    print("***   Main Start   ***")
    initProject()
    managerRun()
    # regularRun()



def regularRun():
    indexer = Indexer()
    fileReader = ReadFile(indexer, config.corpusPath)
    # try:
    # fileReader.readAllFiles()
    listOfFolders = os.listdir(config.corpusPath)
    counter = 0
    thisRunFolderResult = []
    startTime = datetime.now()
    # pool = mp.Pool()
    for folder in listOfFolders:
        if counter < 10:
            # result = MyExecutors._instance.CPUExecutor.apply_async(fileReader.readTextFile, (folder,))
            # result = pool.apply_async(fileReader.readTextFile(folder))
            fileReader.readTextFile(folder)
            counter += 1
            # thisRunFolderResult.append(result)
        else:
            for result in thisRunFolderResult:
                result.get()
            thisRunFolderResult = []
            indexer.flushMemory()
            counter = 0
    for result in thisRunFolderResult:
        result.get()
    indexer.flushMemory()



    # MyExecutors._instance.CPUExecutor.close()
    # print("CPU Closed")
    # MyExecutors._instance.CPUExecutor.join()
    # print("CPU Finished")
    # MyExecutors._instance.IOExecutor.close()
    # print("IO Closed")
    # MyExecutors._instance.IOExecutor.join()
    # print("IO Finished")

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

    print ("Number of files Processed: " + str(len(listOfFolders)))
    print(str(timeItTook.seconds) + " seconds")
    # print(str(timeItTook2.seconds) + " seconds after sorting")

    print('***   Done   ***')


def managerRun():
    startTime = datetime.now()

    listOfFolders = os.listdir(config.corpusPath)
    managersNumber = 5
    filesPerIteration = 5
    folderPerManager = int(len(listOfFolders)/managersNumber)
    toStem = False
    managersList = []
    pool = mp.Pool(8)
    for i in range(0,managersNumber):
        start = i * folderPerManager
        end = (i + 1) * folderPerManager
        if end > len(listOfFolders):
            end = len(listOfFolders)

        manager = MyManager(managerID = i, filesPerIteration = filesPerIteration,
                            folderList = listOfFolders[int(start):int(end)],
                            toStem = toStem, indexer = None)
        manager.start(pool)
        managersList.append(manager)

    for i in range(0,managersNumber):
        managersList[i].get()
        print ("Got manager " + str(i))

    finishTime = datetime.now()
    timeItTook = finishTime - startTime

    print ("Number of files Processed: " + str(len(listOfFolders)))
    print(str(timeItTook.seconds) + " seconds")



if __name__ == "__main__":
    main()