import multiprocessing
import concurrent.futures.process
import threading

class MyDictionary:

    def __init__(self):
        self.dictionary_term_dicData = {}
        # self.lock = multiprocessing.RLock()
        # self.lock = threading.RLock()

    # assuming termString gets in all CAP or all LOW letters already from parser
    def addTerm(self, termString, docNo, termFrequency):
        # self.lock.acquire()
        # termInDictionary = updateTermToDictionaryByTheRules(self.dictionary_term_dicData, termString)
        # termDicData = self.dictionary_term_dicData.get(termInDictionary)
        # if termDicData is None:
        #     # add new term
        #     termDicData = DictionaryData(len(self.dictionary_term_dicData))
        #     self.dictionary_term_dicData[termInDictionary] = termDicData
        # self.lock.release()
        # # add the doc to the term posting line
        # termDicData.addDocument(docID=docNo, docTF_int=termFrequency)

        # with self.lock:
        #     termInDictionary = updateTermToDictionaryByTheRules(self.dictionary_term_dicData, termString)
        #     termDicData = self.dictionary_term_dicData.get(termInDictionary)
        #     if termDicData is None:
        #         # add new term
        #         termDicData = DictionaryData(len(self.dictionary_term_dicData))
        #         self.dictionary_term_dicData[termInDictionary] = termDicData
        # # add the doc to the term posting line
        # termDicData.addDocument(docID=docNo, docTF_int=termFrequency)

        termInDictionary = updateTermToDictionaryByTheRules(self.dictionary_term_dicData, termString)
        termDicData = self.dictionary_term_dicData.get(termInDictionary)
        if termDicData is None:
            # add new term
            termDicData = DictionaryData(len(self.dictionary_term_dicData))
            self.dictionary_term_dicData[termInDictionary] = termDicData
        # add the doc to the term posting line
        termDicData.addDocument(docID=docNo, docTF_int=termFrequency)


    def getPostingLine(self, term):
        dicData = self.dictionary_term_dicData.get(term)
        if dicData is not None:
            return dicData.postingLine
        return None

    def print(self):
        print("MyDictionary Size: " + str(len(self.dictionary_term_dicData)))
        return
        for term, termData in sorted(self.dictionary_term_dicData.items()):
            print(term + " - " + termData.toString())
        print("MyDictionary Size: " + str(len(self.dictionary_term_dicData)))


class DictionaryData:

    def __init__(self, postingLine):
        self.termDF = 0
        self.sumTF = 0
        self.postingLine = postingLine
        self.string_docID_tf = ""
        # self.dictionary_docID_tf = {}
        # self.lock = multiprocessing.RLock()
        # self.lock = threading.RLock()


    def addDocument(self, docID, docTF_int):
        # self.lock.acquire()
        self.termDF += 1
        self.sumTF += docTF_int
        self.string_docID_tf += str(docID) + "#" + str(docTF_int) + ","
        # self.dictionary_docID_tf[docID] = docTF_int
        # self.lock.release()

        # with self.lock:
        #     self.termDF += 1
        #     self.sumTF += docTF_int
        #     self.dictionary_docID_tf[docID] = docTF_int

    def toString(self):
        '''
        posting Format:
        term|DF|sumTF|DOC#TF,*
        '''
        arr = [str(self.termDF),str(self.sumTF), self.string_docID_tf.strip(',')]
        ans = "|".join(arr)

        return ans

    def cleanPostingData(self):
        # with self.lock:
        self.string_docID_tf = ""


class DocumentIndexData:

    def __init__(self, max_tf, uniqueTermsCount, docLength, city = None):
        self.max_tf = max_tf
        self.uniqueTermCount = uniqueTermsCount
        self.docLength = docLength
        self.city = city


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