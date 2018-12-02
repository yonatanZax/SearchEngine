

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
    numAsFloat = float(removeCommasFromNumber(numAsString.rstrip('.')))
    moduloMillion = numAsFloat/1000000
    if moduloMillion >= 1:
        if str(moduloMillion).endswith('.0'):
            moduloMillion = int(moduloMillion)
        return (str("{0:.2f}".format(round(moduloMillion,2))).rstrip('0').rstrip('.') + ' M')
    else:
        # if str(numAsFloat).endswith('.0'):
        #     numAsFloat = int(numAsFloat)
        return str(str("{0:.2f}".format(round(numAsFloat,2))).rstrip('0').rstrip('.'))


def convertNumToKMBformat(numAsString):
    numToFloat = removeCommasFromNumber(numAsString)
    from BasicMethods import isfloat
    if isfloat(numToFloat):
        numAsFloat = float(numToFloat)
        moduloMillion = numAsFloat / 100000000
        if moduloMillion >= 1:
            return (str("{0:.2f}".format(round(moduloMillion,2))).rstrip('0').rstrip('.') + ' B')
        elif moduloMillion * 100 >= 1:
            return (str("{0:.2f}".format(round(moduloMillion*100,2))).rstrip('0').rstrip('.') + ' M')
        elif moduloMillion * 100000 >= 1:
            return (str("{0:.2f}".format(round(moduloMillion*100000,2))).rstrip('0').rstrip('.') + ' K')
        else:
            return str("{0:.2f}".format(round(numAsFloat,2))).rstrip('0').rstrip('.')
    else:
        return numToFloat.rstrip('0').rstrip('.')


def removeCommasFromNumber(numAsString):
    return numAsString.replace(',','')





