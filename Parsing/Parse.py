

import Parsing.Regex as regex


class Parse:

    def __init__(self, indexer):
        self.myIndexer = indexer

    def parseDoc(self, documentAsString):
        # print ("parseDoc")
        docFromRegex = regex.tokenizeRegex(documentAsString)
        documentDictionary = docFromRegex.termDocDictionary_term_termData
        docNo = docFromRegex.docNo
        for term, termData in documentDictionary.items():
            # add the term to the dictionary
            self.myIndexer.addTermToDictionary(term, docNo, termData.termFrequency)
        # self.myIndexer.addNewDoc( document=docFromRegex)

        # print(docFromRegex.docNo)







