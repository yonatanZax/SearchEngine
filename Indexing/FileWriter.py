import os


class FileWriter:

    def __init__(self, config):
        self.i = 0
        self.config = config

    def cleanIndex(self,indexer):
        # currentFileNumber = i.getAndIncrement()
        currentFileNumber = self.i
        self.i += 1
        headLineToWrite = 'term|DF|sumTF|DOC#TF#Position:*,*'
        for dictionaryKey, dictionaryVal in indexer.myDictionaryByLetters.items():
            self.writeDictionaryToFile(dictionaryKey + str(indexer.ID) + "_" + str(currentFileNumber), headLineToWrite,
                                  dictionaryVal)

    def writeDictionaryToFile(self,fileName, headLineToWrite, dictionaryToWrite):

        dirPath = self.config.savedFilePath + '\\' + fileName[0]

        if not os.path.exists(dirPath):
            os.mkdir(dirPath)

        path = self.config.savedFilePath + '\\' + fileName[0] + '\\' + fileName

        lineToWrite = ""
        # Iter over all the terms in the dictionary and create a string to write
        for term, termData in sorted(dictionaryToWrite.dictionary_term_dicData.items()):
            if len(termData.string_docID_tf) > 0:
                lineToWrite += term + "|" + termData.toString() + "\n"
                # cleans the posting dictionary
                termData.cleanPostingData()

        # write to the end of the file at one time on another thread
        if len(lineToWrite) > 0:
            self.writeToFile(path, lineToWrite)

    def cleanDocuments(self,dictionaryToWrite):
        path = self.config.documentsIndexPath
        if not os.path.exists(path):
            headLineToWrite = 'DOCID|max_tf|uniqueTermCount|docLength|city'
            self.createFile(path, headLineToWrite)

        lineToWrite = ""
        for docNo, documentData in sorted(dictionaryToWrite.items()):
            lineToWrite += (docNo + "|" + documentData.toString() + "\n")

        # write to the end of the file at one time on another thread
        self.writeToFile(path, lineToWrite)

    # TODO (DONE) - make sure that if we use stem we won't run over not stemmed files
    # TODO (DONE) - change path to relative and add the stem and file name to the method signature

    def writeMergedFile(self,finalList, outputFile):
        lineToWritePost = ""
        lineToWriteDic = ""
        index = 0
        pathForPosting = outputFile + 'PostingFolder'
        os.mkdir(pathForPosting)
        pathForPosting += '\\'
        for line in finalList:
            if index < 999:
                lineToWriteDic += line[0] + '|' + str(index) + '\n'
                lineToWritePost += line[1] + "\n"
                index += 1
            else:
                lineToWriteDic += line[0] + '|' + str(index) + '\n'
                lineToWritePost += line[1] + "\n"
                index = 0

                endTermIndex = line[0].find('|')
                lastTerm = line[0][0:endTermIndex]

                self.writeToFile(pathForPosting + lastTerm + '_post', lineToWritePost)
                lineToWritePost = ''

        if index != 0:
            endTermIndex = finalList[len(finalList) - 1][0].find('|')
            lastTerm = finalList[len(finalList) - 1][0][0:endTermIndex]
            self.writeToFile(pathForPosting + lastTerm + '_post', lineToWritePost)

        self.writeToFile(outputFile + "mergedFile_dic", lineToWriteDic)

    def writeMergedFileTemp(self,finalList, outputFile):
        lineToWrite = ""
        for line in finalList:
            lineToWrite += line[0] + '|' + line[1] + '\n'
        self.writeToFile(outputFile, lineToWrite)

    def createFile(self,path, headLineString):
        myFile = open(path, 'w')
        myFile.write(headLineString + "\n")
        myFile.close()

    def writeToFile(self,path, lineToWrite):
        myFile = open(path, 'a')
        myFile.write(lineToWrite)
        myFile.close()



