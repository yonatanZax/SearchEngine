
import re
import BasicMethods as basic
import Configuration as config
from Indexing.Document import TermData





# *** Tokenize rules ***

# numberWithCommasRule
nwcr = "[\d,]+"
betweenRule = "[Bb]etween " + nwcr + " and " + nwcr
# January | February | March | April | May | June | July | August | September | October | November | December
monthList = ["[Jj]anuary", "[Ff]ebruary", "[Mm]arch", "[Aa]pril"]
hasMonthRule = '|'.join(monthList)


# '[jJ]anuary \\d{2}|[Ff]ebruary \\d{2}|[Mm]arch \\d{2}|[Aa]pril \\d{2}'
monthBeforeRule = " \d{2,4}|".join(monthList) + " \d{2,4}"
twoFourDigitNum = "\d{2,4} "
tempMonthList = []
for month in monthList:
    tempMonthList.append(month + '|')
monthAfterRule = '{1}{0}'.format(twoFourDigitNum.join(tempMonthList), twoFourDigitNum)

# '\\d{2} [jJ]anuary|\\d{2} [Ff]ebruary|\\d{2} [Mm]arch|\\d{2} [Aa]pril'
monthAfterRule = monthAfterRule[:-1]

combainedRule = "\w+-\w+"
percentRule = "\d+[\s/-/]percentage|\d+[\s/-/]percent"

listTMBT = [" [Tt]housand", " [Mm]illion", " [Bb]illion", " [Tt]rillion"]
listNumWithTMBT = []
for t in listTMBT:
    listNumWithTMBT.append(nwcr + t)

numWithTMBTRule = '|'.join(listNumWithTMBT)

# '\\$[\\d,]+ Thousand|\\$[\\d,]+ Million|\\$[\\d,]+ Billion|\\$[\\d,]+ Trillion'
dSignWithTMBT = '{1}{0}'.format("|\$".join(listNumWithTMBT), "\$")

# '[\\d,]+ Thousand Dollars|[\\d,]+ Million Dollars|[\\d,]+ Billion Dollars|[\\d,]+ Trillion [Dd]ollars|'
dollarsWithTMBT = " [Dd]ollars|".join(listNumWithTMBT) + " [Dd]ollars"

# '[\\d,]+ Thousand U.S. Dollars|[\\d,]+ Million U.S. Dollars|[\\d,]+ Billion U.S. Dollars|[\\d,]+ Trillion [Dd]ollars|'
usDollarsWithTMBT = " U.S. [Dd]ollars|".join(listNumWithTMBT) + " U.S. [Dd]ollars"

# \$[\d,]+ Thousand|\$[\d,]+ Million|\$[\d,]+ Billion|\$[\d,]+ Trillion|
# [\d,]+ Thousand Dollars|[\d,]+ Million Dollars|[\d,]+ Billion Dollars|[\d,]+ Trillion|
# [\d,]+ Thousand U.S. Dollars|[\d,]+ Million U.S. Dollars|[\d,]+ Billion U.S. Dollars|[\d,]+ Trillion
dollarRule = "|".join([dSignWithTMBT, dollarsWithTMBT, usDollarsWithTMBT])



try:
    path = config.projectMainFolder + 'stop_words.txt'
    with open(path) as f:
        stopWordsList = f.read().splitlines()
except IOError:
    print("Can't find path:",path)



def findByRule(rule, term):
    find = re.findall(rule, term)
    if (len(find) > 0):
        return True
    return False




def convertTokenToTerm(token):
    # return token
    import Parsing.ConvertMethods as convert
    term = token
    global betweenRule, hasMonthRule, monthBeforeRule, monthAfterRule, combainedRule, percentRule, numWithTMBTRule, dollarRule

    termAsArray = term.split(' ')
    if len(termAsArray) > 1:
        # BetweenRule
        if findByRule(betweenRule, term):
            return termAsArray[1] + '-' + termAsArray[3]

        # todo - add yearRule
        if findByRule(hasMonthRule, term):
            if basic.isInt(termAsArray[0]):
                return convert.convertMonthToInt(termAsArray[1][:3].lower()) + '-' + termAsArray[0]
            elif basic.isInt(termAsArray[1]):
                return convert.convertMonthToInt(termAsArray[0][:3].lower()) + '-' + termAsArray[1]

        # PercentRule
        if findByRule(percentRule, term):
            num = termAsArray[0]
            if num[0] == '0':
                num = num[1:]
            return num + '%'


        if findByRule(dollarRule, term):
            if term[0] == '$':
                termAsArray[0] = convert.convertNumToMoneyFormat(termAsArray[0][1:])

        if findByRule(dollarRule,term):
            if len(termAsArray) > 2:
                tmbtAsNum = convert.convertTMBT_toNum(termAsArray[1].lower())
                number = int(termAsArray[0])*tmbtAsNum
            return convert.convertNumToMoneyFormat(str(number)) + " Dollars"

        if findByRule(numWithTMBTRule,term):
            tmbtLetter = convert.convertTMBT_toLetter(termAsArray[1].lower())
            if tmbtLetter == 'T':
                if basic.isInt(termAsArray[0]):
                    return str(int(termAsArray[0]) * 1000) + 'B'
                return str(float(termAsArray[0]) * 1000)[:6].strip('0') + 'B'
            return termAsArray[0] + tmbtLetter


    else:
        termAsArray = term.split('-')
        if len(termAsArray) > 1:
            splitedTerm = term.replace('-',' ')

            # PercentRule
            if findByRule(percentRule, splitedTerm):
                num = termAsArray[0]
                if num[0] == '0':
                    num = num[1:]
                return num + '%'


            if findByRule(dollarRule, splitedTerm):
                if splitedTerm[0] == '$':
                    termAsArray[0] = convert.convertNumToMoneyFormat(termAsArray[0][1:])

                if findByRule(numWithTMBTRule, splitedTerm):
                    tmbtLetter = convert.convertTMBT_toLetter(termAsArray[1].lower())
                    if tmbtLetter == 'T':
                        if basic.isInt(termAsArray[0]):
                            return str(int(termAsArray[0]) * 1000) + 'B'
                        return str(float(termAsArray[0]) * 1000)[:6].strip('0') + 'B'
                    return termAsArray[0] + termAsArray[1] + tmbtLetter

            if findByRule(numWithTMBTRule, splitedTerm):
                tmbtLetter = convert.convertTMBT_toLetter(termAsArray[1].lower())
                if tmbtLetter == 'T':
                    if basic.isInt(termAsArray[0]):
                        return str(int(termAsArray[0]) * 1000) + 'B'
                    return str(float(termAsArray[0]) * 1000)[:6].strip('0') + 'B'
                return termAsArray[0] + tmbtLetter


        else:

            if findByRule(dollarRule, term):
                if term[0] == '$':
                    term[0] = convert.convertNumToMoneyFormat(term[1:])

                tmbtLetter = convert.convertTMBT_toLetter(term.lower())
                if tmbtLetter == 'T':
                    if basic.isInt(term):
                        return str(int(term) * 1000) + 'B'
                    return str(float(term) * 1000)[:6].strip('0') + 'B'
                return term + tmbtLetter

            if findByRule(numWithTMBTRule, term):
                tmbtLetter = convert.convertTMBT_toLetter(termAsArray[1].lower())
                if tmbtLetter == 'T':
                    if basic.isInt(termAsArray[0]):
                        return str(int(termAsArray[0]) * 1000) + 'B'
                    return str(float(termAsArray[0]) * 1000)[:6].strip('0') + 'B'
                return termAsArray[0] + tmbtLetter


    return term




def getRegexMatches(expression, text, toStem = False):
    import Stemmer.Stemmer

    from Indexing.MyDictionary import updateTermToDictionaryByTheRules
    termDictionary = {}
    pattern = re.compile(expression)
    matches = pattern.finditer(text)
    # matches = pattern.findall(text)
    # matches = tokinizer(text)
    for match in matches:
        # matchStart = match.start()
        token = match.group()
        if token.lower() in stopWordsList:
            continue
        if toStem:
            token = Stemmer.Stemmer.stemTerm(token)
        count = 1
        term = convertTokenToTerm(token)
        termFromDic = updateTermToDictionaryByTheRules(termDictionary,term)
        termDataFromDic = termDictionary.get(termFromDic)
        if termDataFromDic is not None:
            count = termDataFromDic.termFrequency + 1
            termDataFromDic.termFrequency = count
            continue

        # newTerm = TermData(count, matchStart)
        newTerm = TermData(count, 0)
        termDictionary[termFromDic] = newTerm

    return termDictionary


def runExpression(regexFunction):
    print("\n\n***      Running         ***\n")

    regexFunction()

    print("\n\nDONE")




def tokenizeRegex(text, fromFile = True):
    # print("tokenizeRegex")
    from Indexing.Document import Document
    tokenizeExpression = '|'.join([betweenRule,monthBeforeRule,monthAfterRule,combainedRule,percentRule,dollarRule,numWithTMBTRule])
    tokenizeExpression = tokenizeExpression + '|' + "[a-zA-Z]+"
    # tokenizeExpression = "\d+"


    docNo = 'test'
    if fromFile:
        try:
            docNo = re.findall(r'<DOCNO>(.*?)</DOCNO>', text)[0]
            onlyText = text.split("<TEXT>")[1]
            text = onlyText
        except IndexError:
            print("ERROR - Regex - tokenizeRegex")
        # print(text)
    termDictionary = getRegexMatches(tokenizeExpression, text)
    return Document(docNo,termDictionary)
    # return [docNo,None]






textToCheck = '''  bla bla 12 jan bla '''
# '''
# 2,522,421 Million Dollars ... U.S. Dollars 542 Thousand and 15 Trillion
# March 24 ... between 20 and 40, 80% cost $25 today-tomorrow\n 8,324 U.S. Dollars will be 60 percent"
# '''
tokenizeRegex(textToCheck,False)





'''
.       - Any Character Except New Line
\d	Any decimal digit (equivalent to [0-9])
\D	Any non-digit character (equivalent to [^0-9])
\s	Any whitespace character (equivalent to [ \t\n\r\f\v])
\S	Any non-whitespace character (equivalent to [^ \t\n\r\f\v])
\w	Any alphanumeric character (equivalent to [a-zA-Z0-9_])
\W	Any non-alphanumeric character (equivalent to [^a-zA-Z0-9_])
\t	The tab character
\n	The newline character

\b      - Word Boundary
\B      - Not a Word Boundary
^       - Beginning of a String
$       - End of a String

[]      - Matches Characters in brackets
[^ ]    - Matches Characters NOT in brackets
|       - Either Or
( )     - Group

Quantifiers:
*       - 0 or More
+       - 1 or More
?       - 0 or One
{3}     - Exact Number
{3,4}   - Range of Numbers (Minimum, Maximum)


#### Sample Regexs ####

[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+





'''






'''

#ALL THESE REQUIRE THE WHOLE STRING TO BE A NUMBER
#For numbers embedded in sentences, see discussion below

#### NUMBERS AND DECIMALS ONLY ####
#No commas allowed
#Pass: (1000.0), (001), (.001)
#Fail: (1,000.0)
^\d*\.?\d+$

#No commas allowed
#Can't start with "."
#Pass: (0.01)
#Fail: (.01)
^(\d+\.)?\d+$

#### CURRENCY ####
#No commas allowed
#"$" optional
#Can't start with "."
#Either 0 or 2 decimal digits
#Pass: ($1000), (1.00), ($0.11)
#Fail: ($1.0), (1.), ($1.000), ($.11)
^\$?\d+(\.\d{2})?$

#### COMMA-GROUPED ####
#Commas required between powers of 1,000
#Can't start with "."
#Pass: (1,000,000), (0.001)
#Fail: (1000000), (1,00,00,00), (.001)
^\d{1,3}(,\d{3})*(\.\d+)?$

#Commas required
#Cannot be empty
#Pass: (1,000.100), (.001)
#Fail: (1000), ()
^(?=.)(\d{1,3}(,\d{3})*)?(\.\d+)?$

#Commas optional as long as they're consistent
#Can't start with "."
#Pass: (1,000,000), (1000000)
#Fail: (10000,000), (1,00,00)
^(\d+|\d{1,3}(,\d{3})*)(\.\d+)?$

#### LEADING AND TRAILING ZEROES ####
#No commas allowed
#Can't start with "."
#No leading zeroes in integer part
#Pass: (1.00), (0.00)
#Fail: (001)
^([1-9]\d*|0)(\.\d+)?$

#No commas allowed
#Can't start with "."
#No trailing zeroes in decimal part
#Pass: (1), (0.1)
#Fail: (1.00), (0.1000)
^\d+(\.\d*[1-9])?$



'''


def test():
    import re

    txt = 'this is a paragraph with<[1> in between</[1> and then there are cases ... where the<[99> number ranges from 1-100</[99>.  and there are many other lines in the txt files with<[3> such tags </[3>'

    out = re.sub("(<[^>]+>)", '===<ROY>', txt)
    print(out)


def test2():
    import re

    def multiple_replace(dict, text):
        # Create a regular expression  from the dictionary keys
        regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

        # For each match, look-up corresponding value in dictionary
        return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)

    if __name__ == "__main__":
        text = "Larry Wall is the creator of Perl"

        dict = {
            "Larry Wall": "Guido van Rossum",
            "creator": "Benevolent Dictator for Life",
            "Perl": "Python",
        }

        print(multiple_replace(dict, text))



# test2()

