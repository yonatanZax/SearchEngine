from Indexing.MyDictionary import MyDictionary, DocumentIndexData
import string

class Indexer:


    def __init__(self):

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
        for term, termData in documentDictionary.items():
            # add the term to the dictionary
            if term[0].isalpha():
                self.myDictionaryByLetters[term[0].lower()].addTerm(termString=term, docNo=docNo, termFrequency=termData.termFrequency)
            else:
                self.myDictionaryByLetters["#"].addTerm(termString=term, docNo=docNo, termFrequency=termData.termFrequency)
        newDocumentIndexData = DocumentIndexData(max_tf=document.mostFrequentTermNumber, uniqueTermsCount=len(document.termDocDictionary_term_termData), docLength=document.docLength, city = document.city)
        self.documents_dictionary[docNo] = newDocumentIndexData

    def flushMemory(self):
        from Indexing import FileWriter
        import MyExecutors
        MyExecutors._instance.CPUExecutor.apply_async(FileWriter.cleanIndex,(self,))






