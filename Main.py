
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

    GUIRun()

    # managerRun()

def GUIRun():
    import GuiExample
    print("***   Main Start   ***")
    root = GuiExample.Tk()
    root.geometry('500x550')
    root.title("SearchEngine")

    guiFrame = GuiExample.EngineBuilder(root,numOfManagers=config.managersNumber, numOfTotalFiles=config.listOfFoldersLength)
    guiFrame.mainloop()


def managerRun():
    startTime = datetime.now()
    managersNumber = config.managersNumber
    filesPerIteration = config.filesPerIteration
    listOfFolders = os.listdir(config.corpusPath)
    listOfFolders.remove(config.stopWordFile)
    folderPerManager = int(len(listOfFolders)/managersNumber) + 1
    toStem = False
    managersList = []
    pool = ProcessPoolExecutor()
    for i in range(0, managersNumber):
        start = i * folderPerManager
        end = (i + 1) * folderPerManager
        if end > len(listOfFolders):
            end = len(listOfFolders)
        manager = MyManager(managerID = i, filesPerIteration = filesPerIteration,
                            folderList = listOfFolders[int(start):int(end)],
                            toStem = toStem, indexer = None)
        managersList.append(manager)



    for manager in zip(managersList, pool.map(run, managersList)):
        manager[0].get()

    Indexer.merge()


    finishTime = datetime.now()
    timeItTook = finishTime - startTime

    print ("Number of files Processed: " + str(len(listOfFolders)))
    print("Everything took: " + str(timeItTook.seconds) + " seconds")

def run(manager):
    manager.run()


if __name__ == "__main__":
    main()