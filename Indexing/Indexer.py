import os
from Indexing.MyDictionary import MyDictionary, DocumentIndexData
import string
import Configuration as config

class Indexer:

    # TODO - add 2 information on terms or documents

    def __init__(self, indexerID):
        self.ID = indexerID

        self.myDictionaryByLetters = {}
        for letter in string.ascii_lowercase[:26]:
            self.myDictionaryByLetters[letter] = MyDictionary()
        self.myDictionaryByLetters["#"] = MyDictionary()

        self.documents_dictionary = {}

        self.country_dictionary = {}

    def addNewDoc(self, document):
        # go over each term in the doc
        documentDictionary = document.termDocDictionary_term_termData
        docNo = document.docNo
        maxFrequentWord = 0
        for term, termData in documentDictionary.items():
            # add the term to the dictionary
            # term = cleanDashesCommas(term)
            if len(term) == 0:
                continue
            if englishLetters.get(term[0]):
                self.myDictionaryByLetters[term[0].lower()].addTerm(termString=term, docNo=docNo, termFrequency=termData.termFrequency)
            else:
                if len(term) > 0:
                    self.myDictionaryByLetters["#"].addTerm(termString=term, docNo=docNo, termFrequency=termData.termFrequency)
            maxFrequentWord = max(termData.termFrequency, maxFrequentWord)
        newDocumentIndexData = DocumentIndexData(max_tf=maxFrequentWord, uniqueTermsCount=len(document.termDocDictionary_term_termData), docLength=document.docLength, city = document.city)
        self.documents_dictionary[docNo] = newDocumentIndexData

    def flushMemory(self):
        from Indexing import FileWriter
        FileWriter.cleanIndex(self)

        FileWriter.cleanDocuments(self.documents_dictionary)
        self.documents_dictionary = {}


    def uploadDictionary(self):
#         TODO - implement me
        x=1

    @staticmethod
    def merge():
        from datetime import datetime
        from Indexing.KWayMerge import Merger
        from Indexing import FileWriter

        startTime = datetime.now()

        merger = Merger()
        savedFilesPathList = os.listdir(config.savedFilePath)

        savedFilesPathList.remove('docIndex') # TODO - find a way to fix this

        for folder in savedFilesPathList:
            letterFilesList = os.listdir(config.savedFilePath + "\\" + folder)
            mergedList = merger.merge(letterFilesList)
            FileWriter.writeMergedFile(mergedList , config.savedFilePath + "\\" + folder + "\\mergedFile")


        finishTime = datetime.now()
        timeItTook = finishTime - startTime

        print("Entire Merge took: "+ str(timeItTook.seconds) + " seconds")


def cleanDashesCommas(token):
    # TODO - remove this function and the use of this in addNewDoc
    size = len(token)
    if size > 0:
        start = 0
        while start < size:
            if token[start] == '-' or token[start] == ',' or token[start] == '.' or token[start] == '=':
                start += 1
            break

        token = token[start:].strip('-').strip(',').strip('.')

    return token



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





