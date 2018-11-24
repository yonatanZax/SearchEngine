

# ********************  Configurations File  ********************

import os
projectMainFolder = os.path.dirname(os.path.abspath(__file__)) + '\\'



corpusPath = projectMainFolder + 'corpus'
savedFilePath = projectMainFolder + 'SavedFiles'
documentsIndex = savedFilePath + '/docIndex'

managersNumber = 4
filesPerIteration = 10
listOfFoldersLength = len(os.listdir(corpusPath))

# TODO - add stop words path to the corpus path

# TODO - add functions to change the configurations

# Todo - add with/without stem