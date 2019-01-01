import os
from Indexing.MyDictionary import MyDictionary, DocumentIndexData,CityIndexData
import string
from Indexing.FileWriter import FileWriter
from Indexing.KWayMerge import MyHeap
import BasicMethods as basic

class TopList():
    # This data structure keeps the top N values

    def __init__(self,size):
        self.myList = []
        for i in range(0,size):
            self.myList.append((0,''))


    def _getMinValue(self):
        # find min
        minValue = min([value for value in self.myList])
        self.myList.remove(minValue)
        return minValue

    def _getMaxValue(self):
        # find max
        minValue = max([value for value in self.myList])
        self.myList.remove(minValue)
        return minValue


    def tryAddNewValue(self, newValue):
        # Compare and add the max of the two values
        minValue = self._getMinValue()
        if minValue[0] > newValue[0]:
            self.myList.append(minValue)
        else:
            self.myList.append(newValue)


    def getSortedList(self):
        # Get a sorted list of values
        sorted = []
        for i in range(0,len(self.myList)):
            sorted.append(self._getMaxValue())

        return sorted


    def testTopFive(self):
        # test top N
        self.tryAddNewValue((3, 'abc'))
        self.tryAddNewValue((4, 'abc'))
        self.tryAddNewValue((2, 'abc'))
        self.tryAddNewValue((3, 'abc'))
        self.tryAddNewValue((1, 'abc'))
        self.tryAddNewValue((5, 'abc'))
        self.tryAddNewValue((3, 'abc'))
        self.tryAddNewValue((4, 'abc'))





class Indexer:

    def __init__(self, indexerID,config):
        self.config = config
        self.fileWriter = FileWriter(self.config)
        self.ID = indexerID

        self.myDictionaryByLetters = {}

        # Init a dictionary with letters dictionaries
        for letter in string.ascii_lowercase[:26]:
            self.myDictionaryByLetters[letter] = MyDictionary()
        self.myDictionaryByLetters["#"] = MyDictionary()

        # init fields
        self.documents_dictionary = {}
        self.city_dictionary = {}
        self.languagesDic = {}
        self.flushIndicator = 0


    def addNewDoc(self, document,docNoAsIndex=0):

        # Go over each term in the doc
        documentDictionary = document.termDocDictionary_term_termData
        docNo = document.docNo
        maxFrequentWord = 0

        # TopList of five
        dominantTerms = TopList(5)



        for term, termData in documentDictionary.items():
            # add the term to the dictionary
            if len(term) <= 1:
                continue

            # Remove unwanted chars
            if not englishLetters.get(term[0]) and not term[0].isdigit():
                continue

            termFrequency = termData.getTermFrequency()
            if englishLetters.get(term[0]):

                # ZAXROY raplaces the city in the doc
                if 'ZAXROY' in term and len(document.city) > 1:
                    term = term.replace('ZAXROY',document.city)

                # Add term to the letter's dictionary
                self.myDictionaryByLetters[term[0].lower()].addTerm(termString=term,
                                                                    docNo=docNo,
                                                                    termFrequency=termFrequency,
                                                                    termPositions=termData.getPositions(),
                                                                    docNoAsIndex=docNoAsIndex)


                # If entity, check if term is in Top5 in doc
                if term.isupper():
                    from Ranker.Ranker import getPositionsScore
                    positionsAsString = termData.getPositions()
                    listOfPositionsWithGaps = positionsAsString.split(':')
                    # get location score
                    score = getPositionsScore(document.docLength,listOfPositionsWithGaps)

                    # add if score is greater than min value
                    dominantTerms.tryAddNewValue((score, term))


            else:
                if len(term) > 0:
                    self.myDictionaryByLetters["#"].addTerm(termString=term,
                                                            docNo=docNo,
                                                            termFrequency=termFrequency,
                                                            termPositions=termData.getPositions(),
                                                            docNoAsIndex=docNoAsIndex)

            # Check if term has the max freq in doc
            maxFrequentWord = max(termFrequency, maxFrequentWord)





        # Create IndexData
        newDocumentIndexData = DocumentIndexData(max_tf=maxFrequentWord,
                                                 uniqueTermsCount=len(document.termDocDictionary_term_termData),
                                                 docLength=document.docLength,
                                                 city = document.city,
                                                 language = document.language,
                                                 dominantTerm=dominantTerms.getSortedList())


        # Add doc to document dictionary
        self.documents_dictionary[docNo] = newDocumentIndexData

        if len(document.city) > 1:
            positions = ''
            try:
                # get city position
                positions = document.termDocDictionary_term_termData["ZAXROY"].getPositions()

            except Exception as ex:
                pass


            # Add city to cities dictionary
            if self.city_dictionary.get(document.city) is None:
                self.city_dictionary[document.city] = CityIndexData(docNoAsIndex, positions)
            else:
                # If already exists - add to list
                self.city_dictionary[document.city].addDocumentToCity(docNoAsIndex, positions)

        # If language doesnt exists - add to language dic
        if len(document.language) > 1 and self.languagesDic.get(document.language) is None:
            self.languagesDic[document.language] = True




    def flushMemory(self):

        # Save posting to tempFile
        self.fileWriter.cleanIndex(self)

        # Write docs to temp docFile
        self.fileWriter.cleanDocuments(self.documents_dictionary)
        self.documents_dictionary = {}

        self.flushIndicator += 1
        # Every 10 flushes - clean the letter dictionary
        if self.flushIndicator == 10:
            self.flushIndicator = 0
            for letter in string.ascii_lowercase[:26]:
                self.myDictionaryByLetters[letter] = MyDictionary()
            self.myDictionaryByLetters["#"] = MyDictionary()


    def updateProgressBar(self, value, posting_merge):
        path = self.config.get__savedFilePath() + '/Progress/%s' % (posting_merge)
        fileName = str(self.ID) + '_' + str(value)

        if os.path.exists(path):
            myFile = open(path + '/' + fileName, 'w')
            myFile.close()



    def merge(self):
        from Indexing.KWayMerge import Merger
        from concurrent.futures import ThreadPoolExecutor

        merger = Merger(config=self.config)
        savedFilesPathList = list(string.ascii_lowercase)
        savedFilesPathList.append('#')

        executor = ThreadPoolExecutor()
        futureList = []

        # merge local 'small' files
        for folder in savedFilesPathList:
            letterFilesList = os.listdir(self.config.savedFilePath + "\\" + folder)
            fileToMergeList = []
            filesPerIteration = 10
            iteration = 0
            counter = 0

            progressCounter = 0

            # Iter over letterList and if file belongs to ID - add to merge list
            for letterFile in letterFilesList:

                if letterFile[1] == str(self.ID):
                    iteration += 1
                    fileToMergeList.append(letterFile)
                    if iteration == filesPerIteration:
                        # update progress
                        progressCounter += 10*iteration
                        self.updateProgressBar(progressCounter, 'Merge')

                        iteration = 0
                        # merge the list
                        mergedList = merger.merge(fileToMergeList)
                        if mergedList is None:
                            continue

                        # Create future - Write the merged tempFiles
                        future = executor.submit(self.fileWriter.writeMergedFileTemp,mergedList, self.config.savedFilePath + "\\" + folder + "\\" + str(folder[0]) + str(self.ID) + "-" + str(counter))
                        # add future
                        futureList.append(future)
                        fileToMergeList = []

                        counter += 1

            # If greater than half - also make a temp file
            if iteration > filesPerIteration / 2:

                mergedList = merger.merge(fileToMergeList)
                if mergedList is not None:
                    future = executor.submit(self.fileWriter.writeMergedFileTemp, mergedList,
                                             self.config.savedFilePath + "\\" + folder + "\\" + str(folder[0]) + str(
                                                 self.ID) + "-" + str(counter))

                    futureList.append(future)


            # update progress
            progressCounter += 10*iteration
            if progressCounter > 0:
                self.updateProgressBar(progressCounter, 'Merge')

            fileToMergeList = []

            for future in futureList:
                future.result()

            # Add files to mergeList
            letterFilesList = os.listdir(self.config.savedFilePath + "\\" + folder)
            for letterFile in letterFilesList:
                if letterFile[1] == str(self.ID):
                    fileToMergeList.append(letterFile)


            # Merge the list - add future
            mergedList = merger.merge(fileToMergeList)
            if mergedList is not None:
                future = executor.submit(self.fileWriter.writeMergedFileTemp, mergedList,
                                         self.config.savedFilePath + "\\" + folder + "\\" + str(folder[0]) + str(
                                             self.ID))
                futureList.append(future)

        # Close ThreadPool
        executor.shutdown()


englishLetters = {

    'a' : True,
    'A' : True,
    'b' : True,
    'B' : True,
    'c' : True,
    'C' : True,
    'd' : True,
    'D' : True,
    'e' : True,
    'E' : True,
    'f' : True,
    'F' : True,
    'g' : True,
    'G' : True,
    'h' : True,
    'H' : True,
    'i' : True,
    'I' : True,
    'j' : True,
    'J' : True,
    'k' : True,
    'K' : True,
    'l' : True,
    'L' : True,
    'm' : True,
    'M' : True,
    'n' : True,
    'N' : True,
    'o' : True,
    'O' : True,
    'p' : True,
    'P' : True,
    'q' : True,
    'Q' : True,
    'r' : True,
    'R' : True,
    's' : True,
    'S' : True,
    't' : True,
    'T' : True,
    'u' : True,
    'U' : True,
    'v' : True,
    'V' : True,
    'w' : True,
    'W' : True,
    'x' : True,
    'X' : True,
    'y' : True,
    'Y' : True,
    'z' : True,
    'Z' : True,

}