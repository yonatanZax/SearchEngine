import re
from Parsing.IterativeParsing import IterativeTokenizer

class Parse:

    def __init__(self,config):
        self.tokenizer = IterativeTokenizer(config=config)


    def getCityPattern(self, cityAsList):
        regexString = " ".join(cityAsList)

        # regexString = 'r' + regexString
        cityPattern = re.compile()

        return cityPattern

    def replaceCity(self, token):
        return "ZAXROY"

    def parseDoc(self, documentAsString):
        from Indexing.Document import Document

        docNo = 'test'
        cityAsArray = [""]
        try:
            topOfText1 = documentAsString[0:100]
            topOfText2 = documentAsString[0:int(len(documentAsString)/10)]
            docNo = re.findall(r'<DOCNO>(.*?)</DOCNO>', topOfText1)
            if len(docNo) > 0:
                docNo = docNo[0][1:-1]
                # print("#"+docNo+"#")
            else: return None
            countryLine = re.findall(r"<F P=101>(.+?)</F>", topOfText2)
            cityLine = re.findall(r"<F P=104>(.+?)</F>", topOfText2)
            if len(cityLine) > 0:
                cityAsArray = re.findall(r"[a-zA-Z]+", cityLine[0].strip(' '))
            if len(countryLine) > 0:
                country = countryLine[0].strip(' ')
                # documentAsString = documentAsString.replace(city,"ZAXROY")


            onlyText = documentAsString.split("<TEXT>")
            if len(onlyText) > 0:
                documentAsString = onlyText[1]
            else: return None
        except IndexError as e:
            print(e)
            # print("Error - Parse - parseText")
            return None

        termDictionary, docLength = self.tokenizer.getTermDicFromText(documentAsString)
        document =  Document(docNo, termDictionary, docLength, city = cityAsArray[0])
        return document






