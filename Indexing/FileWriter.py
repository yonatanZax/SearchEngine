from AtomicInteger import AtomicCounter
i = AtomicCounter()
def cleanIndex(indexer):
    global i
    currentFileNumber = i.getAndIncrement()
    for dictionaryKey, dictionaryVal in indexer.myDictionaryByLetters.items():
        writeDictionaryToFile(dictionaryKey + str(currentFileNumber), ['term', 'termData'],dictionaryVal)

def writeDictionaryToFile(fileName, headLineAsArray, dictionaryToWrite):
    import os
    import Configuration as config
    import MyExecutors
    dirPath = config.savedFilePath + '\\' + fileName[0]

    if not os.path.exists(dirPath):
        os.mkdir(dirPath)

    path = config.savedFilePath + '\\' + fileName[0] + '\\' + fileName

    fileSeparator = '|'

    # If file doesn't exists, create a new file with headline
    result = None
    if not os.path.exists(path):
        headLineToWrite = fileSeparator.join(headLineAsArray)
        result = MyExecutors._instance.IOExecutor.apply_async(_createFile, (path, headLineToWrite,))


    lineToWrite = ""
    # Iter over all the terms in the dictionary and create a string to write
    dictionaryToWrite.lock.acquire()
    for term, termData in sorted(dictionaryToWrite.dictionary_term_dicData.items()):
        if len(termData.dictionary_docID_tf) > 0:
            lineToWrite += (term + " - " + termData.toString() + "\n")
            # cleans the posting dictionary
            termData.cleanPostingData()

    dictionaryToWrite.lock.release()

    # wait for the file to be created
    result.get()
    # write to the end of the file at one time on another thread
    MyExecutors._instance.IOExecutor.apply_async(_writeToFile, (path,lineToWrite,))



    return True


def _createFile(path, headLineString):
    myFile = open(path, 'w')
    myFile.write(headLineString + "\n")
    myFile.close()

def _writeToFile(path, lineToWrite):
    myFile = open(path, 'a')
    myFile.write(lineToWrite)
    myFile.close()
