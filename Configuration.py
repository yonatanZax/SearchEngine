

# ********************  Configurations File  ********************
import os
import shutil



class ConfigClass:


    def __init__(self):
        projectMainFolder = os.path.dirname(os.path.abspath(__file__)) + '\\'
        self.corpusPath = projectMainFolder + 'corpus'
        self.savedFileMainFolder = projectMainFolder + 'SavedFiles'
        self.saveFilesWithStem = self.savedFileMainFolder + "\\WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "\\WithoutStem"

        # if os.path.exists(self.savedFileMainFolder):
        #     shutil.rmtree(self.savedFileMainFolder)
        # while 1:
        #     try:
        #         os.mkdir(self.savedFileMainFolder)
        #         break
        #     except PermissionError:
        #         continue

        self.stopWordFile = 'stop_words.txt'
        self.stopWordPath = self.corpusPath + '/' + self.stopWordFile

        self.managersNumber = os.cpu_count()
        # self.managersNumber = 1
        self.filesPerIteration = 10
        self.listOfFoldersLength = len(os.listdir(self.corpusPath))

        self.toStem = False
        if not self.toStem:
            self.savedFilePath = self.saveFilesWithoutStem
        else:
            self.savedFilePath = self.saveFilesWithStem

        self.documentsIndexPath = self.savedFilePath + '/docIndex'

        print('Project was created successfully..')





    def setCorpusPath(self,newPath):
        self.corpusPath = newPath
        self.stopWordPath = self.corpusPath + "/" + self.stopWordFile
        self.listOfFoldersLength = len(os.listdir(self.corpusPath))
        print('corpus path changed')


    def setSavedFilePath(self,newPath):
        self.savedFilePath = newPath
        self.setDocumentsIndex(self.savedFilePath)

    def setDocumentsIndex(self,savedFilePath):
        self.documentsIndexPath = savedFilePath + '/docIndex'


    def setSaveMainFolderPath(self,newPath):
        if not os.path.exists(newPath):
            os.mkdir(newPath)
        self.savedFileMainFolder = newPath
        self.saveFilesWithStem = self.savedFileMainFolder + "\\WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "\\WithoutStem"

        if not self.toStem:
            if os.path.exists(self.saveFilesWithoutStem):
                shutil.rmtree(self.saveFilesWithoutStem)
            os.mkdir(self.saveFilesWithoutStem)
            if not os.path.exists(self.saveFilesWithoutStem):
                os.mkdir(self.saveFilesWithoutStem)
            self.savedFilePath = self.saveFilesWithoutStem
        else:
            if os.path.exists(self.saveFilesWithStem):
                shutil.rmtree(self.saveFilesWithStem)
            os.mkdir(self.saveFilesWithStem)
            if not os.path.exists(self.saveFilesWithStem):
                os.mkdir(self.saveFilesWithStem)
            self.savedFilePath = self.saveFilesWithStem

        self.setSavedFilePath(self.savedFilePath)


    def setToStem(self,bool):
        self.toStem = bool
        print('Stem changed to: ',bool)
        if not self.toStem:
            self.savedFilePath = self.saveFilesWithoutStem
        else:
            self.savedFilePath = self.saveFilesWithStem

            self.setSavedFilePath(self.savedFilePath)


    def getSavedFilesPath(self):
        return self.savedFilePath


    def get__savedFileMainFolder(self):
        return self.savedFileMainFolder

    def get__corpusPath(self):
        return self.corpusPath

    def get__saveFilesWithStem(self):
        return self.saveFilesWithStem

    def get__saveFilesWithoutStem(self):
        return self.saveFilesWithoutStem

    def get__stopWordFile(self):
        return self.stopWordFile

    def get__stopWordPath(self):
        return self.stopWordPath

    def get__managersNumber(self):
        return self.managersNumber

    def get__filesPerIteration(self):
        return self.filesPerIteration

    def get__listOfFoldersLength(self):
        return self.listOfFoldersLength


    def get__documentsIndexPath(self):
        return self.documentsIndexPath

    def get__savedFilePath(self):
        return self.savedFilePath

    def get__toStem(self):
        return self.toStem


