import os


class FileWriter:

    def __init__(self, config):
        self.counter = 0
        self.config = config

    def cleanIndex(self,indexer):
        # currentFileNumber = i.getAndIncrement()
        currentFileNumber = self.counter
        self.counter += 1
        # headLineToWrite = 'term|DF|sumTF|DOC#TF#Position:*,*'
        for dictionaryKey, dictionaryVal in indexer.myDictionaryByLetters.items():
            self.writeDictionaryToFile(dictionaryKey + str(indexer.ID) + "_" + str(currentFileNumber),dictionaryVal)

    def writeDictionaryToFile(self,fileName, dictionaryToWrite):



        path = self.config.savedFilePath + '\\' + fileName[0] + '\\' + fileName

        lineToWrite = ""
        # Iter over all the terms in the dictionary and create a string to write
        for term, termData in sorted(dictionaryToWrite.dictionary_term_dicData.items()):
            if len(termData.string_docID_tf_positions) > 0:
                lineToWrite += term + "|" + termData.toString() + "\n"
                # cleans the posting dictionary
                termData.cleanPostingData()

        # write to the end of the file at one time on another thread
        if len(lineToWrite) > 0:
            self.writeToFile(path, lineToWrite)

    def cleanDocuments(self,dictionaryToWrite):
        path = self.config.documentsIndexPath
        if not os.path.exists(path):
            headLineToWrite = 'DOCID|max_tf|uniqueTermCount|docLength|City|Language'
            self.createFile(path, headLineToWrite)

        lineToWrite = ""
        for docNo, documentData in sorted(dictionaryToWrite.items()):
            lineToWrite += (docNo + "|" + documentData.toString() + "\n")

        # write to the end of the file at one time on another thread
        self.writeToFile(path, lineToWrite)



    def writeMergedFile(self,finalList, outputFile):
        lineToWritePost = ""
        lineToWriteDic = ""
        index = 0
        pathForPosting = outputFile + 'PostingFolder'
        os.mkdir(pathForPosting)
        pathForPosting += '\\'

        termAppearanceThreshold = self.config.minimumTermAppearanceThreshold
        ListToWriteDic = []

        for line in finalList:

            if line[0][2] < termAppearanceThreshold:
                continue

            currentLineDic = '|'.join((line[0][0],str(line[0][1]),str(line[0][2]),str(index)))

            if index < 999:
                # lineToWriteDic += currentLineDic + '\n'
                ListToWriteDic.append(currentLineDic)
                lineToWritePost += line[1] + "\n"
                index += 1
            else:
                # lineToWriteDic += currentLineDic + '\n'
                ListToWriteDic.append(currentLineDic)

                lineToWritePost += line[1] + "\n"
                index = 0

                # endTermIndex = line[0].find('|')
                # lastTerm = line[0][0:endTermIndex]
                lastTerm = line[0][0]

                self.writeToFile(pathForPosting + lastTerm + '_post', lineToWritePost)
                lineToWritePost = ''

        if index != 0:
            # endTermIndex = finalList[len(finalList) - 1][0].find('|')
            endTermIndex = ListToWriteDic[len(ListToWriteDic) - 1].find('|')
            # lastTerm = finalList[len(finalList) - 1][0][0:endTermIndex]
            lastTerm = ListToWriteDic[len(ListToWriteDic) - 1][0:endTermIndex]
            self.writeToFile(pathForPosting + lastTerm + '_post', lineToWritePost)

        lineToWriteDic = '\n'.join(ListToWriteDic)

        self.writeToFile(outputFile + "mergedFile_dic", lineToWriteDic)

        return len(ListToWriteDic)

    def writeMergedFileTemp(self,finalList, outputFile):
        lineToWrite = ""
        for line in finalList:
            currentLineDic = '|'.join((line[0][0],str(line[0][1]),str(line[0][2])))

            lineToWrite += currentLineDic + '|' + line[1] + '\n'

        self.writeToFile(outputFile, lineToWrite)

    def createFile(self,path, headLineString):
        myFile = open(path, 'w')
        myFile.write(headLineString + "\n")
        myFile.close()

    def writeToFile(self,path, lineToWrite):
        myFile = open(path, 'a')
        myFile.write(lineToWrite)
        myFile.close()



