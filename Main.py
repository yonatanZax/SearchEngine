
import os
from datetime import datetime
from Manager import MyManager
from concurrent.futures import ProcessPoolExecutor
from Configuration import ConfigClass


config = None

def main():

    mainManager = MainClass()
    mainManager.GUIRun()

    # managerRun()


class MainClass:

    def __init__(self):

        self.config = ConfigClass()

    def GUIRun(self):
        import GuiExample

        print("***   Main Start   ***")
        root = GuiExample.Tk()
        root.geometry('500x550')
        root.title("SearchEngine")

        guiFrame = GuiExample.EngineBuilder(root,mainManager=self, config=self.config, numOfTotalFiles=self.config.get__listOfFoldersLength())
        guiFrame.mainloop()

    def managerRun(self):
        import string
        startTime = datetime.now()
        managersNumber = self.config.get__managersNumber()
        filesPerIteration = self.config.get__filesPerIteration()
        listOfFolders = os.listdir(self.config.get__corpusPath())
        listOfFolders.remove(self.config.get__stopWordFile())

        folderPerManager = int(len(listOfFolders) / managersNumber) + 1
        lettersList = list(string.ascii_lowercase)
        lettersList.append('#')

        lettersPerManager = int(len(lettersList) / managersNumber) + 1
        toStem = self.config.get__toStem()
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


            folderListPerManager = []
            for j in range(i,len(listOfFolders),managersNumber):
                folderListPerManager.append(listOfFolders[j])


            manager = MyManager(managerID=i, filesPerIteration=filesPerIteration,
                                folderList=folderListPerManager,
                                lettersList=lettersList[int(startLetters):int(endLetters)], config=self.config, indexer=None)
            managersList.append(manager)

        for manager in zip(managersList, pool.map(self.run, managersList)):
            manager[0].getRun()

        finishTime = datetime.now()
        timeItTook = finishTime - startTime

        print("Term Posting took: " + str(timeItTook.seconds) + " seconds")

        for manager in zip(managersList, pool.map(self.managerMerge, managersList)):
            manager[0].getMerge()

        # Indexer.staticMerge()

        finishTime = datetime.now()
        timeItTook = finishTime - startTime

        print("Number of files Processed: " + str(len(listOfFolders)))
        print("Everything took: " + str(timeItTook.seconds) + " seconds")

    def run(self,manager):
        manager.run()

    def managerMerge(self,manager):
        manager.merge()


if __name__ == "__main__":
    main()