i = 0
def cleanIndex(indexer):
    global i
    i += 1
    for dictionaryKey, dictionaryVal in indexer.myDictionaryByLetters.items():
        writeDictionaryToFile(dictionaryKey + str(i), ['term', 'termData'],dictionaryVal)

def writeDictionaryToFile(fileName, headLineAsArray, dictionaryToWrite):
    import os
    import Configuration as config
    path = config.savedFilePath + '\\' + fileName

    fileSeparator = '|'


    try:
        # If file dosen't exists, create a new file with headline
        if not os.path.exists(path):
            headLineToWrite = fileSeparator.join(headLineAsArray)
            myFile = open(path, 'w')
            myFile.write(headLineToWrite + "\n")
            myFile.close()


        # Add line at the end of the file
        myFile = open(path, 'a')





        # Iter over all the terms in the dictionary and store to file
        for term, termData in sorted(dictionaryToWrite.dictionary_term_dicData.items()):
            lineToWrite = (term + " - " + termData.toString())
            myFile.write(lineToWrite + "\n")



        myFile.close()

    except IOError:
        with myFile:
            print("Error while writing new line to path:    ", path)
            myFile.close()
            return False

    return True

