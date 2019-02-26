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
        language = ''
        try:
            tagDic = getTagDicFromDocument(documentAsString)
            if tagDic:
                if not tagDic.get('text') is None:
                    if len(tagDic.get('text')) > 10:
                        onlyText = tagDic.get('text')


                        # Add new doc to 'allDocsDic'
                        docNo = tagDic['docNo']


                        # Add new city to the cities dictionary
                        if not tagDic.get('city') == '':
                            city = tagDic.get('city')

                        # onlyText = tagDic.get('text')
                        language = tagDic.get('language')

                    else:
                        return None
                else:
                    return None



        except Exception as e:
            return None


        termDictionary, docLength = self.tokenizer.getTermDicFromText(onlyText)
        if len(tagDic['title']) > 1:
            titleTermDictionary, titleLength = self.tokenizer.getTermDicFromText(tagDic['title'])
            termDictionary = self.addTitleToDic(termDictionary, titleTermDictionary)
        document =  Document(docNo, termDictionary, docLength, city = city,language=language)
        return document


    @staticmethod
    def addTitleToDic(termDictionary, titleTermDictionary):
        from Indexing.Document import TermData
        for term in titleTermDictionary.keys():
            if termDictionary.get(term.lower()) is not None:
                termDictionary[term.lower()].setInTitle()
            elif termDictionary.get(term.upper()) is not None:
                termDictionary[term.upper()].setInTitle()
            else:
                termDictionary[term] = TermData(1, '-')
        return termDictionary

