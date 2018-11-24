from AtomicInteger import AtomicCounter
import os
import Configuration as config
import MyExecutors

i = AtomicCounter()
x = 0
def cleanIndex(indexer):
    global i , x
    # currentFileNumber = i.getAndIncrement()
    currentFileNumber = x
    x += 1
    headLineToWrite = 'term|DF|sumTF|DOC#TF,*'
    for dictionaryKey, dictionaryVal in indexer.myDictionaryByLetters.items():
        writeDictionaryToFile(dictionaryKey + str(indexer.ID) + "_" + str(currentFileNumber), headLineToWrite,dictionaryVal)

def writeDictionaryToFile(fileName, headLineToWrite, dictionaryToWrite):

    dirPath = config.savedFilePath + '\\' + fileName[0]

    if not os.path.exists(dirPath):
        os.mkdir(dirPath)

    path = config.savedFilePath + '\\' + fileName[0] + '\\' + fileName

    # If file doesn't exists, create a new file with headline
    result = None
    if not os.path.exists(path):
        result = MyExecutors._instance.IOExecutor.apply_async(_createFile, (path, headLineToWrite,))

    lineToWrite = ""
    # Iter over all the terms in the dictionary and create a string to write
    for term, termData in sorted(dictionaryToWrite.dictionary_term_dicData.items()):
        if len(termData.string_docID_tf) > 0:
            lineToWrite += (term + "|" + termData.toString() + "\n")
            # cleans the posting dictionary
            termData.cleanPostingData()


    # wait for the file to be created
    if result is not None:
        result.get()

    # write to the end of the file at one time on another thread
    MyExecutors._instance.IOExecutor.apply_async(_writeToFile, (path,lineToWrite,))

def cleanDocuments(dictionaryToWrite):
    path = config.documentsIndex
    result = None
    if not os.path.exists(path):
        headLineToWrite = 'term|max_tf|uniqueTermCount|docLength|city'
        result = MyExecutors._instance.IOExecutor.apply_async(_createFile, (path, headLineToWrite,))
        _createFile(path, headLineToWrite)

    lineToWrite = ""
    for docNo, documentData in sorted(dictionaryToWrite.items()):
        lineToWrite += (docNo + "|" + documentData.toString() + "\n")

    # wait for the file to be created
    if result is not None:
        result.get()

    # write to the end of the file at one time on another thread
    MyExecutors._instance.IOExecutor.apply_async(_writeToFile, (path,lineToWrite,))

# TODO - make sure that if we use stem we won't run over not stemmed files
# TODO - change path to relative and add the stem and file name to the method signature

def writeMergedFile(finalList, outputFile):
    lineToWrite = ""
    for line in finalList:
        lineToWrite += line + "\n"
    _writeToFile(outputFile,lineToWrite)


def _createFile(path, headLineString):
    myFile = open(path, 'w')
    # myFile.write(headLineString + "\n")
    myFile.close()

def _writeToFile(path, lineToWrite):
    myFile = open(path, 'a')
    myFile.write(lineToWrite)
    myFile.close()
