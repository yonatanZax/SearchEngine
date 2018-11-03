


class MyDictionary:

    def __init__(self):
        self.dictionary_term_dicData = {}

    # assuming termString gets in all CAP or all LOW letters already from parser
    def addTerm(self, termString, docData):
        termDicData = None

        # if the term already in the dictionary the function will change the dictionary key word and return the data
        # if the term doesn't exists in the dictionary it will add it and return null
        termInDictionary = updateTermToDictionaryByTheRules(self.dictionary_term_dicData, termString)
        termDicData = self.dictionary_term_dicData.get(termInDictionary)
        if termDicData is None:
            # add new term
            termDicData = DictionaryData(len(self.dictionary_term_dicData))
            self.dictionary_term_dicData[termInDictionary] = termDicData

        # add the doc to the term posting line
        termDicData.addDocument(docID=docData.docNo, docTF_int=docData.termDoc)




    def getPostingLine(self, term):
        dicData = self.dictionary_term_dicData.get(term)
        if dicData is not None:
            return dicData.postingLine
        return None

# get the format of the term how its saved in the dictionary or none if its not in the dictionary
def getTermDictionaryForm(dictionary, termString):
    if termString.lower() in dictionary:
        return termString.lower()
    if termString.upper() in dictionary:
        return termString.upper()
    return None

# add or do update to the dictionary like it suppose to and will return the it in the way its suppose to be in the dictionary
def updateTermToDictionaryByTheRules(dictionary, termString):
    termInDictionary = dictionary(dictionary=dictionary,termString=termString)
    ans = termInDictionary
    # if the term already in the dictionary
    if termInDictionary is not None:
        dicData = dictionary[termInDictionary]

        # figure out if the term is suppose to be lower or upper

        # if the term is in CAP in dictionary
        if termString.upper() == termInDictionary :

            # but not the term string isn't - change the term in dictionary to small
            if termString[0].islower():
                ans = termString.lower()
                dictionary.pop(termInDictionary)
                dictionary[ans] = dicData


        return ans

    else:
        if termString[0].isupper():
            ans = termString.upper()
        else:
            ans = termString.lower()
        dictionary[ans] = None
        return ans



class DictionaryData:

    def __init__(self, postingLine):
        self.termDF = 0
        self.sumTF = 0
        self.postingLine = postingLine
        self.dictionary_docID_tf = {}

    def addDocument(self, docID, docTF_int):
        self.termDF += 1
        self.sumTF += docTF_int
        self.dictionary_docID_tf[docID] = docTF_int




