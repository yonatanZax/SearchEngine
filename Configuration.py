

# ********************  Configurations File  ********************

import os
projectMainFolder = os.path.dirname(os.path.abspath(__file__)) + '\\'

print ("Configurations")

corpusPath = projectMainFolder + 'corpus'
savedFilePath = projectMainFolder + 'SavedFiles'
documentsIndexPath = savedFilePath + '/docIndex'
stopWordFile = 'stop_words.txt'
stopWordPath = corpusPath + '/' + stopWordFile

managersNumber = os.cpu_count()
filesPerIteration = 10
listOfFoldersLength = len(os.listdir(corpusPath))

toStem = False


# TODO (DONE) - add stop words path to the corpus path

# TODO (DONE) - add functions to change the configurations

def setCorpusPath(newPath):
    global corpusPath,stopWordPath,listOfFoldersLength
    corpusPath = newPath
    stopWordPath = corpusPath + '/'
    listOfFoldersLength = len(os.listdir(corpusPath))
    print('corpus path changed')

def setSavedFilePath(newPath):
    global savedFilePath
    savedFilePath = newPath
    setDocumentsIndex(savedFilePath)

def setDocumentsIndex(savedFilePath):
    global documentsIndexPath
    documentsIndexPath = savedFilePath + '/docIndex'

def setToStem(bool):
    global toStem
    toStem = bool


# Todo - add with/without stem