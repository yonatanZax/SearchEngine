import re
import BasicMethods as basic
import Configuration as config
from datetime import datetime

from Indexing.Document import TermData
import nltk


stopWordsDic = {}
try:
    path = config.projectMainFolder + 'stop_words.txt'
    with open(path) as f:
        for word in  f.read().splitlines():
            stopWordsDic[word] = 'a'
        del stopWordsDic["may"]
except IOError:
    print("Can't find path:",path)



monthDic = {
        'jan': '01',
        'january': '01',
        'feb': '02',
        'february': '02',
        'mar': '03',
        'march': '03',
        'apr': '04',
        'april': '04',
        'may': '05',
        'jun': '06',
        'june': '06',
        'jul': '07',
        'july': '07',
        'aug': '08',
        'august': '08',
        'sep': '09',
        'september': '09',
        'oct': '10',
        'october': '10',
        'nov': '11',
        'november': '11',
        'dec': '12',
        'december': '12'
    }

TMBTDic = {
        'thousand': 'K',
        'million': 'M',
        'billion': 'B',
        'trillion': 'T',
    }

cleanerDic = {
    '{' : 'a',
    '}' : 'a',
    '[' : 'a',
    ']' : 'a',
    '.' : 'a',
    ',' : 'a',
    '\"' : 'a',
    '\'' : 'a',
    '(' :'a',
    ')' : 'a',
    '?' : 'a',
    '!' : 'a',
    '#' : 'a',
    '@' : 'a',
    '/' : 'a',
    '\\' : 'a',
    '\t' : 'a',
    '\n' : 'a',
    ' ' : 'a',
    '_' : 'a',
    '>' : 'a',
    '<' : 'a',
    '`' : 'a',
    '~' : 'a',
    ';' : 'a',
    ':' : 'a',
    '*' : 'a',
    '+': 'a',

}

betweenPattern = re.compile(r"[Bb]etween " + "[\d,]+" + " and " + "[\d,]+")

cleanPattern = re.compile(r'[\S\n]+')

def replaceBetween(token):
    splitedToken = token.group().split(' ')
    return splitedToken[0] + '-' + splitedToken[2]


def cleanWithGroup(token):
    token = token.group()
    return cleanToken(token)




def cleanToken(token):
    size = len(token)
    if size > 0:



        if stopWordsDic.get(token.lower()) is not None:
            return None

        start = 0
        end = size - 1
        startBool = True
        endBool = True
        while (startBool or endBool) and end >= start:
            if end == start:
                if cleanerDic.get(token[start]) is not None:
                    return None
                else:
                    return token[start]
            if startBool and cleanerDic.get(token[start]) is not None:
                start += 1
            elif startBool:
                startBool = False
            if endBool and cleanerDic.get(token[end]) is not None:
                end -= 1
            elif endBool:
                endBool = False
        if end < start:
            return None

        return token[start:end + 1]

    return None


def addTermToDic(termDictionary, term):
    from Indexing.MyDictionary import updateTermToDictionaryByTheRules
    count = 1
    termFromDic = updateTermToDictionaryByTheRules(termDictionary, term)
    termDataFromDic = termDictionary.get(termFromDic)
    if termDataFromDic is not None:
        count = termDataFromDic.termFrequency + 1
        termDataFromDic.termFrequency = count
    else:
        newTerm = TermData(count, 0)
        termDictionary[termFromDic] = newTerm

def parseText(text, toStem=False):
    import Stemmer.Stemmer

    betweenPattern.sub(replaceBetween,text)
    newText = cleanPattern.sub(cleanWithGroup, text)
    splittedText = nltk.regexp_tokenize(newText, r'\S+')
    # splittedText = text.split(' ')
    size = len(splittedText)
    textIndex = 0
    termsDic = {}
    docLength = 0
    while textIndex < size:
        currWord = splittedText[textIndex]
        if len(currWord) == 0:
            textIndex += 1
            continue
        # cleanedWord = currWord
        cleanedWord = cleanToken(currWord)
        if cleanedWord is None or stopWordsDic.get(cleanedWord.lower()) is not None:
            textIndex += 1
            continue

        docLength += 1

        if cleanedWord[0].isdigit():
            temp, returnedIndex = percentToken(textIndex, splittedText)
            if temp is not None:
                textIndex = returnedIndex
                addTermToDic(termsDic, temp)
                continue
            temp, returnedIndex = monthToken_H1(textIndex, splittedText)
            if temp is not None:
                textIndex = returnedIndex
                addTermToDic(termsDic, temp)
                continue
            numOfDashes = splittedText[textIndex].count('-')
            if numOfDashes > 1:
                tokenList, returnedIndex = splitDashToken(textIndex, splittedText)
                for token in tokenList:
                    if len(token) > 0:
                        addTermToDic(termsDic, token)
                textIndex = returnedIndex
                continue
            temp, returnedIndex = numTMBT_tokenToTerm(textIndex, splittedText)
            if temp is not None and len(temp) > 0:
                textIndex = returnedIndex
                addTermToDic(termsDic, temp)
                continue
            addTermToDic(termsDic, cleanedWord)


        else:

            # TODO - stem suppose to be here somewhere
            # TODO - stopwords suppose to be here somewhere
            if currWord[0] == '$':
                if len(currWord) == 1:
                    docLength -= 1
                    textIndex += 1
                    continue
                temp, returnedIndex = startWithDollar(textIndex, splittedText)
                if temp is not None:
                    textIndex = returnedIndex
                    addTermToDic(termsDic, temp)
                    continue
            numOfDashes = currWord.count('-')
            if currWord.count('-') > 0:
                if numOfDashes == 1 and currWord[0] == '-':
                    if len(splittedText[textIndex]) > 1 and splittedText[textIndex][1].isdigit:
                        addTermToDic(termsDic, cleanedWord)
                    else:
                        cleanedToken = cleanToken(splittedText[textIndex][1:len(splittedText[textIndex])])
                        if cleanedToken is not None:
                            addTermToDic(termsDic, cleanedToken)
                    textIndex += 1
                    continue
                else:
                    tokenList, returnedIndex = splitDashToken(textIndex, splittedText)
                    for token in tokenList:
                        if len(token) > 0:
                            addTermToDic(termsDic, token)
                    textIndex = returnedIndex
                    continue
            temp, returnedIndex = dateParse_H2_O(textIndex,splittedText)
            if temp is not None:
                textIndex = returnedIndex
                addTermToDic(termsDic, temp)
                continue
            if cleanedWord.lower() not in ['may']:
                if toStem:
                    cleanedWord = Stemmer.Stemmer.stemTerm(cleanedWord)
                addTermToDic(termsDic, cleanedWord)
            else:
                docLength -= 1

        textIndex += 1

    return termsDic, docLength
    # print (termsDic.keys())



def percentToken(index, textList):
    currWord = textList[index]
    if currWord[len(currWord) - 1] is '%':
        index += 1
        return currWord ,index
    elif index + 1 < len(textList) and textList[index + 1].lower() in ["percent", "percentage"]:
        term = textList[index] + "%"
        index += 2
        return term, index
    return None , index


def monthToken_H1(index, textList):
    currWord = textList[index]
    if basic.isInt(currWord):
        if index + 1 < len(textList) and monthDic.get(textList[index + 1].lower()) is not None:
            if len(currWord) < 2:
                currWord = "0" + currWord
            returnValue = monthDic.get(textList[index + 1].lower()) + "-" + currWord
            index += 2
            return returnValue, index
    return None, index

def dateParse_H2_O(index, textList):
    currWord = textList[index]
    if monthDic.get(currWord.lower()) is not None:
        monthNumber = monthDic.get(currWord.lower())
        if index + 1 < len(textList) and basic.isInt(textList[index + 1]):
            numberString = textList[index + 1]
            if len(numberString) == 4:
                returnValue = numberString + "-" + monthNumber
            else:
                if len(numberString) < 2:
                    numberString = "0" + numberString
                returnValue = monthNumber + "-" + numberString
            index += 2
            return returnValue, index

    return None, index

def splitDashToken(index, textList):
    tokenList = []
    tokenList = textList[index].split("-")
    # for term in tokenList:
    #     # cleanedTerm = cleanToken(term)
    #     if cleanedTerm is None:
    #         tokenList.remove(term)
    tokenList.append(textList[index])
    return tokenList, index + 1



def startWithDollar(curIndex,listOfTokens):
    import Parsing.ConvertMethods  as convert
    token = listOfTokens[curIndex]
    term = token[1]
    p = 2

    while p < len(token):
        # token = 1,550.23 -> 1550.23
        if token[p].isdigit() or token[p] == '.':
            term += token[p]
        elif token[p] == ',':
            p += 1
            continue
        elif token[p].lower() in ['m', 'k', 'b', 't']:
            term = str(float(term) * convert.convertTMBT_toNum('', token[p].lower()))
        else:
            return None, curIndex

        p = p + 1

    # locking for 1/2
    curIndex += 1
    numWithSlash = listOfTokens[curIndex]
    p = 0
    if numWithSlash[p].isdigit():
        numWithSlashToAdd = numWithSlash[p]
        p += 1
        hasSlash = False
        while p < len(numWithSlash):

            if numWithSlash[p].isdigit():
                numWithSlashToAdd += numWithSlash[p]
                p += 1
            elif numWithSlash[p] == '/':
                if not hasSlash:
                    hasSlash = True
                    numWithSlashToAdd += numWithSlash[p]
                    p += 1
                else:
                    # if nextToken has more than 1 slash , meaning is not a fraction
                    # TODO - convert term
                    return term, curIndex
            else:
                break

            p = p + 1

        if hasSlash:
            term = term + ' ' + numWithSlash
            return term + ' Dollars', curIndex + 1

    checkTMBT = listOfTokens[curIndex]
    if checkTMBT in ['Thousand', 'thousand', 'Million', 'million', 'Billion', 'billion', 'Trillion', 'trillion']:
        term = str(float(term) * convert.convertTMBT_toNum(tmbtString=checkTMBT.lower()))
        term = convert.convertNumToMoneyFormat(term)
        return term + ' Dollars', curIndex + 1

    term = convert.convertNumToMoneyFormat(term)
    return term + ' Dollars', curIndex


def numTMBT_tokenToTerm(curIndex,listOfTokens):
    import Parsing.ConvertMethods  as convert
    token = listOfTokens[curIndex]
    term = token[0]
    p = 1

    while p < len(token):
        # token = 1,550.23 -> 1550.23
        if token[p].isdigit() or token[p] == '.':
            term += token[p]
        elif token[p] == ',':
            p += 1
            continue
        elif token[p].lower() in ['m','k','b','t']:
            term = str(float(term)*convert.convertTMBT_toNum('',token[p].lower()))
        else:
            return None,curIndex

        p = p + 1

    # locking for 1/2
    curIndex += 1
    numWithSlash = listOfTokens[curIndex]
    p = 0
    if numWithSlash[p].isdigit():
        numWithSlashToAdd = numWithSlash[p]
        p += 1
        hasSlash = False
        while p < len(numWithSlash):

            if numWithSlash[p].isdigit():
                numWithSlashToAdd += numWithSlash[p]
                p += 1
            elif numWithSlash[p] == '/':
                if not hasSlash:
                    hasSlash = True
                    numWithSlashToAdd += numWithSlash[p]
                    p+=1
                else:
                    # if nextToken has more than 1 slash , meaning is not a fraction
                    return None,curIndex-1
            else:
                break

            p = p + 1

        if hasSlash:
            term = term + ' ' + numWithSlash
            curIndex += 1
            checkForUSDOLLARS = listOfTokens[curIndex]
            if checkForUSDOLLARS == 'U.S':
                curIndex += 1
                checkForUSDOLLARS = listOfTokens[curIndex]
                if checkForUSDOLLARS in ['Dollars', 'dollars']:
                    term = convert.convertNumToMoneyFormat(term)
                    return term + ' Dollars', curIndex + 1
                return term, curIndex -1

            elif checkForUSDOLLARS in ['Dollars', 'dollars']:
                term = convert.convertNumToMoneyFormat(term)
                return term + ' Dollars', curIndex + 1
            return term, curIndex



    checkTMBT = listOfTokens[curIndex]
    if checkTMBT in ['Thousand', 'thousand','Million','million','Billion','billion','Trillion','trillion']:
        term = str(float(term) * convert.convertTMBT_toNum(tmbtString=checkTMBT.lower()))
        curIndex += 1
        checkForUSDOLLARS = listOfTokens[curIndex]
        if checkForUSDOLLARS == 'U.S':
            curIndex += 1
            checkForUSDOLLARS = listOfTokens[curIndex]
            if checkForUSDOLLARS in ['Dollars', 'dollars']:
                term = convert.convertNumToMoneyFormat(term)
                return term + ' Dollars', curIndex + 1
            return term, curIndex - 1

        elif checkForUSDOLLARS in ['Dollars', 'dollars']:
            term = convert.convertNumToMoneyFormat(term)
            return term + ' Dollars', curIndex + 1
        else:
            term = convert.convertNumToKMBformat(term)
            return term , curIndex



    checkForUSDOLLARS = listOfTokens[curIndex]
    if checkForUSDOLLARS == 'U.S':
        curIndex += 1
        checkForUSDOLLARS = listOfTokens[curIndex]
        if checkForUSDOLLARS in ['Dollars', 'dollars']:
            term = convert.convertNumToMoneyFormat(term)
            return term + ' Dollars', curIndex + 1
        return term, curIndex - 1

    elif checkForUSDOLLARS in ['Dollars', 'dollars']:
        term = convert.convertNumToMoneyFormat(term)
        return term + ' Dollars', curIndex + 1


    term = convert.convertNumToKMBformat(term)
    return term, curIndex





# text = "one day i was 6% 6.4% and also 8 percent but also 9 percentage 7 May 3 october 31 NOV JUNE 16 May 1992 "
# cleanText = '20b , 15k , 22 3/4 , 10,123 , 123 Thousand , 1010.56 , 10,123,000,000 , 55 Billion , 7 Trillion ,' \
# #             ' 1.7320 Dollars , 1,732 , 22 Dollars , 1,000,000 Dollars , 100 billion U.S. Dollars ,' \
# #             ' 320 million U.S. Dollars , 1 trillion U.S. Dollars '
# #
# dollarText = '$22 3/4 , $50 Thousand , $450,000 , $450,000,000 , $100 million , $100 billion'
# text += cleanText + dollarText
#
# parseText(text)


