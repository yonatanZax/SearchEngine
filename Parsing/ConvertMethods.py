

def convertTMBT_toLetter(tmbt):
    # Get the letter
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

    # Get num values from letter
    return {
        'K': 1000,
        'M': 1000000,
        'B': 1000000000,
        'BN': 1000000000,
        'T': 1000000000000,
    }[tmbtLetter]


def convertNumToMoneyFormat(numAsString):
    # from num to dollar format
    numAsFloat = float(removeCommasFromNumber(numAsString.rstrip('.')))
    moduloMillion = numAsFloat/1000000
    if moduloMillion >= 1:
        # Convert only million in dollar format
        if str(moduloMillion).endswith('.0'):
            moduloMillion = int(moduloMillion)
        return (str("{0:.2f}".format(round(moduloMillion,2))).rstrip('0').rstrip('.') + ' M')
    else:
        return str(str("{0:.2f}".format(round(numAsFloat,2))).rstrip('0').rstrip('.'))


def convertNumToKMBformat(numAsString):

    # Add letter to num if needed
    numToFloat = removeCommasFromNumber(numAsString)
    from BasicMethods import isfloat
    if isfloat(numToFloat):
        numAsFloat = float(numToFloat)
        moduloMillion = numAsFloat / 1000000000
        if moduloMillion >= 1:
            return (str("{0:.2f}".format(round(moduloMillion,2))).rstrip('0').rstrip('.') + ' B')
        elif moduloMillion * 1000 >= 1:
            return (str("{0:.2f}".format(round(moduloMillion*1000,2))).rstrip('0').rstrip('.') + ' M')
        elif moduloMillion * 1000000 >= 1:
            return (str("{0:.2f}".format(round(moduloMillion*1000000,2))).rstrip('0').rstrip('.') + ' K')
        else:
            return str("{0:.2f}".format(round(numAsFloat,2))).rstrip('0').rstrip('.')
    else:
        return numToFloat.rstrip('0').rstrip('.')


def removeCommasFromNumber(numAsString):
    return numAsString.replace(',','')


def converSecondsToTime(numInSeconds):
    import datetime
    return str(datetime.timedelta(seconds=numInSeconds))



