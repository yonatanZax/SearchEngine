import os


class FileWriter:

    def __init__(self, config):
        self.counter = 0
        self.config = config

    def cleanIndex(self,indexer):
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

            lineToWrite += (str(docNo) + "|" + documentData.toString() + "\n")


        # write to the end of the file at one time on another thread
        self.writeToFile(path, lineToWrite)



    def writeMergedFile(self,finalList, outputFile):
        from BasicMethods import getStringSizeInBytes

        lineToWritePost = ""

        index = 0
        pathForPosting = outputFile + 'PostingFolder'
        os.mkdir(pathForPosting)
        pathForPosting += '\\'
        currentTerm = ''

        termAppearanceThreshold = self.config.minimumTermAppearanceThreshold
        postingMaxSize = pow(2,20)
        ListToWriteDic = []

        for line in finalList:

            if line[0][2] < termAppearanceThreshold:
                continue

            lastTerm = currentTerm
            currentTerm = line[0][0]

            sortedPostingLine = self.sortPostingLineAndUseGaps(line[1])

            if getStringSizeInBytes(lineToWritePost) + getStringSizeInBytes(line[1]) < postingMaxSize:

                # Dictionary line format: Term|df|sumTf|postingLine
                currentLineDic = '|'.join((line[0][0], str(line[0][1]), str(line[0][2]), str(index)))

                index += 1

                ListToWriteDic.append(currentLineDic)
                lineToWritePost += sortedPostingLine + "\n"


            else:
                if len(lineToWritePost) > 0:
                    self.writeToFile(pathForPosting + lastTerm + '_post', lineToWritePost.rstrip('\n'))

                index = 0


                currentLineDic = '|'.join((line[0][0], str(line[0][1]), str(line[0][2]), str(index)))
                index += 1
                ListToWriteDic.append(currentLineDic)
                lineToWritePost = ''
                lineToWritePost += sortedPostingLine + "\n"




        if len(lineToWritePost) > 0:
            endTermIndex = ListToWriteDic[len(ListToWriteDic) - 1].find('|')
            currentTerm = ListToWriteDic[len(ListToWriteDic) - 1][0:endTermIndex]
            self.writeToFile(pathForPosting + currentTerm + '_post', lineToWritePost.rstrip('\n'))

        lineToWriteDic = '\n'.join(ListToWriteDic)

        self.writeToFile(outputFile + "mergedFile_dic", lineToWriteDic)

        return len(ListToWriteDic)



    @staticmethod
    def sortPostingLineAndUseGaps(lineToSort):
        splitLine = lineToSort.rstrip(',').split(',')
        # TODO - when we move to using number only user a lambda like this: int(item.split('#')[0])
        # Sorting
        twoDListOfPosting = []
        for line in splitLine:
            twoDListOfPosting.append(line.split('#'))
        sorted_twoDListOfPosting = sorted(twoDListOfPosting, key=lambda item: int(item[0]))

        # Change to Gaps
        lastDocumentNumber = 0
        SortedGapedPostingLineList = []
        for document in sorted_twoDListOfPosting:
            gap = int(document[0]) - lastDocumentNumber
            lastDocumentNumber = int(document[0])
            document[0] = str(gap)
            SortedGapedPostingLineList.append('#'.join(document))

        sortedLine = ','.join(SortedGapedPostingLineList)
        return sortedLine


    def writeMergedFileTemp(self,finalList, outputFile):
        lineToWrite = ""
        for line in finalList:
            currentLineDic = '|'.join((line[0][0],str(line[0][1]),str(line[0][2])))

            lineToWrite += currentLineDic + '|' + line[1] + '\n'

        self.writeToFile(outputFile, lineToWrite)

    def createFile(self,path, headLineString):
        myFile = open(path, 'w', encoding='utf-8')
        myFile.write(headLineString + "\n")
        myFile.close()

    def writeToFile(self,path, lineToWrite):
        myFile = open(path, 'a', encoding='utf-8')
        myFile.write(lineToWrite)
        myFile.close()



