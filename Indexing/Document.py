


class Document:

    def __init__(self, docNo, termDocDictionary = None, docLength = 0, city = '',language = ''):
        self.docNo = docNo
        self.termDocDictionary_term_termData = termDocDictionary
        self.docLength = docLength
        self.city = city
        self.language = language




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
        return '#'.join([str(self._termFrequency), self._positionStringWithGaps])

    def setInTitle(self):
        self._termFrequency += 1
        self._positionStringWithGaps = '-:' + self._positionStringWithGaps


    def toString(self):
        return '#'.join([str(self._termFrequency), self._positionStringWithGaps])



