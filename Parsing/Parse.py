import re
from Parsing.IterativeParsing import IterativeTokenizer

class Parse:

    def __init__(self,config):
        self.tokenizer = IterativeTokenizer(config=config)

        self.keepGoingCityDic = {'new','san','sao','la','tel','santa','hong','xian','cape','rio','buenos','panama','mexico','guatemala','abu'}

        self.avoidCities = {'bartaman','dokumentation','nezavisimaya','calcutta','the','air'}


    def parseDoc(self, documentAsString):
        from Indexing.Document import Document

        docNo = 'doc null'
        city = ''
        cityLine = ''
        language = ''
        languageLine = ''
        try:
            docNo = documentAsString[documentAsString.find('<DOCNO>') + len('<DOCNO>'):documentAsString.rfind('</DOCNO>')]
            if len(docNo) > 2:
                docNo = docNo.strip(' ')
                # print("#"+docNo+"#")
            else: return None
            textLabelIndex = documentAsString.find('<TEXT>')
            onlyText = documentAsString[textLabelIndex + len('<TEXT>'):documentAsString.rfind('</TEXT>')]
            findTextSquared = onlyText.find('[Text]')
            if findTextSquared > 0:
                onlyText = onlyText[findTextSquared + len('[Text]'):]
                textLabelIndex = findTextSquared
            if len(onlyText) < 15:
                return None

            # countryLine = documentAsString[documentAsString.find('<F P=101>') + len('<F P=101>'):documentAsString.find('</F>')]
            # countryLine = re.findall(r"<F [Pp]=101>(.+?)</F>", documentAsString)
            cityStart = documentAsString.find('<F P=104>')
            if cityStart > 0:
                cityEnd = documentAsString[cityStart:].find('</F>')
                cityLine = documentAsString[cityStart + len('<F P=104>'): cityStart + cityEnd]
            # cityLine = documentAsString[documentAsString.find('<F P=104>') + len('<F P=104>'):documentAsString.find('</F>')]
            # cityLine = re.findall(r"<F [Pp]=104>(^((?!</F>).)*)", documentAsString)
            # languageLine = documentAsString[documentAsString.find('<F P=105>') + len('<F P=105>'):documentAsString.find('</F>')]
            languageStart = documentAsString.find('<F P=105>')
            if languageStart > 0:
                languageEnd = documentAsString[languageStart:].find('</F>')
                languageLine = documentAsString[languageStart + len('<F P=105>'): languageStart + languageEnd]


            if len(cityLine) > 1 :
                splittedCity =  cityLine.replace('\n',' ').strip(' ').split(' ')
                city = splittedCity[0]
                if city.lower() in self.keepGoingCityDic and len(splittedCity) > 1:
                    city = city + ' ' + splittedCity[1].strip(' ')
                    if len(splittedCity) > 2 and splittedCity[1].lower() in ['de']:
                        city = city + ' ' + splittedCity[2].strip(' ')

                if city.isalpha() and city.lower() not in self.avoidCities:
                    onlyText = onlyText.replace(city, 'ZAXROY')
                else:
                    city = ''
            # if len(countryLine) > 0:
            #     country = countryLine[0].strip(' ')

            if len(languageLine) > 0 :
                languageLine = languageLine.replace('\n',' ').strip(' ').split(' ')[0]
                if len(languageLine) > 1 and languageLine[0].isupper():
                    tempLanguage = languageLine[0]
                    for l in languageLine[1:]:
                        if l.isalpha():
                            tempLanguage += l
                        else: break

                    if len(tempLanguage) > 2:
                        language = languageLine



        except Exception as e:
            print('DocNo: ',docNo)
            print('Error spliting docs in parse, e: ',e)
            # print("Error - Parse - parseText")
            return None


        termDictionary, docLength = self.tokenizer.getTermDicFromText(onlyText)
        document =  Document(docNo, termDictionary, docLength, city = city,language=language)
        return document






