import math
import BasicMethods as basic


class Ranker:

    def __init__(self, config):
        self.config = config

        # format: key=docID, value = [0-max_tf, 1-uniqueTermCount, 2-docLength, 3-City, 4-Language]
        self.dictionary_document_info = {}
        self.__getDocumentIndex()

        self.dictionary_city_documents = {}
        self.__getCitiesIndex()



    def __getDocumentIndex(self):
        file = open(self.config.get__documentsIndexPath(),'r',encoding='utf-8')
        fileLines = file.readlines()
        file.close()
        del file
        totalLength = 0
        for lineNumber in range(0,len(fileLines)):
            splitLine = fileLines[lineNumber].split('|')
            self.dictionary_document_info[lineNumber] = splitLine
            totalLength += int(splitLine[3])
        self.config.setAverageDocLength(totalLength=totalLength, numberOfDocs=len(fileLines))


    def __getCitiesIndex(self):
        file = open(self.config.getSavedFilesPath() + '/cityIndex','r',encoding='utf-8')
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
            self.dictionary_city_documents[city] = document_positionsList_dict


    def convertDocNoListToDocID(self, docNoList : list)-> list:
        docIDList = []
        for docNo_score in docNoList:
            docIDList.append([self.dictionary_document_info[int(docNo_score[0])][0], docNo_score[1], int(docNo_score[0])])
        return docIDList


    def getDocumentsFromCityList(self, citiesList: list)-> set:
        documentsDict = set()
        for city in citiesList:
            documentsDict.update(self.dictionary_city_documents[city].keys())
        return documentsDict



    def getScore(self, docID:str, docDF:int, positionList:list, termDF:int) -> float:

        BM25Score = self.getBM25Score(docID=int(docID), docDF=docDF, termDF=termDF)

        AxiomaticTermWeightingScore = self.getAxiomaticTermWeightingScore(docID=int(docID), docDF=docDF, termDF=termDF)

        # Add positionScore
        docLength = int(self.dictionary_document_info[docID][2])
        positionScore = getPositionsScore(docLength,positionList)

        # TODO - calculate the score in more ways
        joinedScore = BM25Score + 6*AxiomaticTermWeightingScore
        # joinedScore = BM25Score + 3*AxiomaticTermWeightingScore + 0.3*positionScore

        # if positionList[0] is '-':
        #     joinedScore *= 1.5

        # return positionScore
        # return AxiomaticTermWeightingScore
        return joinedScore



    def getBM25Score(self, docID:int, docDF:int, termDF:int)->float:
        """
        BM25:
        F(q,d) = SIGMA[c(w,q)*((k+1)*c(w,d))/((c(w,d)+k*(1-b+b*|D|/avd(D)))*Log((M-c(w,d)+0.5)/(df(w)+0.5))]
        """

        docLength = float(self.dictionary_document_info[docID][2])


        mone = (self.config.BM25_K + 1) * docDF

        mehane = docDF + self.config.BM25_K*(1 - self.config.BM25_B + self.config.BM25_B * (docLength/self.config.BM25_avgDLength))

        # log = math.log10((self.config.totalNumberOfDocs + 1) / termDF)

        log = math.log10((self.config.totalNumberOfDocs - termDF + 0.5) / (termDF + 0.5))

        score = (mone / mehane) * log

        return score


    def getAxiomaticTermWeightingScore(self, docID:int, docDF:int, termDF:int):
#         https://pdfs.semanticscholar.org/94c9/30d010c17f3edc0df39ea99fd311d33327c1.pdf

        mone = docDF * math.pow(self.config.totalNumberOfDocs,0.35)

        mehane = (docDF + 0.5 + (0.5 * float(self.dictionary_document_info[docID][2]) / self.config.BM25_avgDLength)) * termDF

        return mone / mehane


def getPositionsScore(length, listOfPositionsWithGaps):
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
