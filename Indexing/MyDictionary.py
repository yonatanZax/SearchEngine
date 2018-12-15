
class MyDictionary:

    def __init__(self):
        self.dictionary_term_dicData = {}


    # assuming termString gets in all CAP or all LOW letters already from parser
    def addTerm(self, termString, docNo, termFrequency, termPositions,docNoAsIndex=0):

        termInDictionary = updateTermToDictionaryByTheRules(self.dictionary_term_dicData, termString)
        termDicData = self.dictionary_term_dicData.get(termInDictionary)
        if termDicData is None:
            # add new term
            termDicData = DictionaryData()
            self.dictionary_term_dicData[termInDictionary] = termDicData

        # add the doc to the term posting line
        termDicData.addDocument(docID=docNoAsIndex, docTF_int=termFrequency,termPositions= termPositions)




class DictionaryData:

    def __init__(self):
        self.termDF = 0
        self.sumTF = 0
        self.string_docID_tf_positions = ""



    def addDocument(self, docID, docTF_int, termPositions):
        self.sumTF += docTF_int
        self.termDF += 1
        self.string_docID_tf_positions += str(docID) + "#" + str(docTF_int) + "#" + termPositions + ","



    def toString(self):
        '''
        posting Format:
        term|DF|sumTF|DOC#TF,*
        '''
        arr = [str(self.termDF), str(self.sumTF), self.string_docID_tf_positions]
        ans = "|".join(arr)

        return ans

    def cleanPostingData(self):
        self.string_docID_tf_positions = ""
        self.sumTF = 0
        self.termDF = 0


class DocumentIndexData:

    def __init__(self, max_tf, uniqueTermsCount, docLength, city = '',language = ''):
        self.max_tf = max_tf
        self.uniqueTermCount = uniqueTermsCount
        self.docLength = docLength
        self.city = city.upper()
        self.language = language

    def toString(self):
        '''
        max_tf|uniqueTermCount|docLength|city|language
        :return:
        '''
        ans = '|'.join([str(self.max_tf) , str(self.uniqueTermCount), str(self.docLength) ,str(self.city),self.language])
        return ans


class CityIndexData:

    def __init__(self,doc,locations):
        self.dictionary_doc_locations = {}
        self.dictionary_doc_locations[doc] = locations

    def __iadd__(self, other):
        for docID,locations in other.dictionary_doc_locations.items():
            self.dictionary_doc_locations[docID] = locations

        return self

    def addDocumentToCity(self, docID, locations):
        self.dictionary_doc_locations[docID] = locations

    def getDocLocationsAsString(self):
        # ansList = []
        # for doc, locations in sorted(self.dictionary_doc_locations.items()):
        #     ansList.append('|'.join())
        ans = ','.join(['#'.join([doc,locations]) for doc,locations in sorted(self.dictionary_doc_locations.items())])
        return ans

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


