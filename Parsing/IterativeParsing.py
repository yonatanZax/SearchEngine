import re
import BasicMethods as basic
from Indexing.Document import TermData

class IterativeTokenizer:

    def __init__(self, config):

        self.config = config

        self.monthDic = {
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

        self.TMBTDic = {
            'thousand': 'K',
            'million': 'M',
            'billion': 'B',
            'trillion': 'T',
        }

        self.cleanerDic = {
            '{': 'a',
            '}': 'a',
            '[': 'a',
            ']': 'a',
            '.': 'a',
            ',': 'a',
            '\"': 'a',
            '\'': 'a',
            '(': 'a',
            ')': 'a',
            '?': 'a',
            '!': 'a',
            '#': 'a',
            '@': 'a',
            '/': 'a',
            '\\': 'a',
            '\t': 'a',
            '\n': 'a',
            ' ': 'a',
            '_': 'a',
            '>': 'a',
            '<': 'a',
            '`': 'a',
            '~': 'a',
            ';': 'a',
            ':': 'a',
            '*': 'a',
            '+': 'a',
            '|': 'a',
            '&': 'a'

        }

        self.betweenPattern = re.compile(r"[Bb]etween " + "[\d,]+" + " and " + "[\d,]+")

        self.cleanPattern = re.compile(r'[\S\n]+')

        self.stopWordsDic = {}
        try:
            path = self.config.stopWordPath
            with open(path) as f:
                for word in f.read().splitlines():
                    self.stopWordsDic[word] = 'a'
                del self.stopWordsDic["may"]
        except IOError:
            print("Can't find path:", path)



    def getTermDicFromText(self, text):
        return self.parseText(text)



    def replaceBetween(self,token):
        splitedToken = token.group().split(' ')
        return splitedToken[0] + '-' + splitedToken[2]

    def cleanWithGroup(self,token):
        token = token.group()
        return self.cleanToken(token)

    def cleanToken(self,token):
        size = len(token)
        if size > 0:
            start = 0
            end = size - 1
            startBool = True
            endBool = True
            while (startBool or endBool) and end >= start:
                if end == start:
                    if self.cleanerDic.get(token[start]) is not None:
                        return None
                    else:
                        return token[start]
                if startBool and self.cleanerDic.get(token[start]) is not None:
                    start += 1
                elif startBool:
                    startBool = False
                if endBool and self.cleanerDic.get(token[end]) is not None:
                    end -= 1
                elif endBool:
                    endBool = False
            if end < start:
                return None

            return token[start:end + 1]

        return None

    def addTermToDic(self,termDictionary, term, index):
        from Indexing.MyDictionary import updateTermToDictionaryByTheRules
        term = term.rstrip(',').rstrip('.')
        if len(term) == 0:
            return
        count = 1
        termFromDic = updateTermToDictionaryByTheRules(termDictionary, term)
        termDataFromDic = termDictionary.get(termFromDic)
        if termDataFromDic is not None:
            termDataFromDic.addPositionToTerm(index)
        else:
            newTerm = TermData(count, index)
            termDictionary[termFromDic] = newTerm

    # function that filters vowels
    def filterAll(self,currWord):
        cleanedWord = self.cleanToken(currWord)
        if cleanedWord is None or self.stopWordsDic.get(cleanedWord.lower()) is not None:
            return False
        return True

    # TODO (DONE) - check where we want to change 'strip()' methods to 'rstrip()' or 'lstrip()'

    def parseText(self,text):
        import Stemmer.Stemmer

        self.betweenPattern.sub(self.replaceBetween, text)
        text = text.replace("\n", '').replace('\t', '').replace('{', '').replace('}', '').replace('[', '').replace(']',
                                                                                                                   '').replace(
            '\"', '').replace('\'', '').replace('(', '').replace(')', '').replace('?', '').replace('!', '').replace('#',
                                                                                                                    '').replace(
            '@', '').replace('/', '').replace('\\', '').replace('_', '').replace('>', '').replace('<', '').replace('`',
                                                                                                                   '').replace(
            '~', '').replace(';', '').replace(':', '').replace('*', '').replace('+', '').replace('|', '').replace('&',
                                                                                                                  '').replace(
            '=', '').replace('--', ' ')
        splittedText = text.split(' ')
        splittedText = list(filter(self.filterAll, splittedText))
        size = len(splittedText)
        textIndex = 0
        termsDic = {}
        docLength = 0
        while textIndex < size:
            cleanedWord = splittedText[textIndex]
            docLength += 1

            if cleanedWord[0].isdigit():
                temp, returnedIndex = self.percentToken(textIndex, splittedText)
                if temp is not None:
                    self.addTermToDic(termsDic, temp, textIndex)
                    textIndex = returnedIndex
                    continue
                temp, returnedIndex = self.monthToken_H1(textIndex, splittedText)
                if temp is not None:
                    self.addTermToDic(termsDic, temp, textIndex)
                    textIndex = returnedIndex

                    continue
                numOfDashes = splittedText[textIndex].count('-')
                if numOfDashes > 0:
                    tokenList, returnedIndex = self.splitDashToken(textIndex, splittedText)
                    for token in tokenList:
                        if len(token) > 0:
                            self.addTermToDic(termsDic, token, textIndex)
                    textIndex = returnedIndex
                    continue
                temp, returnedIndex = self.numTMBT_tokenToTerm(textIndex, splittedText)
                if temp is not None and len(temp) > 0:
                    self.addTermToDic(termsDic, temp, textIndex)
                    textIndex = returnedIndex
                    continue
                self.addTermToDic(termsDic, cleanedWord, textIndex)


            else:

                # TODO (DONE) - stem suppose to be here somewhere, make sure the toStem gets all the way down to here
                if len(cleanedWord) < 2:
                    docLength -= 1
                    textIndex += 1
                    continue

                if cleanedWord[0] == '-' and not cleanedWord[1].isdigit():
                    cleanedWord = cleanedWord[1:]

                if cleanedWord[0] == '$':
                    temp, returnedIndex = self.startWithDollar(textIndex, splittedText)
                    if temp is not None:
                        self.addTermToDic(termsDic, temp, textIndex)
                        textIndex = returnedIndex
                        continue
                numOfDashes = cleanedWord.count('-')
                if cleanedWord.count('-') > 0:
                    if numOfDashes == 1 and cleanedWord[0] == '-':
                        if len(cleanedWord) > 1 and cleanedWord[1].isdigit:
                            self.addTermToDic(termsDic, cleanedWord, textIndex)
                        else:
                            cleanedToken = self.cleanToken(cleanedWord[1:len(cleanedWord)])
                            if cleanedToken is not None:
                                self.addTermToDic(termsDic, cleanedToken, textIndex)
                        textIndex += 1
                        continue
                    else:
                        tokenList, returnedIndex = self.splitDashToken(textIndex, splittedText)
                        for token in tokenList:
                            if len(token) > 0:
                                # TODO (DONE) - check if the term is number
                                self.addTermToDic(termsDic, token, textIndex)
                        textIndex = returnedIndex
                        continue
                temp, returnedIndex = self.dateParse_H2_O(textIndex, splittedText)
                if temp is not None:
                    self.addTermToDic(termsDic, temp, textIndex)
                    textIndex = returnedIndex

                    continue
                if cleanedWord.lower() not in ['may']:
                    if self.config.toStem:
                        afterStem = Stemmer.Stemmer.stemTerm(cleanedWord)
                        cleanedWord = afterStem
                    if len(cleanedWord) > 0:
                        self.addTermToDic(termsDic, cleanedWord, textIndex)
                    else:
                        docLength -= 1
                else:
                    docLength -= 1

            textIndex += 1

        return termsDic, docLength

    def percentToken(self,index, textList):
        currWord = textList[index]
        if currWord[len(currWord) - 1] is '%':
            index += 1
            return currWord, index
        elif index + 1 < len(textList) and textList[index + 1].lower() in ["percent", "percentage"]:
            term = textList[index] + "%"
            index += 2
            return term, index
        return None, index

    def monthToken_H1(self, index, textList):
        currWord = textList[index]
        if basic.isInt(currWord):
            if index + 1 < len(textList) and self.monthDic.get(textList[index + 1].lower()) is not None:
                if len(currWord) < 2:
                    currWord = "0" + currWord
                returnValue = self.monthDic.get(textList[index + 1].lower()) + "-" + currWord
                index += 2
                return returnValue, index
        return None, index

    def dateParse_H2_O(self,index, textList):
        currWord = textList[index]
        if self.monthDic.get(currWord.lower()) is not None:
            monthNumber = self.monthDic.get(currWord.lower())
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

    def splitDashToken(self,index, textList):
        tokenList = []
        token = textList[index]
        tokenList = token.split('-')
        ansList = []
        for term in tokenList:
            cleanedTerm = self.cleanToken(term)
            if cleanedTerm is not None and len(term) > 1:
                ansList.append(term)
        ansList.append(textList[index])
        return ansList, index + 1

    # TODO - add 2 rules

    def startWithDollar(self,curIndex, listOfTokens):
        import Parsing.ConvertMethods  as convert
        token = listOfTokens[curIndex]
        term = token[1]
        if not term.isdigit():
            return token, curIndex + 1
        p = 2
        hasDot = False

        while p < len(token):
            # token = 1,550.23 -> 1550.23
            if token[p] == '.':
                if hasDot:
                    return token, curIndex + 1
                else:
                    hasDot = True
                    term += token[p]
                    p += 1
                    continue

            elif token[p].isdigit():
                term += token[p]
            elif token[p] == ',':
                p += 1
                continue
            elif token[p].lower() in ['m', 'k', 'b', 't']:
                if not basic.isfloat(term):
                    return token, curIndex + 1
                term = str(float(term) * convert.convertTMBT_toNum('', token[p].lower()))
            else:
                return token, curIndex + 1

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
                        # TODO (DONE) - convert term
                        term = convert.convertNumToKMBformat(term)
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

    def numTMBT_tokenToTerm(self,curIndex, listOfTokens):
        import Parsing.ConvertMethods  as convert
        token = listOfTokens[curIndex]
        term = token[0]
        p = 1
        hasDot = False

        while p < len(token):
            # token = 1,550.23 -> 1550.23
            if token[p] == '.':
                if hasDot:
                    return token, curIndex + 1
                else:
                    hasDot = True
                    term += token[p]
                    p += 1
                    continue

            elif token[p].isdigit():
                term += token[p]
            elif token[p] == ',':
                p += 1
                continue
            elif token[p].lower() in ['m', 'k', 'b', 't']:
                if not basic.isfloat(term):
                    return token, curIndex + 1
                term = str(float(term) * convert.convertTMBT_toNum('', token[p].lower()))
            else:
                return token, curIndex + 1

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
                        return None, curIndex - 1
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
                    return term, curIndex - 1

                elif checkForUSDOLLARS in ['Dollars', 'dollars']:
                    term = convert.convertNumToMoneyFormat(term)
                    return term + ' Dollars', curIndex + 1
                return term, curIndex

        checkTMBT = listOfTokens[curIndex]
        if checkTMBT in ['Thousand', 'thousand', 'Million', 'million', 'Billion', 'billion', 'Trillion', 'trillion']:
            if basic.isfloat(term):
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
                    return term, curIndex
            else:
                return term, curIndex

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

#     TODO - encapsulate all the functions



