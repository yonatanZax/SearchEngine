import string

from Parsing.IterativeParsing import IterativeTokenizer
import os

from Ranker.Ranker import Ranker
from Searching.WordEmbedding import WordEmbedding


class SearcherIterativeTokenizer(IterativeTokenizer):

    def ruleNBA(self, index: int, textList: list) -> (list,int):

        listOfTerms = [textList[index]]
        bigLetters = textList[index][0]
        tempIndex = index + 1
        while tempIndex < len(textList):

            currWord = textList[tempIndex]
            currWord = self.cleanToken(currWord)
            if currWord is None:
                tempIndex += 1
                continue

            if currWord[0].isupper():
                bigLetters += currWord[0]
                if len(bigLetters) > 6:
                    # Too long, return first
                    return listOfTerms, index + 1
            else:
                # Only the first is upper
                if len(bigLetters) == 1:
                    return listOfTerms, index + 1

                # Add the combination, add the
                listOfTerms = [' '.join(textList[index:tempIndex])] + textList[index:tempIndex]
                listOfTerms.append(bigLetters)
                return listOfTerms, tempIndex

            tempIndex += 1

        listOfTerms = [' '.join(textList[index:tempIndex])] + textList[index:tempIndex]
        listOfTerms.append(bigLetters)
        return listOfTerms, tempIndex




class Searcher:

    def __init__(self, config, dataNoStem, dataWithStem):
        self.iterativeTokenizer = SearcherIterativeTokenizer(config)

        # form of dictionary: key=term, value=[0-df, 1-sumTF, 2-postingLine]
        self.termDictionaryNoStem = dataNoStem
        self.termDictionaryWithStem = dataWithStem

        self.config = config
        # self.wordEmbedding = WordEmbedding()

        self.ranker = Ranker(config)


        dataNoStemLen = 0
        dataWithStemLen = 0
        if dataNoStem is not None:
            dataNoStemLen = len(dataNoStem)
        if dataWithStem is not None:
            dataWithStemLen = len(dataWithStem)

        self.config.setTotalNumberOfTerms(numNoStem=dataNoStemLen,numWithStem=dataWithStemLen)
        self.documentsByCitiesSet = None




    def getDocsForQueryWithExpansion(self, queryString: str, citiesList: list=None, expend: bool=False, useStem = False):
        """
        get a query and return the docs in the correct order with expanding of the query using the word embedding
        :param expend:
        :param citiesList:
        :param queryString:
        :return:
        """

        queryTermDictionary, queryLength = self.iterativeTokenizer.parseText(queryString)
        queryList = list(queryTermDictionary.keys())
        if expend:
            queryList = self.wordEmbedding.expandQuery(queryList)

        self.documentsByCitiesSet = None
        if len(citiesList) > 0:
            self.documentsByCitiesSet = self.ranker.getDocumentsFromCityList(citiesList=citiesList)


        if useStem:
            termDictionary = self.termDictionaryWithStem
        else:
            termDictionary = self.termDictionaryNoStem

        document_score_dictionary = {}
        for term in queryList:
            termForm = None
            if termDictionary.get(term.lower()) is not None:
                termForm = term.lower()
            elif termDictionary.get(term.upper()) is not None:
                termForm = term.upper()
            else:
                continue

            correctPostingFilePath = self.getDocumentsFromPostingFile(termForm)

            temp_document_score_dictionary = self.getDocumentsScoreFromPostingLine(correctPostingFilePath, termForm, int(termDictionary[termForm][2]), useStem = useStem)

            for document, score in temp_document_score_dictionary.items():
                if document_score_dictionary.get(document) is None:
                    document_score_dictionary[document] = score
                else:
                    document_score_dictionary[document] += score

        sorted_dic = sorted(document_score_dictionary.items(), key=lambda kv: kv[1],reverse=True)
        filteredSortedList = self.filterByScores(sorted_dic)
        # limit = 200
        limit = 50
        if len(filteredSortedList) < limit:
            limit = len(filteredSortedList)
        return self.ranker.convertDocNoListToDocID(list(filteredSortedList)[:limit])


    @staticmethod
    def filterByScores(doc_Score_list: list)-> list:
        if len(doc_Score_list) == 0:
            return doc_Score_list
        topScore = doc_Score_list[0][1]
        filterPercent = 0.2
        # filterPercent = 0.4
        threshold = topScore * filterPercent
        index = 0
        for index in range(0,len(doc_Score_list)):
            if doc_Score_list[index][1] < threshold:
                break
        return doc_Score_list[:index]


    @staticmethod
    def getResultFormatFromResultList(qID:str , runID: str, results:list ) -> (str,str):
        resultsToWrite = ''
        resultsToPrint = ""
        resultsForDominant = []
        for index in range(0,len(results)):
            # String to write 'Save Trec_Eval'
            resultsToWrite += str(qID) + ' 0 ' + str(results[index][0]) + ' ' + str(index) + ' ' + str("{0:.3f}".format(round(results[index][1],3))) + ' ' + str(runID) + '\n'


            # String to print in output window
            lineSize = 44
            windowSizes = [7, 24, 10]

            values = [str(qID), str(results[index][0]), str("{0:.3f}".format(round(results[index][1], 3)))]
            for i in range(0, len(values)):
                dif = windowSizes[i] - len(values[i])
                before = int(dif / 2)
                values[i] = ' ' * before + values[i] + ' ' * (dif - before)

            resultsToPrint += "%s|%s|%s\n" % (values[0], values[1], values[2])
            resultsForDominant = [str(qID), str(results[index][0])]

            # resultsToPrint += "  %s  |  %s  |  %s  \n" % (str(qID),str(results[index][0]),str("{0:.3f}".format(round(results[index][1],3))) )
        return resultsToWrite, resultsToPrint, resultsForDominant


    def getDocumentsFromPostingFile(self, term:str) -> str:
        folderAsChar = term[0]
        if not term[0].isalpha():
            folderAsChar = '#'
        savedFilesPath = self.config.getSavedFilesPath() + '/' + folderAsChar + '/PostingFolder/'

        # get the list of posting files for the relevant term
        postingFilesList = os.listdir(savedFilesPath)

        # convert the list to term only
        postingFilesList = [str(file.split('_')[0]) for file in sorted(postingFilesList)]

        # get the correct file
        correctPostingFilePath = ''
        for postingFile in postingFilesList:
            if term <= postingFile:
                correctPostingFilePath = savedFilesPath + postingFile + '_post'
                break

        return correctPostingFilePath



    def getDocumentsScoreFromPostingLine(self, postingFilePath:str, term:str, line:int, useStem = False) -> dict:
        file = open(postingFilePath, 'r', encoding='utf-8')
        fileLine = file.readlines()[line]
        file.close()
        gapAccumulator = 0
        document_rank_dictionary = {}

        if useStem:
            termDictionary = self.termDictionaryWithStem
        else:
            termDictionary = self.termDictionaryNoStem

        TermDocumentsList = fileLine.split(',')
        for documentSegment in TermDocumentsList:
            # docID#DF#positions:
            splitDocumentInfo = documentSegment.split('#')
            gapAccumulator += int(splitDocumentInfo[0])
            if self.documentsByCitiesSet is not None and gapAccumulator not in self.documentsByCitiesSet:
                continue
            termScoreInDoc = self.ranker.getScore(docID=gapAccumulator, docDF=int(splitDocumentInfo[1]), positionList=splitDocumentInfo[2].split(':'), termDF=int(termDictionary[term][0]))
            document_rank_dictionary[gapAccumulator] = termScoreInDoc


        return document_rank_dictionary




# def getDicFromFile(path, sep = '|'):
#
#     try:
#         myFile = open(path,'r')
#
#         with myFile:
#             lines = myFile.readlines()
#             myFile.close()
#             myDict = {}
#
#             for line in lines:
#                 lineAsArray = line.split(sep)
#                 myDict[lineAsArray[0]] = lineAsArray[1:]
#
#             return myDict
#
#     except Exception as ex:
#         print("Error while converting file to Dic, E: ",ex)
#
#
#
#
# def load(config):
#     # TODO - change this function to create a dictionary instead of lists (maybe a dic of the form - term, [df,sumTF,postingLine]
#     savedFolderPath = config.saveFilesWithoutStem
#     lettersList = list(string.ascii_lowercase)
#     lettersList.append('#')
#     totalDict = dict()
#     for letter in lettersList:
#         path = savedFolderPath + '/' + letter + '/' + 'mergedFile_dic'
#         if not os.path.exists(path):
#             print('Location not found', path)
#             return
#         arrayFromFile = getDicFromFile(path=path)
#         if len(totalDict) == 0:
#             totalDict = arrayFromFile
#         else:
#             totalDict.update(arrayFromFile)
#     return totalDict
#
#
# def test():
#     import Configuration
#     config = Configuration.ConfigClass()
#     config.setCorpusPath('C:/Users/doroy/Documents/סמסטר ה/אחזור מידע/עבודה/corpus')
#     config.setSaveMainFolderPath('C:/Users/doroy/Documents/סמסטר ה/אחזור מידע/עבודה/SavedFiles/SavedFiles')
#     termDic = load(config)
#     searcher = Searcher(config, termDic)
#     rankDic = searcher.getDocsForQueryWithExpansion('attracts man walk')
#     print(rankDic)


# test()