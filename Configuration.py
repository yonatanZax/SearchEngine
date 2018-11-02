

# ********************  Configurations File  ********************

import os
projectMainFolder = os.path.dirname(os.path.abspath(__file__)) + '\\'

# Returns an array: [folder path, file type(.csv , .txt)]
def getAbsolutePathToDataFolderAndFileType(dataType):

    return {

        'corpus': projectMainFolder + 'corpus',

    }[dataType]





