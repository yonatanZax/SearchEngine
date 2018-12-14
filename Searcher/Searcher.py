from Parsing.IterativeParsing import IterativeTokenizer

class SearcherIterativeTokenizer(IterativeTokenizer):

    def ruleNBA(self, index: int, textList: list) -> (list,int):
#         TODO  - change me
        pass



class Searcher:

    def __init__(self,config):
        self.iterativeTokenizer = SearcherIterativeTokenizer(config)


