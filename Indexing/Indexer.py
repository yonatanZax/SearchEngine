
class Indexer:


    def __init__(self):

        self.dictionary = {}


    def addNewDoc(self,doc):
        # return
        dicOfDataTerms = doc.termDoc
        for key, value in dicOfDataTerms.items():
        # for dataTerm in listOfDataTerms:
            term = key
            valueFromDic = self.dictionary.get(term)
            isLower = self.dictionary.get(term.lower())
            if isLower is not None:
                term = term.lower()
            if valueFromDic is None:
                if term[0].islower():
                    term = term.lower()
                    value.term = term
                else:
                    term = term.upper()
                    value.term = term
                self.dictionary[term] = [[doc.docNo, value.toString()]]
            else:
                valueFromDic.append([doc.docNo, value.toString()])
                self.dictionary[term] = valueFromDic



