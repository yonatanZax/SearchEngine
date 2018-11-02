
import Parsing.Regex as regex


class Parse():

    def __init__(self, indexer):
        self.indexer = indexer
        print("Parse created")

    def parseDoc(self,documentAsSring):
        regex.tokenizeRegex(documentAsSring)

    def getTextFromDoc(self, documentAsString):
        return None

    def parseDocument(self, documentAsSring):
        return None







