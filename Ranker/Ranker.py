import math


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
            docIDList.append((self.dictionary_document_info[int(docNo_score[0])][0], docNo_score[1]))
        return docIDList


    def getDocumentsFromCityList(self, citiesList: list)-> set:
        documentsDict = set()
        for city in citiesList:
            documentsDict.update(self.dictionary_city_documents[city].keys())
        return documentsDict



    def getScore(self, docID:str, docDF:int, positionList:list, termDF:int) -> int:
        BM25Score = self.getBM25Score(docID=int(docID), docDF=docDF, termDF=termDF)
        # TODO - calculate the score in more ways
        return BM25Score



    def getBM25Score(self, docID:int, docDF:int, termDF:int):
        """
        BM25:
        F(q,d) = SIGMA[c(w,q)*((k+1)*c(w,d))/((c(w,d)+k*(1-b+b*|D|/avd(D)))*Log((M+1)/df(w))
        """

        mone = (self.config.BM25_K + 1) * docDF

        mehane = docDF + self.config.BM25_K*(1 - self.config.BM25_B + self.config.BM25_B * int(self.dictionary_document_info[docID][2])/self.config.BM25_avgDLength)

        log = math.log10((self.config.totalNumberOfDocs + 1) / termDF)

        score = (mone / mehane) * log

        return score

