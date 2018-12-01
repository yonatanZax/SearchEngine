


class Document:

    def __init__(self, docNo, termDocDictionary = None, docLength=0, city=''):
        self.docNo = docNo
        self.termDocDictionary_term_termData = termDocDictionary
        self.docLength = docLength
        # self.mostFrequentTermNumber = maxTFDoc
        self.city = city




class TermData:

    def __init__(self, termFrequency, position):
        self._termFrequency = termFrequency
        self._positionStringWithGaps = str(position)
        self._lastPositionEntered = position

    def addPositionToTerm(self, position):
        self._termFrequency += 1
        gap = position - self._lastPositionEntered
        self._positionStringWithGaps += ':' + str(gap)
        self._lastPositionEntered = position

    def getTermFrequency(self):
        return self._termFrequency

    def getPositions(self):
        return self._positionStringWithGaps

    def toString(self):
        return '#'.join([self._termFrequency, self._positionStringWithGaps])








