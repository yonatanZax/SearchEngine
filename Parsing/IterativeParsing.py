import re
import BasicMethods as basic
from Indexing.Document import TermData
from Indexing.MyDictionary import updateTermToDictionaryByTheRules
import Stemmer.Stemmer


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

        self.stopWordsDic = {}

        self.dictionary_term_stemmedTerm = {}
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
        term = term.rstrip(',').rstrip('.').rstrip('-')
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


    def parseText(self,text):

        self.betweenPattern.sub(self.replaceBetween, text)

        text = text.replace("<P>", '').replace("</P>", '').replace("\n", ' ').replace('\t', ' ').replace('{', '').replace('}', '').replace('[', '').replace(']',
                                                                                                                   '').replace(
            '\"', '').replace('\'', '').replace('(', '').replace(')', '').replace('?', '').replace('!', '').replace('#',
                                                                                                                    '').replace(
            '@', '').replace('/', '').replace('\\', '').replace('_', '').replace('>', '').replace('<', '').replace('`',
                                                                                                                   '').replace(
            '~', '').replace(';', '').replace(':', '').replace('*', '').replace('+', '').replace('|', '').replace('&',
                                                                                                                  '').replace(
            '=', '')
        text = re.sub(r'[-]+','-',text)
        text = re.sub(r'[.]+', '.', text)
        text = re.sub(r'[,]+', ',', text)
        splittedText = text.split(' ')
        return self.parseFromList(splittedText, 0)

    def parseFromList(self, splittedText, offset = 0):

        splittedText = list(filter(self.filterAll, splittedText))

        docLength = 0
        size = len(splittedText)
        termsDic = {}
        textIndex = 0
        while textIndex < size:
            cleanedWord = splittedText[textIndex]
            docLength += 1
            if len(cleanedWord) == 0:
                docLength -= 1
                textIndex += 1
                continue
            if cleanedWord[0] == '.':
                cleanedWord = '0' + cleanedWord

            if cleanedWord[0].isdigit():
                temp, returnedIndex = self.percentToken(textIndex, splittedText)
                if temp is not None:
                    self.addTermToDic(termsDic, temp, textIndex + offset)
                    textIndex = returnedIndex
                    continue
                temp, returnedIndex = self.monthToken_H1(textIndex, splittedText)
                if temp is not None:
                    self.addTermToDic(termsDic, temp, textIndex + offset)
                    textIndex = returnedIndex

                    continue
                numOfDashes = splittedText[textIndex].count('-')
                if numOfDashes > 0:
                    tokenDic, LengthReturned = self.splitTokenBySeparator(textIndex, splittedText,'-')
                    i = 0
                    for token, termData in tokenDic.items():
                        if len(token) > 0 and self.stopWordsDic.get(token.lower()) is None:
                            self.addTermToDic(termsDic, token, textIndex + i)
                    textIndex += 1
                    docLength += LengthReturned
                    continue


                termList, returnedIndex = self.numTMBT_tokenToTerm(textIndex, splittedText)
                if termList is None:
                    textIndex = returnedIndex
                    continue

                for i in range(0,len(termList)):
                    self.addTermToDic(termsDic, termList[i], textIndex + i)

                textIndex = returnedIndex
                continue



            else:

                if len(cleanedWord) < 2:
                    docLength -= 1
                    textIndex += 1
                    continue

                if cleanedWord[0] == '-' and not cleanedWord[1].isdigit():
                    cleanedWord = cleanedWord[1:]

                numOfDashes = cleanedWord.count('-')
                if cleanedWord.count('-') > 0:
                    if numOfDashes == 1 and cleanedWord[0] == '-':
                        if len(cleanedWord) > 1 and cleanedWord[1].isdigit:
                            self.addTermToDic(termsDic, cleanedWord, textIndex + offset)
                        else:
                            cleanedToken = self.cleanToken(cleanedWord[1:len(cleanedWord)])
                            if cleanedToken is not None:
                                self.addTermToDic(termsDic, cleanedToken, textIndex + offset)
                        textIndex += 1
                        continue
                    else:
                        tokenDic, LengthReturned = self.splitTokenBySeparator(textIndex, splittedText,'-')
                        i = 0
                        for token,termData in tokenDic.items():
                            if len(token) > 0 and self.stopWordsDic.get(token.lower()) is None:
                                self.addTermToDic(termsDic, token, textIndex + i)
                        textIndex += 1
                        docLength += LengthReturned
                        continue

                if cleanedWord[0] == '$':
                    termList, returnedIndex = self.startWithDollar(textIndex, splittedText)
                    if termList is None:
                        textIndex = returnedIndex
                        continue

                    for i in range(0, len(termList)):
                        self.addTermToDic(termsDic, termList[i], textIndex + i)

                    textIndex = returnedIndex
                    continue

                temp, returnedIndex = self.dateParse_H2_O(textIndex, splittedText)
                if temp is not None:
                    self.addTermToDic(termsDic, temp, textIndex + offset)
                    textIndex = returnedIndex

                    continue


                if len(cleanedWord) > 0:
                    splitByComma = cleanedWord.strip(',').split(',')
                    if len(splitByComma) > 1:
                        tokenDic, LengthReturned = self.parseFromList(splitByComma, textIndex)
                        i = 0
                        for token, termData in tokenDic.items():
                            if len(token) > 0 and self.stopWordsDic.get(token.lower()) is None:
                                self.addTermToDic(termsDic, token, textIndex + i)
                        textIndex += 1
                        docLength += LengthReturned
                        continue
                        # termList = []
                        # for w in splitByComma:
                        #     terms , index = self.parseText(w)
                        #     termList = termList + list(terms)
                        # for term in termList:
                        #     self.addTermToDic(termsDic, term, textIndex + offset)
                    elif cleanedWord.count('.') > 0:
                        splitByDot = cleanedWord.strip('.').split('.')
                        tokenDic, LengthReturned = self.parseFromList(splitByDot, textIndex)
                        i = 0
                        for token, termData in tokenDic.items():
                            if len(token) > 0 and self.stopWordsDic.get(token.lower()) is None:
                                self.addTermToDic(termsDic, token, textIndex + i)
                        textIndex += 1
                        docLength += LengthReturned
                        continue
                        # if len(splitByDot) > 1:
                        #     termList = []
                        #     for w in splitByDot:
                        #         terms, index = self.parseText(w)
                        #         termList = termList + list(terms)
                        #
                        #     for term in termList:
                        #         self.addTermToDic(termsDic, term, textIndex + offset)
                    else:
                        if cleanedWord[0].isupper():
                            termList , returnedIndex = self.ruleNBA(textIndex, splittedText)
                            if len(termList) > 1:
                                tempOffSet = 0
                                for term in termList:
                                    self.addTermToDic(termsDic, term, textIndex + tempOffSet + offset)
                                    tempOffSet += 1
                                    docLength += 1
                                docLength -= 1
                                textIndex = returnedIndex
                                continue

                    # else:
                    #     docLength -= 1

                if cleanedWord.lower() not in ['may']:
                    if len(cleanedWord) >= 15 and cleanedWord.lower().find('table') != -1 :
                        docLength -= 1
                        textIndex += 1
                        continue
                    if self.config.toStem:
                        isAllLower = cleanedWord.islower()
                        lowerCaseCleanedWord = cleanedWord.lower()
                        if self.dictionary_term_stemmedTerm.get(lowerCaseCleanedWord) is None:
                            afterStem = Stemmer.Stemmer.stemTerm(lowerCaseCleanedWord)
                            self.dictionary_term_stemmedTerm[lowerCaseCleanedWord] = afterStem
                            cleanedWord = afterStem
                        else:
                            if isAllLower:
                                self.dictionary_term_stemmedTerm[lowerCaseCleanedWord] = \
                                self.dictionary_term_stemmedTerm[lowerCaseCleanedWord].lower()
                            cleanedWord = self.dictionary_term_stemmedTerm[lowerCaseCleanedWord]

                    if self.stopWordsDic.get(cleanedWord.lower()) is None:
                        self.addTermToDic(termsDic, cleanedWord, textIndex + offset)
                else:
                    docLength -= 1

            textIndex += 1

        return termsDic, docLength



    def ruleNBA(self,index,textList):
        listOfTerms = [textList[index]]
        bigLetters = textList[index][0]
        tempIndex = index + 1
        while tempIndex < len(textList):

            currWord = textList[tempIndex]
            currWord = self.cleanToken(currWord)
            if currWord is None:
                tempIndex += 1
                continue
            if currWord == bigLetters:
                listOfTerms = [' '.join(textList[index:tempIndex])] + textList[index:tempIndex]
                listOfTerms.append(currWord)
                return listOfTerms, tempIndex

            if currWord[0].isupper():
                bigLetters += currWord[0]
                if len(bigLetters) > 6:

                    break
            else:
                break

            tempIndex += 1


        return listOfTerms , index + 1



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

    def splitTokenBySeparator(self, index, textList,sep):
        splittedText = textList[index].split(sep)
        # splittedText = list(filter(self.filterAll, splittedText))

        termsDic, docLength = self.parseFromList(splittedText,index)
        if '$' in textList[index] or 'illion' in textList[index]:
            return termsDic, docLength
        self.addTermToDic(termsDic, textList[index], index)

        return termsDic, docLength



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
            if token[p] == 'O':
                token = token[:p] + '0' + token[p+1:]
            if token[p] == '.':
                if hasDot:
                    return [token], curIndex + 1
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
                    return [term], curIndex + 1
                elif p + 1 < len(token):
                    if token[p].lower() == 'b' and token[p+1].lower() == 'n':
                        term = str(float(term) * convert.convertTMBT_toNum('', 'bn'))
                        p += 2
                else:
                    term = str(float(term) * convert.convertTMBT_toNum('', token[p].lower()))

                # term = convert.convertNumToKMBformat(term)

                if p < len(token):
                    if token[p] == '.':
                        hasDot = True
                    p += 1
                    continue

            else:
                term = convert.convertNumToMoneyFormat(term)
                return [term + ' Dollars', token[p:]], curIndex + 1

            p += 1

        # locking for 1/2
        curIndex += 1
        if curIndex < len(listOfTokens):
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
                            if token[p] == '.':
                                p += 1
                            # if nextToken has more than 1 slash , meaning is not a fraction
                            # term = convert.convertNumToKMBformat(term)
                            return [term, token[p + 1:]], curIndex - 1
                    else:
                        break

                    p = p + 1

                if hasSlash:
                    term = term + ' ' + numWithSlash
                    return [term + ' Dollars'], curIndex + 1

            checkTMBT = listOfTokens[curIndex]
            if checkTMBT in ['Thousand', 'thousand', 'Million', 'million', 'Billion', 'billion', 'Trillion',
                             'trillion']:
                term = str(float(term) * convert.convertTMBT_toNum(tmbtString=checkTMBT.lower()))
                term = convert.convertNumToMoneyFormat(term)
                return [term + ' Dollars'], curIndex + 1

            term = convert.convertNumToMoneyFormat(term)
            return [term + ' Dollars'], curIndex

        else:
            term = convert.convertNumToMoneyFormat(term)
            return [term + ' Dollars'], curIndex




    def numTMBT_tokenToTerm(self,curIndex, listOfTokens):
        import Parsing.ConvertMethods  as convert
        token = listOfTokens[curIndex]
        if token[0] == '.':
            token = '0' + token
        term = token[0]
        p = 1
        hasDot = False

        while p < len(token):

            # token = 1,550.23 -> 1550.23

            if token[p] == 'O':
                token = token[:p] + '0' + token[p+1:]
            if token[p] == '.':
                if hasDot:
                    term = convert.convertNumToKMBformat(term)
                    return [term,token[p+1:]], curIndex + 1
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
                    term = convert.convertNumToKMBformat(term)
                    return [term, token[p:]], curIndex + 1
                elif p + 1 < len(token):
                    if token[p].lower() == 'b' and token[p + 1].lower() == 'n':
                        term = str(float(term) * convert.convertTMBT_toNum('', 'bn'))
                        p += 2
                else:
                    term = str(float(term) * convert.convertTMBT_toNum('', token[p].lower()))
                # term = convert.convertNumToKMBformat(term)

                if p < len(token):
                    if token[p] == '.':
                        hasDot = True
                    p += 1
                    continue

            else:

                term = convert.convertNumToKMBformat(term)
                return [term, token[p:]], curIndex + 1

            p += 1

        # locking for 1/2
        curIndex += 1
        if curIndex < len(listOfTokens):
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
                            if token[p] == '.':
                                p += 1
                            # if nextToken has more than 1 slash , meaning is not a fraction
                            term = convert.convertNumToKMBformat(term)
                            return [term, token[p+1:]], curIndex - 1
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
                            return [term + ' Dollars'], curIndex + 1
                        term = convert.convertNumToKMBformat(term)
                        return [term], curIndex - 1

                    elif checkForUSDOLLARS in ['Dollars', 'dollars']:
                        term = convert.convertNumToMoneyFormat(term)
                        return [term + ' Dollars'], curIndex + 1
                    term = convert.convertNumToKMBformat(term)
                    return [term], curIndex

            checkTMBT = listOfTokens[curIndex]
            if checkTMBT in ['Thousand', 'thousand', 'Million', 'million', 'Billion', 'billion', 'Trillion',
                             'trillion']:
                if basic.isfloat(term):
                    term = str(float(term) * convert.convertTMBT_toNum(tmbtString=checkTMBT.lower()))
                    curIndex += 1
                    if curIndex < len(listOfTokens):
                        checkForUSDOLLARS = listOfTokens[curIndex]
                        if checkForUSDOLLARS == 'U.S':
                            curIndex += 1
                            checkForUSDOLLARS = listOfTokens[curIndex]
                            if checkForUSDOLLARS in ['Dollars', 'dollars']:
                                term = convert.convertNumToMoneyFormat(term)
                                return [term + ' Dollars'], curIndex + 1
                            term = convert.convertNumToKMBformat(term)
                            return [term, curIndex - 1]

                        elif checkForUSDOLLARS in ['Dollars', 'dollars']:
                            term = convert.convertNumToMoneyFormat(term)
                            return [term + ' Dollars'], curIndex + 1
                        else:
                            term = convert.convertNumToKMBformat(term)
                            return [term], curIndex
                    else:
                        term = convert.convertNumToKMBformat(term)
                        return [term], curIndex

                else:
                    term = convert.convertNumToKMBformat(term)
                    return [term], curIndex

            checkForUSDOLLARS = listOfTokens[curIndex]
            if checkForUSDOLLARS == 'U.S':
                curIndex += 1
                checkForUSDOLLARS = listOfTokens[curIndex]
                if checkForUSDOLLARS in ['Dollars', 'dollars']:
                    term = convert.convertNumToMoneyFormat(term)
                    return [term + ' Dollars'], curIndex + 1
                return [term], curIndex - 1

            elif checkForUSDOLLARS in ['Dollars', 'dollars']:
                term = convert.convertNumToMoneyFormat(term)
                return [term + ' Dollars'], curIndex + 1

            term = convert.convertNumToKMBformat(term)
            return [term], curIndex

        else:
            term = convert.convertNumToKMBformat(term)
            return [term], curIndex


