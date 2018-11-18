

import re
from Parsing.IterativeParsing import parseText
import MyExecutors

class Parse:

    def __init__(self, indexer):
        self.myIndexer = indexer
        self.cityDic = {}

    def parseDoc(self, documentAsString):
        # print ("parseDoc")
        # docFromRegex = regex.tokenizeRegex(documentAsString)
        docFromRegex = self.parseText(documentAsString)

        self.myIndexer.addNewDoc(document=docFromRegex)
        # MyExecutors._instance.CPUExecutor.apply_async(self.myIndexer.addNewDoc(document=docFromRegex))

        # print(docFromRegex.docNo)


    def parseText(self,text, fromFile = True):
        from Indexing.Document import Document

        docNo = 'test'
        if fromFile:
            try:
                topOfText1 = text[0:50]
                topOfText2 = text[400:500]
                docNo = re.findall(r'<DOCNO>(.*?)</DOCNO>', topOfText1)
                if len(docNo) > 0:
                    docNo = docNo[0]
                    # print(docNo)
                cityLine = re.findall(r"<F P=104>(.+?)</F>",topOfText2)
                if len(cityLine) > 0:
                    city = re.findall(r"[a-zA-Z]+", cityLine[0])[0]
                    self.cityDic[city] = 1
                    # print(cityLine)
                onlyText = text.split("<TEXT>")
                if len(onlyText) > 0:
                    text = onlyText[1]
            except IndexError:
                print("ERROR - Regex - tokenizeRegex")

        termDictionary, docLength = parseText(text)
        return Document(docNo, termDictionary, docLength)



text = '''
<HEADER>
<AU>   FBIS-CHI-94-039 </AU>
Document Type:Daily Report 
<DATE1>  28 Feb 1994 </DATE1>

</HEADER>

<F P=100> HONG KONG &amp; MACAO </F>
<F P=101> Hong Kong </F>
<H3> <TI>   Li Peng Speaks at PWC Meeting in Beijing </TI></H3>
<F P=102>  OW2602155294 Beijing Central Television Program One Network 
in Mandarin 1100 GMT 26 Feb 94 </F>

<F P=103> OW2602155294 </F>
<F P=104>  Beijing Central Television Program One Network 
in Mandarin 1100 GMT 26 Feb 94 </F>



<TEXT>
Language: <F P=105>Mandarin </F>
Article Type:BFN 

<F P=106> [From the "National News Hookup" program] </F>
  [Text] On the evening of 25 February, Premier Li Peng, his 
wife Zhu Lin, Vice Premiers Zou Jiahua and Li Lanqing, and other 
leading comrades spent a happy evening with members of the 
Preliminary Working Committee [PWC] of the Preparatory Committee 
of the Hong Kong SAR at the Hong Kong and Macao Center in 
Beijing. [video opens with a medium shot of a dining hall in 
which many people, including Zou Jiahua, are seated at round 
tables, whereas some of them, including Li Peng and Li Lanqing, 
occupy a long table. Waiters and waitresses are shown serving 
food] 
  At the evening party, Premier Li Peng made remarks on the 
current situation in Hong Kong. [video shows a close shot of Li 
speaking without a written speech while holding a microphone in 
his right hand and partially clenching his left hand into a fist 
and waving the latter while speaking] He said: No matter what 
happens, we are the Chinese people in 1994, not in 1840. 
Today's China is a country with a prosperous economy and a 
stable society. A bright future lies ahead of us. The wheel of 
history is rolling forward, and nobody can resist it. [Li 
smiles after finishing this remark; video shows attendees 
applauding him] 
  Li Peng also noted: Under the current situation, the burden 
is heavier and the responsibility is greater for the PWC. He 
encouraged everybody to work harder and make greater 
contributions to the long-term stability and prosperity of Hong 
Kong and the prosperity of the motherland. This has been a 
report by Beijing Central Television. [video shows shots of Lu 
Ping and attendees at different tables] 

</TEXT>


'''

p = Parse(None)
# p.parseText(text)
