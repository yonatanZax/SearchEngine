
import os
import Configuration as config
from datetime import datetime
from Manager import MyManager
from concurrent.futures import ProcessPoolExecutor
from Indexing.Indexer import Indexer

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
    initProject()

    # GUIRun()

    managerRun()

def GUIRun():
    import GuiExample
    print("***   Main Start   ***")
    root = GuiExample.Tk()
    root.geometry('500x550')
    root.title("SearchEngine")

    guiFrame = GuiExample.EngineBuilder(root,numOfManagers=config.managersNumber, numOfTotalFiles=config.listOfFoldersLength)
    guiFrame.mainloop()


def managerRun():
    import string
    startTime = datetime.now()
    managersNumber = config.managersNumber
    filesPerIteration = config.filesPerIteration
    listOfFolders = os.listdir(config.corpusPath)
    listOfFolders.remove(config.stopWordFile)

    folderPerManager = int(len(listOfFolders)/managersNumber) + 1
    lettersList = list(string.ascii_lowercase)
    lettersList.append('#')

    lettersPerManager = int(len(lettersList)/managersNumber) + 1
    toStem = config.toStem
    managersList = []
    pool = ProcessPoolExecutor()
    for i in range(0, managersNumber):
        startFolder = i * folderPerManager
        endFolder = (i + 1) * folderPerManager
        if endFolder > len(listOfFolders):
            endFolder = len(listOfFolders)

        startLetters = i * lettersPerManager
        endLetters = (i + 1) * lettersPerManager
        if endLetters > len(lettersList):
            endLetters = len(lettersList)

        manager = MyManager(managerID = i, filesPerIteration = filesPerIteration,
                            folderList = listOfFolders[int(startFolder):int(endFolder)],
                            lettersList = lettersList[int(startLetters):int(endLetters)], toStem = toStem, indexer = None)
        managersList.append(manager)



    for manager in zip(managersList, pool.map(run, managersList)):
        manager[0].getRun()

    finishTime = datetime.now()
    timeItTook = finishTime - startTime

    print("Term Posting took: " + str(timeItTook.seconds) + " seconds")

    for manager in zip(managersList, pool.map(managerMerge, managersList)):
        manager[0].getMerge()

    # Indexer.staticMerge()


    finishTime = datetime.now()
    timeItTook = finishTime - startTime

    print ("Number of files Processed: " + str(len(listOfFolders)))
    print("Everything took: " + str(timeItTook.seconds) + " seconds")

def run(manager):
    manager.run()

def managerMerge(manager):
    manager.merge(config.managersNumber)



if __name__ == "__main__":
    main()