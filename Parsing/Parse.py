from Parsing.IterativeParsing import IterativeTokenizer
from BasicMethods import getTagFromText
from PreRun import getTagDicFromDocument

class Parse:

    def __init__(self,config):
        self.tokenizer = IterativeTokenizer(config=config)

        self.keepGoingCityDic = {'new','san','sao','la','tel','santa','hong','xian','cape','rio','buenos','panama','mexico','guatemala','abu'}

        self.avoidCities = {'bartaman','dokumentation','nezavisimaya','calcutta','the','air'}


    def parseDoc(self, documentAsString):
        from Indexing.Document import Document

        docNo = 'doc null'
        onlyText = ''
        city = ''
        cityLine = ''
        language = ''
        languageLine = ''
        try:

            tagDic = getTagDicFromDocument(documentAsString)
            if tagDic:
                if not tagDic.get('text') is None:
                    if len(tagDic.get('text')) > 10:
                        onlyText = tagDic.get('text')

                        # findTextSquared = onlyText.find('[Text]')
                        # if findTextSquared > 0:
                        #     onlyText = onlyText[findTextSquared + len('[Text]'):]
                        # if len(onlyText) <= 10:
                        #     return None

                        # Add new doc to 'allDocsDic'
                        docNo = tagDic['docNo']




                        # Add new city to the cities dictionary
                        if not tagDic.get('city') == '':
                            cityLine = tagDic.get('city')

                        # onlyText = tagDic.get('text')
                        language = tagDic.get('language')

                    else:
                        return None
                else:
                    return None




            # # Todo - change find methods to getTagFromText in basicMethods
            # # docNo = getTagFromText(documentAsString,tag1='<DOCNO>',tag2='</DOCNO>')
            # docNo = documentAsString[documentAsString.find('<DOCNO>') + len('<DOCNO>'):documentAsString.rfind('</DOCNO>')]
            # if len(docNo) > 2:
            #     docNo = docNo.strip(' ')
            #     # print("#"+docNo+"#")
            # else: return None
            # textLabelIndex = documentAsString.find('<TEXT>')
            # onlyText = documentAsString[textLabelIndex + len('<TEXT>'):documentAsString.rfind('</TEXT>')]
            # findTextSquared = onlyText.find('[Text]')
            # if findTextSquared > 0:
            #     onlyText = onlyText[findTextSquared + len('[Text]'):]
            # if len(onlyText) < 15:
            #     return None
            #
            # cityStart = documentAsString.find('<F P=104>')
            # if cityStart > 0:
            #     cityEnd = documentAsString[cityStart:].find('</F>')
            #     cityLine = documentAsString[cityStart + len('<F P=104>'): cityStart + cityEnd]
            #
            # languageStart = documentAsString.find('<F P=105>')
            # if languageStart > 0:
            #     languageEnd = documentAsString[languageStart:].find('</F>')
            #     languageLine = documentAsString[languageStart + len('<F P=105>'): languageStart + languageEnd]
            #
            #
            # if len(cityLine) > 1 :
            #     splittedCity =  cityLine.replace('\n',' ').strip(' ').split(' ')
            #     city = splittedCity[0]
            #     if city.lower() in self.keepGoingCityDic and len(splittedCity) > 1:
            #         city = city + ' ' + splittedCity[1].strip(' ')
            #         if len(splittedCity) > 2 and splittedCity[1].lower() in ['de']:
            #             city = city + ' ' + splittedCity[2].strip(' ')
            #
            #     if city.isalpha() and city.lower() not in self.avoidCities:
            #         onlyText = onlyText.replace(city, 'ZAXROY')
            #     else:
            #         city = ''
            #
            # if len(languageLine) > 0 :
            #     languageLine = languageLine.replace('\n',' ').strip(' ').split(' ')[0]
            #     if len(languageLine) > 1 and languageLine[0].isupper():
            #         tempLanguage = languageLine[0]
            #         for l in languageLine[1:]:
            #             if l.isalpha():
            #                 tempLanguage += l
            #             else: break
            #
            #         if len(tempLanguage) > 2:
            #             language = languageLine



        except Exception as e:
            # print('DocNo: ',docNo)
            # print('Error spliting docs in parse, e: ',e)
            # print("Error - Parse - parseText")
            return None


        termDictionary, docLength = self.tokenizer.getTermDicFromText(onlyText)
        document =  Document(docNo, termDictionary, docLength, city = city,language=language)
        return document






