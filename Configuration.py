

# ********************  Configurations File  ********************
import os
import shutil
import string


class ConfigClass:

    def __init__(self):

        self.corpusPath = ''
        self.savedFileMainFolder = ''
        self.saveFilesWithStem = self.savedFileMainFolder + "/WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "/WithoutStem"
        self.stopWordFile = 'stop_words.txt'
        self.toStem = False

        # Todo - remove before submit
        # self.corpusPath = 'D:/corpus - full'
        self.corpusPath = 'D:/corpus'
        self.savedFileMainFolder = '..'
        # self.corpusPath = 'C:/Users/doroy/Documents/סמסטר ה/אחזור מידע/עבודה/corpus'
        # self.savedFileMainFolder = 'C:/Users/doroy/Documents/סמסטר ה/אחזור מידע/עבודה/SavedFiles'


        # self.corpusPath = '../corpus'
        # self.savedFileMainFolder = '../SavedFiles'
        # if not os.path.exists(self.savedFileMainFolder):
        #     os.mkdir(self.savedFileMainFolder)
        # self.setSaveMainFolderPath(self.savedFileMainFolder)
        # self.savedFilePath = self.saveFilesWithoutStem + '/SavedFiles'
        #
        # self.stopWordPath = self.corpusPath + "/" + self.stopWordFile
        # self.listOfFoldersLength = len(os.listdir(self.corpusPath))
        # self.documentsIndexPath = self.savedFilePath + '/docIndex'






        self.managersNumber = os.cpu_count()
        if self.managersNumber == 1:
            self.managersNumber = 4
        self.filesPerIteration = 10

        # Minimum SumTf
        self.minimumTermAppearanceThreshold = 4

        self.toStem = False



        # Part B

        # Best Values - 189
        self.BM25_K = 1.5
        self.BM25_B = 0.7

        # Best - 188
        # self.Axu_Value = 6
        self.Axu_Value = 10

        # self.Axu_Value = 6
        # self.BM25_K = 1.2
        # self.BM25_B = 0.75


        self.BM25_avgDLength = 100
        self.totalNumberOfDocs = 1000
        self.totalNumberOfTerms = 1000


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


    def setAverageDocLength(self, totalLength:float, numberOfDocs:int) :
        self.BM25_avgDLength = totalLength / numberOfDocs
        self.totalNumberOfDocs = numberOfDocs

    def setTotalNumberOfTerms(self, numNoStem:int, numWithStem:int):
        self.totalNumberOfTermsNoStem = numNoStem
        self.totalNumberOfTermsWithStem = numWithStem

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

    def get__documentIndexPathStem(self):
        return self.saveFilesWithStem + '/docIndex'

    def get__documentIndexPathWithoutStem(self):
        return self.saveFilesWithoutStem + '/docIndex'

    def get__cityIndexPathStem(self):
        return self.saveFilesWithStem + '/cityIndex'

    def get__cityIndexPathWithoutStem(self):
        return self.saveFilesWithoutStem + '/cityIndex'

    def get__savedFilePath(self):
        return self.savedFilePath

    def get__toStem(self):
        return self.toStem

    def get_numOfFiles(self):
        import os
        if os.path.exists(self.corpusPath):
            return len(os.listdir(self.corpusPath)) - 1

