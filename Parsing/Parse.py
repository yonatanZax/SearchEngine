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
            topOfText1 = documentAsString[0:int(len(documentAsString)/10)]
            topOfText2 = documentAsString[0:int(len(documentAsString)/6)]
            docNo = re.findall(r'<DOCNO>(.*?)</DOCNO>', topOfText1)
            if len(docNo) > 0:
                docNo = docNo[0].strip(' ')
                # print("#"+docNo+"#")
            else: return None
            onlyText = documentAsString.split("<TEXT>")
            if len(onlyText) > 0:
                documentAsString = onlyText[1]
            else: return None

            countryLine = re.findall(r"<F P=101>(.+?)</F>", topOfText2)
            cityLine = re.findall(r"<F P=104>(.+?)</F>", topOfText2)
            if len(cityLine) > 0:
                # cityAsArray = re.findall(r"[a-zA-Z]+", cityLine[0].strip(' '))
                splittedCity =  cityLine[0].strip(' ').split(' ')
                city = splittedCity[0]
                if city.lower() in ['new','san','sao','la','tel','santa','hong','xian']:
                    city = city + ' ' + splittedCity[1].strip(' ')
                if city.isalpha() and city.lower() not in ['bartaman','dokumentation','nezavisimaya']:
                    documentAsString = documentAsString.replace(city, 'ZAXROY')
                else:
                    city = ''
            if len(countryLine) > 0:
                country = countryLine[0].strip(' ')



        except Exception as e:
            print('DocNo: ',docNo)
            print('Error spliting docs in parse, e: ',e)
            # print("Error - Parse - parseText")
            return None


        termDictionary, docLength = self.tokenizer.getTermDicFromText(documentAsString)
        document =  Document(docNo, termDictionary, docLength, city = city)
        return document






