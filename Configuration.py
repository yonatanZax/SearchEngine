

# ********************  Configurations File  ********************
import os
import shutil
import string


class ConfigClass:

    def __init__(self):

        self.corpusPath = ''
        self.savedFileMainFolder = ''

        self.stopWordFile = 'stop_words.txt'

        self.managersNumber = os.cpu_count()
        if self.managersNumber == 1:
            self.managersNumber = 4
        self.filesPerIteration = 10
        self.minimumTermAppearanceThreshold = 2

        self.toStem = False

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




    def setSaveMainFolderPath(self,newPath,delete=False):
        if not os.path.exists(newPath):
            os.mkdir(newPath)
        self.savedFileMainFolder = newPath
        self.saveFilesWithStem = self.savedFileMainFolder + "/WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "/WithoutStem"

        if not self.toStem:
            # Build code
            if delete:
                if os.path.exists(self.saveFilesWithoutStem):
                    shutil.rmtree(self.saveFilesWithoutStem)
                os.mkdir(self.saveFilesWithoutStem)
                self.savedFilePath = self.saveFilesWithoutStem

            elif not delete:
                if not os.path.exists(self.saveFilesWithoutStem):
                    os.mkdir(self.saveFilesWithoutStem)
                self.savedFilePath = self.saveFilesWithoutStem


        else:
            # Build code
            if delete:
                if os.path.exists(self.saveFilesWithStem):
                    shutil.rmtree(self.saveFilesWithStem)
                os.mkdir(self.saveFilesWithStem)
                self.savedFilePath = self.saveFilesWithStem



            elif not delete:
                if not os.path.exists(self.saveFilesWithStem):
                    os.mkdir(self.saveFilesWithStem)
                self.savedFilePath = self.saveFilesWithStem

        if delete:
            lettersList = list(string.ascii_lowercase)
            lettersList.append('#')
            for letter in lettersList:
                os.mkdir(self.savedFilePath + '/' + letter)


        self.setSavedFilePath(self.savedFilePath)
        if not os.path.exists(self.savedFilePath + '/Progress'):
            os.mkdir(self.savedFilePath + '/Progress')
            os.mkdir(self.savedFilePath + '/Progress/Posting')
            os.mkdir(self.savedFilePath + '/Progress/Merge')



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

    def get_numOfFiles(self):
        import os
        if os.path.exists(self.corpusPath):
            return len(os.listdir(self.corpusPath)) - 1

