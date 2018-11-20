from Indexing.MyDictionary import MyDictionary, DocumentIndexData
import string

class Indexer:


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
            if term[0].isalpha():
                self.myDictionaryByLetters[term[0].lower()].addTerm(termString=term, docNo=docNo, termFrequency=termData.termFrequency)
            else:
                self.myDictionaryByLetters["#"].addTerm(termString=term, docNo=docNo, termFrequency=termData.termFrequency)
            maxFrequentWord = max(termData.termFrequency, maxFrequentWord)
        newDocumentIndexData = DocumentIndexData(max_tf=maxFrequentWord, uniqueTermsCount=len(document.termDocDictionary_term_termData), docLength=document.docLength, city = document.city)
        self.documents_dictionary[docNo] = newDocumentIndexData

    def flushMemory(self):
        from Indexing import FileWriter
        FileWriter.cleanIndex(self)

        FileWriter.cleanDocuments(self.documents_dictionary)
        self.documents_dictionary = {}
        





