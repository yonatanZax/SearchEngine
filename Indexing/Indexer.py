
from Indexing.Document import Document
from Indexing.Document import TermData

class Indexer:


    def __init__(self):

        self.dictionary = {}


    def addNewDoc(self,doc):
        # return
        listOfDataTerms = doc.termList
        for dataTerm in listOfDataTerms:
            term = dataTerm.term
            valueFromDic = self.dictionary.get(term)
            isLower = self.dictionary.get(term.lower())
            if isLower is not None:
                term = term.lower()
            if valueFromDic is not None:
                count = valueFromDic[0] + 1
                self.dictionary[term] = [count,[doc.docNo, dataTerm.toString()] + valueFromDic[1]]
            else:
                if term[0].islower():
                    term = term.lower()
                    dataTerm.term = term
                else:
                    term = term.upper()
                    dataTerm.term = term
                self.dictionary[term] = [1,[doc.docNo, dataTerm.toString()]]

        print(self.dictionary)


