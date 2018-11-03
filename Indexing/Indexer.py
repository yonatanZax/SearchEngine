from Indexing.MyDictionary import MyDictionary


class Indexer:


    def __init__(self):

        self.myDictionary = MyDictionary()


    def addNewDoc(self, document):
        # go over each term in the doc
        documentDictionary = document.termDocDictionary_term_termData
        docNo = document.docNo
        for term, termData in documentDictionary.items():
            # add the term to the dictionary
            self.myDictionary.addTerm(termString=term, docNo=docNo, termFrequency=termData.termFrequency)

    def flushMemory(self):
        return

