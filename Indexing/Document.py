


class Document:

    def __init__(self, docNo, termDoc):
        self.docNo = docNo
        self.termDoc = termDoc
        # self.mostFrequentTermNumber
        # self.documentLength


class TermData:

    def __init__(self, term,count, startPos, length, posValue):
        self.term = str(term)
        self.count = count
        self.startPos = str(startPos)
        self.length = str(length)
        self.posValue = str(posValue)


    def toString(self):
        return ','.join([self.term,self.startPos,self.length,self.posValue])








