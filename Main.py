
import os
import Configuration as config
from Indexing.Indexer import Indexer
from ReadFiles.ReadFile import ReadFile
from datetime import datetime
import MyExecutors


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
    # testRun()
    regularRun()

def testRun():
    indexer = Indexer()
    fileReader = ReadFile(indexer, config.corpusPath)
    # try:
    # fileReader.readAllFiles()
    listOfFolders = os.listdir(config.corpusPath)
    counter = 0
    startTime = datetime.now()
    folder = listOfFolders[0]
    result0 = MyExecutors._instance.CPUExecutor.apply_async(fileReader.readTextFile, (listOfFolders[0],))
    result1 = MyExecutors._instance.CPUExecutor.apply_async(fileReader.readTextFile, (listOfFolders[1],))
    # result2 = MyExecutors._instance.CPUExecutor.apply_async(fileReader.readTextFile, (listOfFolders[2],))
    # result3 = MyExecutors._instance.CPUExecutor.apply_async(fileReader.readTextFile, (listOfFolders[3],))
    # result4 = MyExecutors._instance.CPUExecutor.apply_async(fileReader.readTextFile, (listOfFolders[4],))
    # result5 = MyExecutors._instance.CPUExecutor.apply_async(fileReader.readTextFile, (listOfFolders[5],))
    # result6 = MyExecutors._instance.CPUExecutor.apply_async(fileReader.readTextFile, (listOfFolders[6],))
    # result7 = MyExecutors._instance.CPUExecutor.apply_async(fileReader.readTextFile, (listOfFolders[7],))
    # result8 = MyExecutors._instance.CPUExecutor.apply_async(fileReader.readTextFile, (listOfFolders[8],))
    # result9 = MyExecutors._instance.CPUExecutor.apply_async(fileReader.readTextFile, (listOfFolders[9],))

    result0.get(10)
    print ("0 has finished")
    result1.get(10)
    print ("1 has finished")

    # result2.wait()
    # print ("2 has finished")
    #
    # result3.wait()
    # print ("3 has finished")
    #
    # result4.wait()
    # print ("4 has finished")
    #
    # result5.wait()
    # print ("5 has finished")
    #
    # result6.wait()
    # print ("6 has finished")
    #
    # result7.wait()
    # print ("7 has finished")
    #
    # result8.wait()
    # print ("8 has finished")
    #
    # result9.wait()
    # print ("9 has finished")


    indexer.flushMemory()

    MyExecutors._instance.CPUExecutor.close()
    print("CPU Closed")
    MyExecutors._instance.CPUExecutor.join()
    print("CPU Finished")
    MyExecutors._instance.IOExecutor.close()
    print("IO Closed")
    MyExecutors._instance.IOExecutor.join()
    print("IO Finished")

    finishTime = datetime.now()
    timeItTook = finishTime - startTime

    print(str(timeItTook.seconds) + " seconds")
    # print(str(timeItTook2.seconds) + " seconds after sorting")

    print('***   Done   ***')


def regularRun():
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
            thisRunFolderResult = []
            indexer.flushMemory()
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
    MyExecutors._instance.CPUExecutor.close()
    print("CPU Closed")
    MyExecutors._instance.CPUExecutor.join()
    print("CPU Finished")
    MyExecutors._instance.IOExecutor.close()
    print("IO Closed")
    MyExecutors._instance.IOExecutor.join()
    print("IO Finished")

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

    print(str(timeItTook.seconds) + " seconds")
    # print(str(timeItTook2.seconds) + " seconds after sorting")

    print('***   Done   ***')


if __name__ == "__main__":
    main()