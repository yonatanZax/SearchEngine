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
            findTextSquared = onlyText.find('[Text]')
            if findTextSquared > 0:
                onlyText = onlyText[findTextSquared + len('[Text]'):]
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



# from Configuration import ConfigClass
# configClass = ConfigClass()
# p = Parse(configClass)

text = '''
<DOC>
<DOCNO> FBIS3-3366 </DOCNO>
<HT>    "drchi054_k_94010" </HT>


<HEADER>
<AU>   FBIS-CHI-94-054 </AU>
Document Type:Daily Report 
<DATE1>  19 Mar 1994 </DATE1>

</HEADER>

<F P=100> Political &amp; Social </F>
<H3> <TI>   CPPCC Second Session Adopts Amended Charter </TI></H3>
<F P=102>  OW1903234794 Beijing XINHUA Domestic Service in Chinese 0921 
GMT 19 Mar 94 </F>

<F P=103> OW1903234794 </F>
<F P=104>  Beijing XINHUA Domestic Service </F>


<TEXT>
Language: <F P=105> Chinese </F>
Article Type:BFN 

  [Text] Beijing, 19 Mar (XINHUA) -- Resolution of the Second 
Session of the Eighth National Committee of the Chinese People's 
Political Consultative Conference [CPPCC] on the (amended) 
"Charter of the Chinese People's Political Consultative 
Conference" 
  (Adopted by the Second Session of the Eighth CPPCC National 
Committee on 19 March 1994) 
  The Second Session of the Eighth CPPCC National Committee 
has 
decided: The (amended) "Charter of the Chinese People's 
Political Consultative Conference" proposed by the Standing 
Committee of the CPPCC National Committee is adopted, and the 
amended "Charter of the Chinese People's Political Consultative 
Conference" shall take effect as of today. 

</TEXT>

</DOC>

'''


# dic = p.parseDoc(text)
# doc = dic.termDocDictionary_term_termData
# for term,data in doc.items():
#     print(term, ', Locations (gaps) : ', data.toString())
#



