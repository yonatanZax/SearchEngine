import os
import Configuration as config

i = 0
def cleanIndex(indexer):
    global i
    # currentFileNumber = i.getAndIncrement()
    currentFileNumber = i
    i += 1
    headLineToWrite = 'term|DF|sumTF|DOC#TF#Position:*,*'
    for dictionaryKey, dictionaryVal in indexer.myDictionaryByLetters.items():
        writeDictionaryToFile(dictionaryKey + str(indexer.ID) + "_" + str(currentFileNumber), headLineToWrite,dictionaryVal)

def writeDictionaryToFile(fileName, headLineToWrite, dictionaryToWrite):

    dirPath = config.savedFilePath + '\\' + fileName[0]

    if not os.path.exists(dirPath):
        os.mkdir(dirPath)

    path = config.savedFilePath + '\\' + fileName[0] + '\\' + fileName

    lineToWrite = ""
    # Iter over all the terms in the dictionary and create a string to write
    for term, termData in sorted(dictionaryToWrite.dictionary_term_dicData.items()):
        if len(termData.string_docID_tf) > 0:
            lineToWrite += term + "|" + termData.toString() + "\n"
            # cleans the posting dictionary
            termData.cleanPostingData()


    # write to the end of the file at one time on another thread
    if len(lineToWrite) > 0:
        _writeToFile(path, lineToWrite)


def cleanDocuments(dictionaryToWrite):
    path = config.documentsIndexPath
    if not os.path.exists(path):
        headLineToWrite = 'DOCID|max_tf|uniqueTermCount|docLength|city'
        _createFile(path, headLineToWrite)

    lineToWrite = ""
    for docNo, documentData in sorted(dictionaryToWrite.items()):
        lineToWrite += (docNo + "|" + documentData.toString() + "\n")

    # write to the end of the file at one time on another thread
    _writeToFile(path, lineToWrite)

# TODO - make sure that if we use stem we won't run over not stemmed files
# TODO - change path to relative and add the stem and file name to the method signature

def writeMergedFile(finalList, outputFile):
    lineToWritePost = ""
    lineToWriteDic = ""
    index = 0
    pathForPosting = outputFile + 'PostingFolder'
    os.mkdir(pathForPosting)
    pathForPosting += '\\'
    for line in finalList:
        if index < 999:
            lineToWriteDic += line[0] + '|' + str(index) +'\n'
            lineToWritePost += line[1] + "\n"
            index += 1
        else:
            lineToWriteDic += line[0] + '|' + str(index) +'\n'
            lineToWritePost += line[1] + "\n"
            index = 0

            endTermIndex = line[0].find('|')
            lastTerm = line[0][0:endTermIndex]

            _writeToFile(pathForPosting + lastTerm + '_post', lineToWritePost)
            lineToWritePost = ''

    if index != 0:
        endTermIndex = finalList[len(finalList)-1][0].find('|')
        lastTerm = finalList[len(finalList)-1][0][0:endTermIndex]
        _writeToFile(pathForPosting + lastTerm + '_post', lineToWritePost)

    _writeToFile(outputFile + "mergedFile_dic", lineToWriteDic)

def writeMergedFileTemp(finalList, outputFile):
    lineToWrite = ""
    for line in finalList:
        lineToWrite += line[0] + '|' + line[1] + '\n'
    _writeToFile(outputFile, lineToWrite)


def _createFile(path, headLineString):
    myFile = open(path, 'w')
    myFile.write(headLineString + "\n")
    myFile.close()

def _writeToFile(path, lineToWrite):
    myFile = open(path, 'a')
    myFile.write(lineToWrite)
    myFile.close()
