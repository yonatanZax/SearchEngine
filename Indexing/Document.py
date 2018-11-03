


class Document:

    def __init__(self, docNo, termDocDictionary):
        self.docNo = docNo
        self.termDocDictionary_term_termData = termDocDictionary
        # self.mostFrequentTermNumber
        # self.documentLength


class TermData:

    def __init__(self, termFrequency, startPos):
        self.termFrequency = termFrequency
        self.startPos = str(startPos)


    def toString(self):
        return ','.join([self.termFrequency,self.startPos])








