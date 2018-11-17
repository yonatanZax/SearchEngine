

import re
from Parsing.IterativeParsing import parseText
import MyExecutors

class Parse:

    def __init__(self, indexer):
        self.myIndexer = indexer

    def parseDoc(self, documentAsString):
        # print ("parseDoc")
        # docFromRegex = regex.tokenizeRegex(documentAsString)
        docFromRegex = self.parseText(documentAsString)

        self.myIndexer.addNewDoc(document=docFromRegex)
        # MyExecutors._instance.CPUExecutor.apply_async(self.myIndexer.addNewDoc(document=docFromRegex))

        # print(docFromRegex.docNo)


    def parseText(self,text, fromFile = True):
        from Indexing.Document import Document

        docNo = 'test'
        if fromFile:
            try:
                docNo = re.findall(r'<DOCNO>(.*?)</DOCNO>', text)[0]
                onlyText = text.split("<TEXT>")[1]
                text = onlyText
            except IndexError:
                print("ERROR - Regex - tokenizeRegex")
            # print(text)

        termDictionary, docLength = parseText(text)
        return Document(docNo, termDictionary, docLength)




