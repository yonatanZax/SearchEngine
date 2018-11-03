






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




def convertNumToMoneyFormat(numAsString):
    numAsFloat = float(removeCommasFromNumber(numAsString))
    moduloMillion = numAsFloat/1000000
    if moduloMillion >= 1:
        return (str(moduloMillion)[:6] + 'M')
    else:
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

    # from django.conf import settings
    # settings.configure()
    # from django.core.wsgi import get_wsgi_application
    # application = get_wsgi_application()
    # from django.contrib.humanize.templatetags.humanize import intword as convertNumbers
    # numAsInt = float(numAsInt)
    # numFromDjango = convertNumbers(numAsInt)



# print(convertNumToKMBformat(removeCommasFromNumber('5,020,553,464')))




