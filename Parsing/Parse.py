import re
from Parsing.IterativeParsing import IterativeTokenizer

class Parse:

    def __init__(self,config):
        self.tokenizer = IterativeTokenizer(config=config)


    def parseDoc(self, documentAsString):
        from Indexing.Document import Document

        docNo = 'doc null'
        city = ''
        try:
            topOfText1 = documentAsString[0:int(len(documentAsString)/6)]
            topOfText2 = documentAsString[0:int(len(documentAsString)/6)]
            # docNo = re.findall(r'<DOCNO>(.*?)</DOCNO>', topOfText1)
            docNo = documentAsString[documentAsString.find('<DOCNO>') + len('<DOCNO>'):documentAsString.rfind('</DOCNO>')]
            if len(docNo) > 2:
                docNo = docNo.strip(' ')
                # print("#"+docNo+"#")
            else: return None
            onlyText = documentAsString[documentAsString.find('<TEXT>') + len('<TEXT>'):documentAsString.rfind('</TEXT>')]
            if len(onlyText) < 20:
                return None

            countryLine = documentAsString[documentAsString.find('<F P=101>') + len('<F P=101>'):documentAsString.rfind('</F>')]
            # countryLine = re.findall(r"<F P=101>(.+?)</F>", topOfText2)
            cityLine = documentAsString[documentAsString.find('<F P=104>') + len('<F P=104>'):documentAsString.rfind('</F>')]
            # cityLine = re.findall(r"<F P=104>(.+?)</F>", topOfText2)
            if len(cityLine) > 2:
                # cityAsArray = re.findall(r"[a-zA-Z]+", cityLine[0].strip(' '))
                splittedCity =  cityLine.strip(' ').split(' ')
                city = splittedCity[0]
                if city.lower() in ['new','san','sao','la','tel','santa','hong','xian']:
                    city = city + ' ' + splittedCity[1].strip(' ')
                if city.isalpha() and city.lower() not in ['bartaman','dokumentation','nezavisimaya']:
                    documentAsString = documentAsString.replace(city, 'ZAXROY')
                else:
                    city = ''
            if len(countryLine) > 2:
                country = countryLine.strip(' ')



        except Exception as e:
            print('DocNo: ',docNo)
            print('Error spliting docs in parse, e: ',e)
            # print("Error - Parse - parseText")
            return None


        termDictionary, docLength = self.tokenizer.getTermDicFromText(onlyText)
        document =  Document(docNo, termDictionary, docLength, city = city)
        return document






