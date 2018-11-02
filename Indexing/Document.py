


class Document:

    def __init__(self, docNo, termList):
        self.docNo = docNo
        self.termList = termList

class TermData:

    def __init__(self, term, startPos, length, posValue):
        self.term = str(term)
        self.startPos = str(startPos)
        self.length = str(length)
        self.posValue = str(posValue)


    def toString(self):
        return ','.join([self.term,self.startPos,self.length,self.posValue])








