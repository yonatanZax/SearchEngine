

# ********************  Configurations File  ********************

import os
projectMainFolder = os.path.dirname(os.path.abspath(__file__)) + '\\'



corpusPath = projectMainFolder + 'corpus'
savedFilePath = projectMainFolder + 'SavedFiles'
documentsIndex = savedFilePath + '/docIndex'

managersNumber = 4
filesPerIteration = 10
listOfFoldersLength = len(os.listdir(corpusPath))

