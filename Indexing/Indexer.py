from Indexing.MyDictionary import MyDictionary
import string

class Indexer:


    def __init__(self):

        # self.myDictionary = MyDictionary()

        self.myDictionaryByLetters = {}
        for letter in string.ascii_lowercase[:26]:
            self.myDictionaryByLetters[letter] = MyDictionary()
        self.myDictionaryByLetters["#"] = MyDictionary()



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

    def flushMemory(self):
        from Indexing import FileWriter
        import MyExecutors
        MyExecutors._instance.CPUExecutor.apply_async(FileWriter.cleanIndex,(self,))


