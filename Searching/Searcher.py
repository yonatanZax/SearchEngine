import string

from Parsing.IterativeParsing import IterativeTokenizer
import os

from Ranker.Ranker import Ranker
from Searching.WordEmbedding import WordEmbedding
from Searching.MyWordEmbedder import WordEmbeddingUser


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
        self.wordEmbedding = WordEmbeddingUser('../../../../SavedModel/mymodel.model.wv.syn0.npy')
        if self.wordEmbedding.loadModel():
            print ('WordEmbedding Model was Loaded successfully')

        else:
            print ('There was a problem while loading the WordEmbedding Model  ')
            self.wordEmbedding = None

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
        :param useStem:
        :param expend:
        :param citiesList:
        :param queryString:
        :return:
        """

        queryTermDictionary, queryLength = self.iterativeTokenizer.parseText(queryString)
        queryList = list(queryTermDictionary.keys())
        expandedList = []

        if useStem:
            termDictionary = self.termDictionaryWithStem
        else:
            termDictionary = self.termDictionaryNoStem

        if expend:
            expandedList = self.expandQuery(queryList, termDictionary)

        self.documentsByCitiesSet = None
        if len(citiesList) > 0:
            self.documentsByCitiesSet = self.ranker.getDocumentsFromCityList(citiesList=citiesList)

        document_score_dictionary = {}
        # Go through the query terms
        for term in queryList:
            termForm = None
            if termDictionary.get(term.lower()) is not None:
                termForm = term.lower()
            elif termDictionary.get(term.upper()) is not None:
                termForm = term.upper()
            else:
                continue

            correctPostingFilePath = self.getDocumentsFromPostingFile(termForm)
            postingLine = int(termDictionary[termForm][2])
            temp_document_score_dictionary = self.getDocumentsScoreFromPostingLine(correctPostingFilePath, termForm, postingLine, useStem = useStem)

            for document, score in temp_document_score_dictionary.items():
                if document_score_dictionary.get(document) is None:
                    document_score_dictionary[document] = score
                else:
                    document_score_dictionary[document] += score

        # Go through the terms came back from the WordEmbedding
        for term in expandedList:
            termForm = None
            termEmbeddingScore = term[1]
            termNormalization = term[2]
            if termDictionary.get(term[0].lower()) is not None:
                termForm = term[0].lower()
            elif termDictionary.get(term[0].upper()) is not None:
                termForm = term[0].upper()
            else:
                continue

            correctPostingFilePath = self.getDocumentsFromPostingFile(termForm)
            postingLine = int(termDictionary[termForm][2])
            temp_document_score_dictionary = self.getDocumentsScoreFromPostingLine(correctPostingFilePath, termForm, postingLine, useStem = useStem)

            for document, score in temp_document_score_dictionary.items():
                if document_score_dictionary.get(document) is None:
                    document_score_dictionary[document] = score * termEmbeddingScore * termNormalization
                else:
                    document_score_dictionary[document] += ((score * termEmbeddingScore) * termNormalization)

        sorted_dic = sorted(document_score_dictionary.items(), key=lambda kv: kv[1],reverse=True)
        filteredSortedList = self.filterByScores(sorted_dic)

        limit = 50

        if len(filteredSortedList) < limit:
            limit = len(filteredSortedList)
        return self.ranker.convertDocNoListToDocID(list(filteredSortedList)[:limit])


    def expandQuery(self, queryList:list, termDictionary:dict)->list or None:
        if self.wordEmbedding is None:
            return None
        expandedQuery = []
        print('The query is: ',queryList)

        for word in queryList:
            try:
                mostSimilar = self.wordEmbedding.getTopNSimilarWords(word=word.lower())
                mostSimilarExistingWords = self.getExistingResults(mostSimilar, termDictionary)
                print ('Existing words in Embedding for the term: ', word.lower())
                for term_sim_tuple in mostSimilarExistingWords:
                    print ('\t\t' + term_sim_tuple[0],term_sim_tuple[1])
                expandedQuery += mostSimilarExistingWords

            except Exception as err:
                pass

        if len(queryList) > 1:
            try:
                lowerList = []
                for w in queryList:
                    lowerList.append(w.lower())
                mostSimilar = self.wordEmbedding.getTopNSimilarWordsFromList(wordList=lowerList)
                mostSimilarExistingWords = self.getExistingResults(mostSimilar, termDictionary)
                expandedQuery += mostSimilarExistingWords
            except Exception as err:
                pass
        finalExtendedQuery = {}
        for term_sim_appearance in expandedQuery:
            term = term_sim_appearance[0]
            sim = term_sim_appearance[1]
            appearance = term_sim_appearance[2]
            if finalExtendedQuery.get(term) is None:
                finalExtendedQuery[term] = (term,sim,appearance,0)
                continue
            numberOfAverage = finalExtendedQuery[term][3]
            newAverageSim = (sim + ((numberOfAverage + 1) * finalExtendedQuery[term][1]) ) / (numberOfAverage + 2)
            newAppearance = (appearance + ((numberOfAverage + 1) * finalExtendedQuery[term][2]) ) / (numberOfAverage + 2)
            finalExtendedQuery[term] = (term, newAverageSim, newAppearance, numberOfAverage + 1)

        return finalExtendedQuery.values()


    @staticmethod
    def getExistingResults(mostSimilar:list, termDictionary:dict)->list:
        finalList = []
        if mostSimilar is not None:
            existingList = []
            for term_sim_tuple in mostSimilar:
                term = term_sim_tuple[0]
                if termDictionary.get(term) is not None:
                    existingList.append(term_sim_tuple)
            existingListSize = len(existingList)
            if existingListSize > 0:
                for term_sim_tuple in existingList:
                    term = term_sim_tuple[0]
                    score = term_sim_tuple[1]
                    finalList.append([term, score, 1 / existingListSize])
        return finalList

    @staticmethod
    def filterByScores(doc_Score_list: list)-> list:
        if len(doc_Score_list) == 0:
            return doc_Score_list
        topScore = doc_Score_list[0][1]
        filterPercent = 0.05
        # filterPercent = 0.4
        threshold = topScore * filterPercent
        index = 0
        for index in range(0,len(doc_Score_list)):
            if doc_Score_list[index][1] < threshold:
                break
        return doc_Score_list[:index]




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

        if useStem:
            termDictionary = self.termDictionaryWithStem
        else:
            termDictionary = self.termDictionaryNoStem


        file = open(postingFilePath, 'r', encoding='utf-8')
        linesFromFile = file.readlines()
        file.close()

        fileLine = linesFromFile[line]


        gapAccumulator = 0
        document_rank_dictionary = {}


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

