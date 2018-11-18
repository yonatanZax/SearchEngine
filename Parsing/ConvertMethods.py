






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

    return {
        'thousand': 'K',
        'million': 'M',
        'billion': 'B',
        'trillion': 'T',
    }[tmbt]


def convertTMBT_toNum(tmbtString, letter=None):
    if letter:
        tmbtLetter = letter.upper()
    else:
        tmbtLetter = convertTMBT_toLetter(tmbtString)
    return {
        'K': 1000,
        'M': 1000000,
        'B': 1000000000,
        'T': 1000000000000,
    }[tmbtLetter]


def convertNumToMoneyFormat(numAsString):
    numToFloat = removeCommasFromNumber(numAsString)
    from BasicMethods import isfloat
    if isfloat(numToFloat):
        numAsFloat = float(removeCommasFromNumber(numAsString))
        moduloMillion = numAsFloat / 1000000
        if moduloMillion >= 1:
            if str(moduloMillion).endswith('.0'):
                moduloMillion = int(moduloMillion)
            return (str(moduloMillion)[:7] + ' M')
        else:
            if str(numAsFloat).endswith('.0'):
                numAsFloat = int(numAsFloat)
            return str(numAsFloat)
    else:
        return numToFloat.strip('0').strip('.')


def convertNumToKMBformat(numAsString):
    numToFloat = removeCommasFromNumber(numAsString)
    from BasicMethods import isfloat
    if isfloat(numToFloat):
        numAsFloat = float(numToFloat)
        moduloMillion = numAsFloat / 1000000000
        if moduloMillion >= 1:
            return (str(moduloMillion)[:6].strip('0').strip('.') + ' B')
        elif moduloMillion * 100 >= 1:
            return (str(moduloMillion * 100)[:6].strip('0').strip('.') + ' M')
        elif moduloMillion * 1000000 >= 1:
            return (str(moduloMillion * 1000000)[:6].strip('0').strip('.') + ' K')
        else:
            return str(numAsFloat)[:6].strip('0').strip('.')
    else:
        return numToFloat.strip('0').strip('.')


def removeCommasFromNumber(numAsString):
    return numAsString.replace(',','')

