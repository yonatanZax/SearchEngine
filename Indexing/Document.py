


class Document:

    def __init__(self, docNo, termDocDictionary = None, docLength=0, city=None):
        self.docNo = docNo
        self.termDocDictionary_term_termData = termDocDictionary
        self.docLength = docLength
        # self.mostFrequentTermNumber = maxTFDoc
        self.city = city




class TermData:

    def __init__(self, termFrequency, startPos):
        self.termFrequency = termFrequency
        self.startPos = str(startPos)


    def toString(self):
        return ','.join([self.termFrequency,self.startPos])








