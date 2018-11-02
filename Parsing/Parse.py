
from Indexing.Document import Document
from Indexing.Indexer import Indexer
import Parsing.Regex as regex


class Parse():

    def __init__(self, indexer):
        self.myIndexer = indexer

    def parseDoc(self,documentAsSring):
        regexData = regex.tokenizeRegex(documentAsSring)
        newDoc = Document(regexData[0], regexData[1])
        self.myIndexer.addNewDoc(newDoc)








