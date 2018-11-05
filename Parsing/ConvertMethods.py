






'''
Jan.
Feb.
Mar.
Apr.
May
June
July
Aug.
Sept.
Oct.
Nov.
Dec.
'''


def convertMonthToInt(month):
    # January | February | March | April | May | June
    # July | August | September | October | November | December

    return {
        'jan': '01',
        'feb': '02',
        'mar': '03',
        'apr': '04',
        'may': '05',
        'june': '06',
        'july': '07',
        'aug': '08',
        'sep': '09',
        'oct': '10',
        'nov': '11',
        'dec': '12',
    }[month]


def convertTMBT_toLetter(tmbt):
    # January | February | March | April | May | June
    # July | August | September | October | November | December

    return {
        'thousand': 'K',
        'million': 'M',
        'billion': 'B',
        'trillion': 'T',
    }[tmbt]


def convertTMBT_toNum(tmbt):
    tmbtLetter = convertTMBT_toLetter(tmbt)
    return {
        'T': 1000,
        'M': 1000000,
        'B': 1000000000,
        'T': 1000000000000,
    }[tmbtLetter]


def convertNumToMoneyFormat(numAsString):
    numAsFloat = float(removeCommasFromNumber(numAsString))
    moduloMillion = numAsFloat/1000000
    if moduloMillion >= 1:
        if str(moduloMillion).endswith('.0'):
            moduloMillion = int(moduloMillion)
        return (str(moduloMillion)[:6] + 'M')
    else:
        if str(numAsFloat).endswith('.0'):
            numAsFloat = int(numAsFloat)
        return str(numAsFloat)


def convertNumToKMBformat(numAsString):
    numAsFloat = float(removeCommasFromNumber(numAsString))
    moduloMillion = numAsFloat / 1000000000
    if moduloMillion >= 1:
        return (str(moduloMillion)[:6].strip('0') + 'B')
    elif moduloMillion*100 >= 1:
        return (str(moduloMillion*100)[:6].strip('0') + 'M')
    elif moduloMillion*100000 >= 1:
        return (str(moduloMillion*100000)[:6].strip('0') + 'K')
    else:
        return str(numAsFloat)[:6].strip('0')


def removeCommasFromNumber(numAsString):
    return numAsString.replace(',','')

