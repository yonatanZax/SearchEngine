import re
from Parsing.IterativeParsing import IterativeTokenizer

class Parse:

    def __init__(self,config):
        self.tokenizer = IterativeTokenizer(config=config)

    def parseDoc(self, documentAsString):
        from Indexing.Document import Document

        docNo = 'test'
        city = ""
        try:
            topOfText1 = documentAsString[0:50]
            topOfText2 = documentAsString[0:int(len(documentAsString)/10)]
            docNo = re.findall(r'<DOCNO>(.*?)</DOCNO>', topOfText1)
            if len(docNo) > 0:
                docNo = docNo[0][1:-1]
                # print("#"+docNo+"#")
            else: return None
            cityLine = re.findall(r"<F P=104>(.+?)</F>", topOfText2)
            if len(cityLine) > 0:
                city = re.findall(r"[a-zA-Z]+", cityLine[0])[0]
                # print(cityLine)
            onlyText = documentAsString.split("<TEXT>")
            if len(onlyText) > 0:
                documentAsString = onlyText[1]
            else: return None
        except IndexError:
            # print("Error - Parse - parseText")
            return None

        termDictionary, docLength = self.tokenizer.getTermDicFromText(documentAsString)
        document =  Document(docNo, termDictionary, docLength, city = city)
        return document






