
import re
import Parsing.Regex as regex


class Parse():

    def __init__(self, indexer):
        self.indexer = indexer
        print("Parse created")

    def parseDoc(self,documentAsSring):
        regex.tokenizeRegex(documentAsSring)








