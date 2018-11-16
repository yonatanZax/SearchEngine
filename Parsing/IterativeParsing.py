import re
import BasicMethods as basic
import Configuration as config
from Indexing.Document import TermData
import nltk


stopWordsList = {}
try:
    path = config.projectMainFolder + 'stop_words.txt'
    with open(path) as f:
        for word in  f.read().splitlines():
            stopWordsList[word] = None
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

# numberWithCommasRule
nwcr = "[\d,]+"
betweenRule = "[Bb]etween " + nwcr + " and " + nwcr
# January | February | March | April | May | June | July | August | September | October | November | December
#monthList = ["[Jj]anuary", "[Ff]ebruary", "[Mm]arch", "[Aa]pril"]
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

# '[\\d,]+ [Tt]housand|[\\d,]+ [Mm]illion|[\\d,]+ [Bb]illion|[\\d,]+ [Tt]rillion'
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

