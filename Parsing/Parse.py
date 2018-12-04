import re
from Parsing.IterativeParsing import IterativeTokenizer

class Parse:

    def __init__(self,config):
        self.tokenizer = IterativeTokenizer(config=config)


    def parseDoc(self, documentAsString):
        from Indexing.Document import Document

        docNo = 'doc null'
        city = ''
        language = ''
        try:
            docNo = documentAsString[documentAsString.find('<DOCNO>') + len('<DOCNO>'):documentAsString.rfind('</DOCNO>')]
            if len(docNo) > 2:
                docNo = docNo.strip(' ')
                # print("#"+docNo+"#")
            else: return None
            onlyText = documentAsString[documentAsString.find('<TEXT>') + len('<TEXT>'):documentAsString.rfind('</TEXT>')]
            if len(onlyText) < 20:
                return None

            # countryLine = documentAsString[documentAsString.find('<F P=101>') + len('<F P=101>'):documentAsString.find('</F>')]
            countryLine = re.findall(r"<F P=101>(.+?)</F>", documentAsString[:int(len(documentAsString)/4)])
            # cityLine = documentAsString[documentAsString.find('<F P=104>') + len('<F P=104>'):documentAsString.find('</F>')]
            cityLine = re.findall(r"<F P=104>(.+?)</F>", documentAsString[:int(len(documentAsString)/4)])
            # languageLine = documentAsString[documentAsString.find('<F P=105>') + len('<F P=105>'):documentAsString.find('</F>')]
            languageLine = re.findall(r"<F P=105>(.+?)</F>", documentAsString[:int(len(documentAsString)/4)])

            if len(cityLine) > 0 :
                # cityAsArray = re.findall(r"[a-zA-Z]+", cityLine[0].strip(' '))
                splittedCity =  cityLine[0].strip(' ').split(' ')
                city = splittedCity[0]
                if city.lower() in ['new','san','sao','la','tel','santa','hong','xian','cape']:
                    city = city + ' ' + splittedCity[1].strip(' ')
                if city.isalpha() and city.lower() not in ['bartaman','dokumentation','nezavisimaya','calcutta']:
                    documentAsString = documentAsString.replace(city, 'ZAXROY')
                else:
                    city = ''
            if len(countryLine) > 0:
                country = countryLine[0].strip(' ')

            if len(languageLine) > 0 :
                languageLine = languageLine[0].strip(' ')
                if languageLine[0].isalpha():
                    language = languageLine



        except Exception as e:
            print('DocNo: ',docNo)
            print('Error spliting docs in parse, e: ',e)
            # print("Error - Parse - parseText")
            return None


        termDictionary, docLength = self.tokenizer.getTermDicFromText(onlyText)
        document =  Document(docNo, termDictionary, docLength, city = city,language=language)
        return document





