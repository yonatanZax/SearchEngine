

import Parsing.Regex as regex


class Parse:

    def __init__(self, indexer):
        self.myIndexer = indexer

    def parseDoc(self, documentAsString):
        # print ("parseDoc")
        docFromRegex = regex.tokenizeRegex(documentAsString)
        print(docFromRegex.docNo)

        self.myIndexer.addNewDoc( document=docFromRegex)
        # print(docFromRegex.docNo)







