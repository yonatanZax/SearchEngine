import os
from Indexing.MyDictionary import MyDictionary, DocumentIndexData,CityIndexData
import string
from Indexing.FileWriter import FileWriter

class Indexer:

    # TODO - add 2 information on terms or documents - added locations

    def __init__(self, indexerID,config):
        self.config = config
        self.fileWriter = FileWriter(self.config)
        self.ID = indexerID

        self.myDictionaryByLetters = {}
        for letter in string.ascii_lowercase[:26]:
            self.myDictionaryByLetters[letter] = MyDictionary()
        self.myDictionaryByLetters["#"] = MyDictionary()

        self.documents_dictionary = {}

        self.city_dictionary = {}

    def addNewDoc(self, document):
        # go over each term in the doc
        documentDictionary = document.termDocDictionary_term_termData
        docNo = document.docNo
        maxFrequentWord = 0
        for term, termData in documentDictionary.items():
            # add the term to the dictionary
            if len(term) <= 1:
                continue
            if not englishLetters.get(term[0]) and not term[0].isdigit():
                continue
            termFrequency = termData.getTermFrequency()
            if englishLetters.get(term[0]):
                if term == 'ZAXROY':
                    term = document.city
                self.myDictionaryByLetters[term[0].lower()].addTerm(termString=term, docNo=docNo, termFrequency=termFrequency, termPositions=termData.getPositions())
            else:
                if len(term) > 0:
                    self.myDictionaryByLetters["#"].addTerm(termString=term, docNo=docNo, termFrequency=termFrequency, termPositions=termData.getPositions())
            maxFrequentWord = max(termFrequency, maxFrequentWord)
        newDocumentIndexData = DocumentIndexData(max_tf=maxFrequentWord, uniqueTermsCount=len(document.termDocDictionary_term_termData), docLength=document.docLength, city = document.city)
        self.documents_dictionary[docNo] = newDocumentIndexData

        if len(document.city) > 1:
            positions = ''
            try:
                positions = document.termDocDictionary_term_termData["ZAXROY"].getPositions()

            except Exception as ex:
            # print("CITYERROR: " + str(ex) + " " + str(docNo) + " " + str(document.city))
                x=1

            if self.city_dictionary.get(document.city) is None:
                self.city_dictionary[document.city] = CityIndexData(docNo, positions)
            else:
                self.city_dictionary[document.city].addDocumentToCity(docNo, positions)




    def flushMemory(self):
        self.fileWriter.cleanIndex(self)
        self.fileWriter.cleanDocuments(self.documents_dictionary)
        self.documents_dictionary = {}



    def merge(self):
        from datetime import datetime
        from Indexing.KWayMerge import Merger
        from concurrent.futures import ThreadPoolExecutor
        from concurrent.futures import as_completed

        startTime = datetime.now()

        merger = Merger(config=self.config)
        savedFilesPathList = os.listdir(self.config.savedFilePath)

        executor = ThreadPoolExecutor()
        futureList = []


        savedFilesPathList.remove('docIndex')
        for folder in savedFilesPathList:
            letterFilesList = os.listdir(self.config.savedFilePath + "\\" + folder)
            fileToMergeList = []
            filesPerIteration = 10
            iteration = 0
            counter = 0
            for letterFile in letterFilesList:

                if letterFile[1] == str(self.ID):
                    iteration += 1
                    fileToMergeList.append(letterFile)
                    if iteration == filesPerIteration:
                        iteration = 0
                        mergedList = merger.merge(fileToMergeList)

                        executor.submit(self.fileWriter.writeMergedFileTemp,mergedList, self.config.savedFilePath + "\\" + folder + "\\" + str(folder[0]) + str(self.ID) + "-" + str(counter))
                        fileToMergeList = []
                        counter += 1

            if iteration > filesPerIteration / 2:
                mergedList = merger.merge(fileToMergeList)

                # self.fileWriter.writeMergedFileTemp(mergedList,self.config.savedFilePath + "\\" + folder + "\\" + str(folder[0]) + str(self.ID) + "-" + str(counter))
                executor.submit(self.fileWriter.writeMergedFileTemp, mergedList,self.config.savedFilePath + "\\" + folder + "\\" + str(folder[0]) + str(self.ID) + "-" + str(counter))
            fileToMergeList = []

            executor.shutdown(True)

            letterFilesList = os.listdir(self.config.savedFilePath + "\\" + folder)
            for letterFile in letterFilesList:
                if letterFile[1] == str(self.ID):
                    fileToMergeList.append(letterFile)

            mergedList = merger.merge(fileToMergeList)

            self.fileWriter.writeMergedFileTemp(mergedList,self.config.savedFilePath + "\\" + folder + "\\" + str(folder[0]) + str(self.ID))
            # executor.submit(self.fileWriter.writeMergedFileTemp,mergedList,self.config.savedFilePath + "\\" + folder + "\\" + str(folder[0]) + str(self.ID))




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