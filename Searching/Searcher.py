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
            if currWord == bigLetters:
                listOfTerms = [' '.join(textList[index:tempIndex])] + textList[index:tempIndex]
                listOfTerms.append(currWord)
                return listOfTerms, tempIndex

            if currWord[0].isupper():
                bigLetters += currWord[0]
                if len(bigLetters) > 6:
                    break
            else:
                break

            tempIndex += 1

        return listOfTerms, index + 1

#         TODO  - change me
        pass



class Searcher:

    def __init__(self, config, termDictionary):
        self.iterativeTokenizer = SearcherIterativeTokenizer(config)
        # form of dictionary: key=term, value=[0-df, 1-sumTF, 2-postingLine]
        self.termDictionary = termDictionary
        self.config = config
        self.ranker = Ranker(config)
        self.config.setTotalNumberOfTerms(len(termDictionary))
        self.wordEmbedding = WordEmbedding()



    def getDocsForQuery(self, queryString):
        """
        get a query and return the docs in the correct order
        :param queryString:
        :return:
        """
        queryTermDictionary, queryLength = self.iterativeTokenizer.parseText(queryString)

        document_score_dictionary = {}
        for term in queryTermDictionary.keys():
            if self.termDictionary.get(term) is not None:
                temp_document_score_dictionary = self.getDocumentsFromPostingFile(term, int(self.termDictionary[term][2]))
                for document, score in temp_document_score_dictionary.items():
                    if document_score_dictionary.get(document) is None:
                        document_score_dictionary[document] = score
                    else:
                        document_score_dictionary[document] += score

        sorted_dic = sorted(document_score_dictionary.items(), key=lambda kv: kv[1],reverse=True)
        limit = 200
        if len(sorted_dic) < limit:
            limit = len(sorted_dic)
        return self.ranker.convertDocNoListToDocID(list(sorted_dic)[:limit])



    def getDocsForQueryWithExpansion(self, queryString: str):
        """
        get a query and return the docs in the correct order with expanding of the query using the word embedding
        :param queryString:
        :return:
        """

        queryTermDictionary, queryLength = self.iterativeTokenizer.parseText(queryString)

        expandedQueryList = self.wordEmbedding.expandQuery(list(queryTermDictionary.keys()))

        document_score_dictionary = {}
        for term in expandedQueryList:
            termForm = None
            if self.termDictionary.get(term.lower()) is not None:
                termForm = term.lower()
            elif self.termDictionary.get(term.upper()) is not None:
                termForm = term.upper()
            else:
                continue
            temp_document_score_dictionary = self.getDocumentsFromPostingFile(termForm, int(self.termDictionary[termForm][2]))
            for document, score in temp_document_score_dictionary.items():
                if document_score_dictionary.get(document) is None:
                    document_score_dictionary[document] = score
                else:
                    document_score_dictionary[document] += score

        sorted_dic = sorted(document_score_dictionary.items(), key=lambda kv: kv[1],reverse=True)
        limit = 200
        # limit = 50
        if len(sorted_dic) < limit:
            limit = len(sorted_dic)
        return self.ranker.convertDocNoListToDocID(list(sorted_dic)[:limit])


    @staticmethod
    def getResultFormatFromResultList(qID:str , runID: str, results:list ) -> (str,str):
        resultsToWrite = ''
        resultsToPrint = "   ID  |     DocNo    |  Score\n"
        for index in range(0,len(results)):
            # String to write 'Save Trec_Eval'
            resultsToWrite += str(qID) + ' 0 ' + str(results[index][0]) + ' ' + str(index) + ' ' + str("{0:.3f}".format(round(results[index][1],3))) + ' ' + str(runID) + '\n'
            # String to print in output window
            resultsToPrint += "  %s  |  %s  |  %s  \n" % (str(qID),str(results[index][0]),str("{0:.3f}".format(round(results[index][1],3))) )
        return resultsToWrite, resultsToPrint


    def getDocumentsFromPostingFile(self, term:str, line:int) -> dict:
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

        return self.getDocumentsScoreFromPostingLine(correctPostingFilePath, line, term)




    def getDocumentsScoreFromPostingLine(self, postingFilePath:str, line:int, term:str) -> dict:
        file = open(postingFilePath, 'r', encoding='utf-8')
        fileLine = file.readlines()[line]
        file.close()
        gapAccumulator = 0
        document_rank_dictionary = {}
        TermDocumentsList = fileLine.split(',')
        for documentSegment in TermDocumentsList:
            # docID#DF#positions:
            splitDocumentInfo = documentSegment.split('#')
            gapAccumulator += int(splitDocumentInfo[0])
            termScoreInDoc = self.ranker.getScore(docID=gapAccumulator, docDF=int(splitDocumentInfo[1]), positionList=splitDocumentInfo[2].split(':'), termDF=int(self.termDictionary[term][0]))
            document_rank_dictionary[gapAccumulator] = termScoreInDoc


        return document_rank_dictionary




def getDicFromFile(path, sep = '|'):

    try:
        myFile = open(path,'r')

        with myFile:
            lines = myFile.readlines()
            myFile.close()
            myDict = {}

            for line in lines:
                lineAsArray = line.split(sep)
                myDict[lineAsArray[0]] = lineAsArray[1:]

            return myDict

    except Exception as ex:
        print("Error while converting file to Dic, E: ",ex)




def load(config):
    # TODO - change this function to create a dictionary instead of lists (maybe a dic of the form - term, [df,sumTF,postingLine]
    savedFolderPath = config.saveFilesWithoutStem
    lettersList = list(string.ascii_lowercase)
    lettersList.append('#')
    totalDict = dict()
    for letter in lettersList:
        path = savedFolderPath + '/' + letter + '/' + 'mergedFile_dic'
        if not os.path.exists(path):
            print('Location not found', path)
            return
        arrayFromFile = getDicFromFile(path=path)
        if len(totalDict) == 0:
            totalDict = arrayFromFile
        else:
            totalDict.update(arrayFromFile)
    return totalDict


def test():
    import Configuration
    config = Configuration.ConfigClass()
    config.setCorpusPath('C:/Users/doroy/Documents/סמסטר ה/אחזור מידע/עבודה/corpus')
    config.setSaveMainFolderPath('C:/Users/doroy/Documents/סמסטר ה/אחזור מידע/עבודה/SavedFiles/SavedFiles')
    termDic = load(config)
    searcher = Searcher(config, termDic)
    rankDic = searcher.getDocsForQuery('attracts')
    print(rankDic)


# test()