
from Parsing.IterativeParsing import IterativeTokenizer
import os

from Ranker.Ranker import Ranker
from Searching.MyWordEmbedder import WordEmbeddingUser


class SearcherIterativeTokenizer(IterativeTokenizer):



    def ruleNBA(self, index, textList):
        # United States America USA -> ["United","States","America","USA","United States America"]

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

        self.wordEmbedding = WordEmbeddingUser(modelPath="SavedModel/mymodel.model")
        if self.wordEmbedding.loadModel():
            print ('WordEmbedding Model was Loaded successfully')

        else:
            print ('There was a problem while loading the WordEmbedding Model  ')
            self.wordEmbedding = None

        self.ranker = Ranker(config)


        dataNoStemLen = 1
        dataWithStemLen = 1
        if dataNoStem is not None:
            dataNoStemLen = len(dataNoStem)
        if dataWithStem is not None:
            dataWithStemLen = len(dataWithStem)

        self.config.setTotalNumberOfTerms(numNoStem=dataNoStemLen,numWithStem=dataWithStemLen)
        self.documentsByCitiesSet = None



    def getDocsForQueryWithExpansion(self, queryString, citiesList=None, expend=False, useStem = False):
        """
        get a query and return the docs in the correct order with expanding of the query using the word embedding
        :param useStem: a flag whether to use stemming on query and use stemming posting file
        :param expend: a flag whether to use the embedding to expand the query.
        :param citiesList: a List containing cities to return files that include one of the cities
        :param queryString: the string of the query given by the user/file
        :return: a list of relevant documents. the list contains a tuple: (docNo, score, docIndex)
        """

        # parse the query
        queryTermDictionary, queryLength = self.iterativeTokenizer.parseText(queryString)
        queryList = list(queryTermDictionary.keys())
        expandedList = []

        # use the correct data depending on the stem state
        if useStem:
            termDictionary = self.termDictionaryWithStem
        else:
            termDictionary = self.termDictionaryNoStem

        # expand the query with wordEmbedding
        if expend:
            expandedList = self.expandQuery(queryList, termDictionary)

        # set the documents we want to retrieve if the user chose cities
        self.documentsByCitiesSet = None
        if len(citiesList) > 0:
            self.documentsByCitiesSet = self.ranker.getDocumentsFromCityList(citiesList=citiesList)

        document_score_dictionary = {}
        # Go through the query terms
        for term in queryList:
            # get the form of the term we want as it is in our data
            termForm = None
            if termDictionary.get(term.lower()) is not None:
                termForm = term.lower()
            elif termDictionary.get(term.upper()) is not None:
                termForm = term.upper()
            else:
                continue

            # get the path to the posting file of the term
            correctPostingFilePath = self.getDocumentsFromPostingFile(termForm)
            # get the line in the posting file
            postingLine = int(termDictionary[termForm][2])
            # gets the files from the posting files and returns then and their score by the current term
            temp_document_score_dictionary = self.getDocumentsScoreFromPostingLine(correctPostingFilePath, termForm, postingLine, useStem = useStem)

            # add the score from the term to the document total score
            for document, score in temp_document_score_dictionary.items():
                if document_score_dictionary.get(document) is None:
                    document_score_dictionary[document] = score
                else:
                    document_score_dictionary[document] += score

        # Go through the terms came back from the WordEmbedding
        for term in expandedList:
            # get the form of the term we want as it is in our data
            termForm = None
            termEmbeddingScore = term[1]
            termNormalization = term[2]
            if termDictionary.get(term[0].lower()) is not None:
                termForm = term[0].lower()
            elif termDictionary.get(term[0].upper()) is not None:
                termForm = term[0].upper()
            else:
                continue

            # get the path to the posting file of the term
            correctPostingFilePath = self.getDocumentsFromPostingFile(termForm)
            # get the line in the posting file
            postingLine = int(termDictionary[termForm][2])
            # gets the files from the posting files and returns then and their score by the current term
            temp_document_score_dictionary = self.getDocumentsScoreFromPostingLine(correctPostingFilePath, termForm, postingLine, useStem = useStem)

            # add the score from the term to the document total score for the terms that came from the expansions
            for document, score in temp_document_score_dictionary.items():
                # normalize the score of the words came back from embedding
                if document_score_dictionary.get(document) is None:
                    document_score_dictionary[document] = score * termEmbeddingScore * termNormalization
                else:
                    document_score_dictionary[document] += ((score * termEmbeddingScore) * termNormalization)

        # sort the dict values by score
        sorted_dic = sorted(document_score_dictionary.items(), key=lambda kv: kv[1],reverse=True)
        # filter the documents that are too irrelevant
        filteredSortedList = self.filterByScores(sorted_dic)

        limit = 50
        # return 50 max documents
        if len(filteredSortedList) < limit:
            limit = len(filteredSortedList)
        #     convert the docs back to their name from indexes numbers
        return self.ranker.convertDocNoListToDocID(list(filteredSortedList)[:limit])



    def expandQuery(self, queryList, termDictionary):
        """
        This function expand the query using the word embedding, filtering what is unnecessary ad the the normalization\n
        :param queryList: a list of the terms of the query\n
        :param termDictionary: the current working dictionary\n
        :return: a list of tuples of words for expansion of the query (term,sim,normalization)\n
        """

        if self.wordEmbedding is None:
            return None
        expandedQuery = []
        # print('The query is: ',queryList)

        for word in queryList:
            try:
                # get the similar words
                mostSimilar = self.wordEmbedding.getTopNSimilarWords(word=word.lower())
                # filter non existing words
                mostSimilarExistingWords = self.getExistingResults(mostSimilar, termDictionary)
                # print("term:", word)
                # print(mostSimilarExistingWords)
                expandedQuery += mostSimilarExistingWords

            except Exception as err:
                pass

        # if len(queryList) > 1:
        #     try:
        #         lowerList = []
        #         for w in queryList:
        #             lowerList.append(w.lower())
        #         mostSimilar = self.wordEmbedding.getTopNSimilarWordsFromList(wordList=lowerList)
        #         mostSimilarExistingWords = self.getExistingResults(mostSimilar, termDictionary)
        #         expandedQuery += mostSimilarExistingWords
        #     except Exception as err:
        #         pass

        # merge words that appear several times and set the normalization and similarity to equal the average of the values
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
    def getExistingResults(mostSimilar, termDictionary):
        """
        checks which words exist in the working dictionary
        :param mostSimilar: words from embedding
        :param termDictionary: working dictionary
        :return:
        """
        finalList = []
        if mostSimilar is not None:
            existingList = []
            # filter non existing words
            for term_sim_tuple in mostSimilar:
                term = term_sim_tuple[0]
                if termDictionary.get(term) is not None:
                    existingList.append(term_sim_tuple)
                elif termDictionary.get(term.upper()) is not None:
                    newTuple = (term.upper(),term_sim_tuple[1])
                    existingList.append(newTuple)


            existingListSize = len(existingList)
            # set the similarity and normalization to be the equal
            if existingListSize > 0:
                for term_sim_tuple in existingList:
                    term = term_sim_tuple[0]
                    score = term_sim_tuple[1]
                    finalList.append([term, score, 1 / existingListSize])
        return finalList




    # ***  Change Percent  ***


    @staticmethod
    def filterByScores(doc_Score_list):
        """
        filter documents that their score is to different from the top document
        :param doc_Score_list: lst of documents
        :return: a filtered list of the same type as received
        """
        if len(doc_Score_list) == 0:
            return doc_Score_list
        topScore = doc_Score_list[0][1]
        # filterPercent = 0.2
        filterPercent = 0.4
        threshold = topScore * filterPercent

        index = 20
        if len(doc_Score_list) <= 20:
            return doc_Score_list

        for index in range(20,len(doc_Score_list)):
            if doc_Score_list[index][1] < threshold:
                break

        return doc_Score_list[0:index]




    def getDocumentsFromPostingFile(self, term):
        """
        gets the path to the posting file depending on the term
        :param term:
        :return: path of the correct file
        """
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



    def getDocumentsScoreFromPostingLine(self, postingFilePath, term, line, useStem = False):
        """
        get the documents from the posting file and runs it through the ranker to get their score
        :param postingFilePath:
        :param term:
        :param line:
        :param useStem:
        :return:
        """

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

        # go through the posting line using the gaps to ge the correct number of the document
        TermDocumentsList = fileLine.split(',')
        for documentSegment in TermDocumentsList:
            # docID#DF#positions:
            splitDocumentInfo = documentSegment.split('#')
            gapAccumulator += int(splitDocumentInfo[0])
            if self.documentsByCitiesSet is not None and gapAccumulator not in self.documentsByCitiesSet:
                continue
            #     get the score from ranker
            termScoreInDoc = self.ranker.getScore(docID=gapAccumulator, docDF=int(splitDocumentInfo[1]), positionList=splitDocumentInfo[2].split(':'), termDF=int(termDictionary[term][0]))
            document_rank_dictionary[gapAccumulator] = termScoreInDoc


        return document_rank_dictionary

