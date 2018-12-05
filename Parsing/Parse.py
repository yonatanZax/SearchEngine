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
        language = ''
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
            if len(onlyText) < 20:
                return None

            # countryLine = documentAsString[documentAsString.find('<F P=101>') + len('<F P=101>'):documentAsString.find('</F>')]
            countryLine = re.findall(r"<F P=101>(.+?)</F>", documentAsString[:textLabelIndex])
            # cityLine = documentAsString[documentAsString.find('<F P=104>') + len('<F P=104>'):documentAsString.find('</F>')]
            cityLine = re.findall(r"<F P=104>(.+?)</F>", documentAsString[:textLabelIndex])
            # languageLine = documentAsString[documentAsString.find('<F P=105>') + len('<F P=105>'):documentAsString.find('</F>')]
            languageLine = re.findall(r"<F P=105>(.+?)</F>", documentAsString[:textLabelIndex])

            if len(cityLine) > 0 :
                # cityAsArray = re.findall(r"[a-zA-Z]+", cityLine[0].strip(' '))
                splittedCity =  cityLine[0].strip(' ').split(' ')
                city = splittedCity[0]
                if city.lower() in self.keepGoingCityDic and len(splittedCity) > 1:
                    city = city + ' ' + splittedCity[1].strip(' ')
                    if len(splittedCity) > 2 and splittedCity[1].lower() in ['de']:
                        city = city + ' ' + splittedCity[2].strip(' ')

                if city.isalpha() and city.lower() not in self.avoidCities:
                    onlyText = onlyText.replace(city, 'ZAXROY')
                else:
                    city = ''
            if len(countryLine) > 0:
                country = countryLine[0].strip(' ')

            if len(languageLine) > 0 :
                languageLine = languageLine[0].strip(' ').split(' ')[0]
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


#
# from Configuration import ConfigClass
# configClass = ConfigClass()
# p = Parse(configClass)

text = '''


'''

#
# dic = p.parseDoc(text)
# doc = dic.termDocDictionary_term_termData
# for term,data in doc.items():
#     print(term, ', Locations (gaps) : ', data.toString())




