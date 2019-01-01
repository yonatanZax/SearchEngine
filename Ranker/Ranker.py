import math
import BasicMethods as basic
import os


class Ranker:

    def __init__(self, config):
        self.config = config

        # format: key=docID, value = [0-max_tf, 1-uniqueTermCount, 2-docLength, 3-City, 4-Language]
        self.dictionary_document_info_stemmed = {}
        self.numberOfDoc_Stemmed = 0
        self.averageDocLength_Stemmed = 0
        if os.path.exists(self.config.get__documentIndexPathStem()):
            self.numberOfDoc_Stemmed, self.averageDocLength_Stemmed = self.__initNumOfDocs_AvgLength(self.config.get__documentIndexPathStem(), self.dictionary_document_info_stemmed)

        self.numberOfDoc_NotStemmed = 0
        self.averageDocLength_NotStemmed = 0
        self.dictionary_document_info_withoutStem = {}
        if os.path.exists(config.get__documentIndexPathWithoutStem()):
            self.numberOfDoc_NotStemmed, self.averageDocLength_NotStemmed = self.__initNumOfDocs_AvgLength(self.config.get__documentIndexPathWithoutStem(), self.dictionary_document_info_withoutStem)

        self.dictionary_city_documents_withoutStem = {}
        if os.path.exists(config.get__cityIndexPathWithoutStem()):
            self.__initCitiesIndex(config.get__cityIndexPathWithoutStem(), self.dictionary_city_documents_withoutStem)

        self.dictionary_city_documents_Stemmed = {}
        if os.path.exists(config.get__cityIndexPathStem()):
            self.__initCitiesIndex(config.get__cityIndexPathStem(), self.dictionary_city_documents_Stemmed)



    @staticmethod
    def __initNumOfDocs_AvgLength(path, dictionary):
        """
        Initialize the document dictionary from the given path of the document index
        :param path:
        :param dictionary:
        :return:
        """
        file = open(path,'r',encoding='utf-8')
        fileLines = file.readlines()
        file.close()
        del file
        if len(fileLines) == 0:
            return 0, 0
        totalLength = 0
        for lineNumber in range(0,len(fileLines)):
            splitLine = fileLines[lineNumber].split('|')
            dictionary[lineNumber] = splitLine
            totalLength += int(splitLine[3])
        return len(fileLines), totalLength/len(fileLines)

    @staticmethod
    def __initCitiesIndex(path, dictionary):
        """
        Initialize the document dictionary from the given path of the document index
        :param path:
        :param dictionary:
        :return:
        """
        file = open(path,'r',encoding='utf-8')
        fileLines = file.readlines()
        file.close()
        del file
        for line in fileLines:
            splitLine = line.split('|')
            city = splitLine[0]
            documents = splitLine[4].split(',')
            document_positionsList_dict = {}
            gapAccumulator = 0

            for document_positions in documents:
                document_location = document_positions.split('#')
                gapAccumulator += int(document_location[0])
                documentID = gapAccumulator
                cityPositionsInDocument = document_location[1].split(':')
                document_positionsList_dict[documentID] = cityPositionsInDocument
            dictionary[city] = document_positionsList_dict


    def convertDocNoListToDocID(self, docIndexList):
        """
        Initialize the document dictionary from the given path of the document index
        :param path:
        :param dictionary:
        :return:
        """
        documentDictionary = {}
        if self.config.get__toStem():
            documentDictionary = self.dictionary_document_info_stemmed
        else:
            documentDictionary = self.dictionary_document_info_withoutStem
        docIDList = []
        for docIndex_score in docIndexList:
            docIDList.append([documentDictionary[int(docIndex_score[0])][0], docIndex_score[1], int(docIndex_score[0])])
        return docIDList


    def getDocumentsFromCityList(self, citiesList):
        """
        Initialize the document dictionary from the given path of the document index
        :param path:
        :param dictionary:
        :return:
        """
        cityDictionary = {}
        if self.config.get__toStem():
            cityDictionary = self.dictionary_document_info_stemmed
        else:
            cityDictionary = self.dictionary_document_info_withoutStem
        documentsDict = set()
        for city in citiesList:
            documentsDict.update(cityDictionary[city].keys())
        return documentsDict



    def getScore(self, docID, docDF, positionList, termDF):
        """
        get the score for the document considering the information it received
        :param docID: the number representing the document to get its data from the document index
        :param docDF: the number of times the term appear in the document
        :param positionList: a list of all the locations of the term in the document
        :param termDF: number of documents the term appears in
        :return: the score of the document for the term
        """
        docLength = 0
        avgDocLength = 0.0
        numberOfDocs = 0

        # get the current working data information
        if self.config.get__toStem():
            docLength = int(self.dictionary_document_info_stemmed[docID][2])
            avgDocLength = self.averageDocLength_Stemmed
            numberOfDocs = self.numberOfDoc_Stemmed
        else:
            docLength = int(self.dictionary_document_info_withoutStem[docID][2])
            avgDocLength = self.averageDocLength_NotStemmed
            numberOfDocs = self.numberOfDoc_NotStemmed

        BM25Score = self.getBM25Score(docDF=docDF, termDF=termDF, documentLength=docLength, docLengthAvg=avgDocLength, numOfDocs=numberOfDocs)

        AxiomaticTermWeightingScore = self.getAxiomaticTermWeightingScore(docDF=docDF, termDF=termDF, documentLength=docLength, docLengthAvg=avgDocLength, numOfDocs=numberOfDocs)

        # Add positionScore
        docLength = int(docLength)
        positionScore = getPositionsScore(docLength, positionList)

        joinedScore = BM25Score + self.config.Axu_Value * AxiomaticTermWeightingScore


        # joinedScore = BM25Score + 3*AxiomaticTermWeightingScore + 0.3*positionScore

        # if positionList[0] is '-':
        #     joinedScore *= 1.5

        # return positionScore
        # return AxiomaticTermWeightingScore
        return joinedScore



    def getBM25Score(self, docDF, termDF, documentLength, docLengthAvg, numOfDocs):
        """
        compute the bm25 score
        BM25:
        F(q,d) = SIGMA[c(w,q)*((k+1)*c(w,d))/((c(w,d)+k*(1-b+b*|D|/avd(D)))*Log((M-c(w,d)+0.5)/(df(w)+0.5))]
        """

        mone = (self.config.BM25_K + 1) * docDF

        mehane = docDF + self.config.BM25_K*(1 - self.config.BM25_B + self.config.BM25_B * (documentLength/docLengthAvg))

        # log = math.log10((self.config.totalNumberOfDocs + 1) / termDF)

        log = math.log10((numOfDocs - termDF + 0.5) / (termDF + 0.5))

        score = (mone / mehane) * log

        return score

    @staticmethod
    def getAxiomaticTermWeightingScore(docDF, termDF, documentLength, docLengthAvg, numOfDocs):
#         https://pdfs.semanticscholar.org/94c9/30d010c17f3edc0df39ea99fd311d33327c1.pdf

        mone = docDF * math.pow(numOfDocs,0.35)

        mehane = (docDF + 0.5 + (0.5 * float(documentLength) / docLengthAvg)) * termDF

        return mone / mehane


def getPositionsScore(length, listOfPositionsWithGaps):
    """
    compute the score of by the positions
    :param length:
    :param listOfPositionsWithGaps:
    :return:
    """
    score = 0
    lastPos = 0
    for pos in listOfPositionsWithGaps:
        if pos == '-':
            score += 1.5
            continue

        if basic.isInt(pos):
            lastPos += int(pos)
            score += (1 - lastPos / length)

    return score
