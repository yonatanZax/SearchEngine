import re
import BasicMethods as basic
import Configuration as config
from datetime import datetime

from Indexing.Document import TermData
import nltk


stopWordsList = {}
try:
    path = config.projectMainFolder + 'stop_words.txt'
    with open(path) as f:
        for word in  f.read().splitlines():
            stopWordsList[word] = 'a'
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
    '-' : 'a',
    '_' : 'a',
    '>' : 'a',
    '<' : 'a',
    '`' : 'a',
    '~' : 'a',
    ';' : 'a',
    ':' : 'a'
}


def cleanToken(token):
    # token = token.group()
    size = len(token)
    if size > 0:
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


def parseText(text):
    # TODO - between shit
    splittedText = text.split(' ')
    for textIndex in range(0,len(splittedText)):
        currWord = splittedText[textIndex]
        if len(currWord) == 0:
            continue

        cleanedWord = cleanToken(currWord)
        if cleanedWord is None or stopWordsList.get(cleanedWord.lower()) is not None:
            continue

        if cleanedWord[0].isdigit():
            wordIndex = 1

        else:
            # TODO - stem suppose to be here somewhere
            # TODO - stopwords suppose to be here somewhere
            wordIndex = 1


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



def parseTest(textList):
    termsDic = {}
    size = len(textList)
    i = -1
    while i < size:
        if textList[i][0].isdigit():
            temp, returnedIndex = percentToken(i,textList)
            if temp is not None:
                i = returnedIndex
                termsDic[temp] = 1
                continue
            temp, returnedIndex = monthToken_H1(i,textList)
            if temp is not None:
                i = returnedIndex
                termsDic[temp] = 1
                continue
        else:
            temp, returnedIndex = dateParse_H2_O(i,textList)
            if temp is not None:
                i = returnedIndex
                termsDic[temp] = 1
                continue
        i += 1

    print (termsDic.keys())

text = "one day i was 6% 6.4% and also 8 percent but also 9 percentage 7 May 3 october 31 NOV JUNE 16 May 1992"

startTime = datetime.now()
splittedText = text.split(' ')
finishTime = datetime.now()
timeItTook = finishTime - startTime
print(str(timeItTook.seconds) + " seconds")

startTime = datetime.now()
pattern = re.compile(r'[\S]+')
text = pattern.sub(cleanToken, text)
finishTime = datetime.now()
timeItTook = finishTime - startTime
print(str(timeItTook.seconds) + " seconds")

print (text)
# parseTest(splittedText)


