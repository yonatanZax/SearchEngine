
class MyDictionary:

    def __init__(self):
        self.dictionary_term_dicData = {}


    # assuming termString gets in all CAP or all LOW letters already from parser
    def addTerm(self, termString, docNo, termFrequency, termPositions):

        termInDictionary = updateTermToDictionaryByTheRules(self.dictionary_term_dicData, termString)
        termDicData = self.dictionary_term_dicData.get(termInDictionary)
        if termDicData is None:
            # add new term
            termDicData = DictionaryData()
            self.dictionary_term_dicData[termInDictionary] = termDicData
        # add the doc to the term posting line
        termDicData.addDocument(docID=docNo, docTF_int=termFrequency,termPositions= termPositions)


    def getPostingLine(self, term):
        dicData = self.dictionary_term_dicData.get(term)
        if dicData is not None:
            return dicData.postingLine
        return None

    def print(self):
        print("MyDictionary Size: " + str(len(self.dictionary_term_dicData)))
        return



class DictionaryData:

    def __init__(self):
        self.termDF = 0
        self.sumTF = 0
        self.string_docID_tf = ""
        # self.dictionary_docID_tf = {}


    # TODO - (DONE) - something is wrong with the numbers fix it

    def addDocument(self, docID, docTF_int, termPositions):
        self.sumTF += docTF_int
        if self.string_docID_tf.count(str(docID)) > 0:
            splitted = self.string_docID_tf.split(',')
            for doc in splitted:
                splittedDoc = doc.split('#')
                if splittedDoc[0] == docID:
                    oldDF = splittedDoc[1]
                    oldPositions = splittedDoc[2]
                    docTF_int += int(splittedDoc[1])
                    splittedDoc[1] = str(docTF_int)
                    self.string_docID_tf = self.string_docID_tf.replace(splittedDoc[0] + '#' + oldDF+ '#' + oldPositions,splittedDoc[0] + '#' + splittedDoc[1] + splittedDoc[2] + termPositions)
                    print ("addDocument" + str(docID))
                    break

        else:
            self.termDF += 1
            self.string_docID_tf += str(docID) + "#" + str(docTF_int) + "#" +  termPositions + ","
        # self.dictionary_docID_tf[docID] = docTF_int



    def toString(self):
        '''
        posting Format:
        term|DF|sumTF|DOC#TF,*
        '''
        arr = [str(self.termDF),str(self.sumTF), self.string_docID_tf]
        ans = "|".join(arr)

        return ans

    def cleanPostingData(self):
        # with self.lock:
        self.string_docID_tf = ""
        self.sumTF = 0
        self.termDF = 0


class DocumentIndexData:

    def __init__(self, max_tf, uniqueTermsCount, docLength, city = None):
        self.max_tf = max_tf
        self.uniqueTermCount = uniqueTermsCount
        self.docLength = docLength
        self.city = city.upper()

    def toString(self):
        '''
        max_tf|uniqueTermCount|docLength|city
        :return:
        '''
        ans = '|'.join([str(self.max_tf) , str(self.uniqueTermCount), str(self.docLength) ,str(self.city)])
        return ans


class CityIndexData:

    def __init__(self,doc,locations):
        self.country = ''
        self.currency = ''
        self.population = 0
        self.dictionary_doc_locations = {}
        self.dictionary_doc_locations[doc] = locations

    def addDocumentToCity(self, docID, locations):
        self.dictionary_doc_locations[docID] = locations

# get the format of the term how its saved in the dictionary or none if its not in the dictionary
def getTermDictionaryForm(dictionary, termString):
    if not termString[0].isalpha():
        if dictionary.get(termString) is not None:
            return termString
    elif dictionary.get(termString.lower()) is not None:
        return termString.lower()
    elif dictionary.get(termString.upper()) is not None:
        return termString.upper()
    return None

# add or do update to the dictionary like it suppose to and will return the it in the way its suppose to be in the dictionary
def updateTermToDictionaryByTheRules(dictionary, termString):
    termInDictionary = getTermDictionaryForm(dictionary=dictionary,termString=termString)
    ans = termInDictionary
    # if the term already in the dictionary
    if termInDictionary is not None:
        dicData = dictionary[termInDictionary]

        # figure out if the term is suppose to be lower or upper
        if not termString[0].isalpha():
            ans = termString
        # if the term is in CAP in dictionary
        elif termString.upper() == termInDictionary :

            # but not the term string isn't - change the term in dictionary to small
            if termString[0].islower():
                ans = termString.lower()
                dictionary.pop(termInDictionary)
                dictionary[ans] = dicData
        return ans

    else:
        if not termString[0].isalpha():
            ans = termString
        elif len(termString) > 0 and termString[0].isupper():
            ans = termString.upper()
        else:
            ans = termString.lower()
        dictionary[ans] = None
        return ans




def TEST_updateTermToDictionaryByTheRules():
    dic = { "brand": "Ford",
            "MODEL": "Mustang"}

    term = "Brand"
    result = updateTermToDictionaryByTheRules(dic,term)
    print ("1. " + str(result == "brand"))

    result = updateTermToDictionaryByTheRules(dic, "Model")
    print ("2. " + str(result == "MODEL"))

    result = updateTermToDictionaryByTheRules(dic, "model")
    print ("3. " + str(result == "model"))


def TEST_addTerm():
    myDic = MyDictionary()
    myDic.addTerm(termString="one", docNo=1, termFrequency=3 )
    myDic.print()
    myDic.addTerm(termString="One",docNo=2,termFrequency=2)
    myDic.print()
    myDic.addTerm(termString="Two", docNo=2, termFrequency=2)
    myDic.print()
    myDic.addTerm(termString="two", docNo=3, termFrequency=3)
    myDic.print()

# TEST_updateTermToDictionaryByTheRules()
# TEST_addTerm()