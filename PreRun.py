from BasicMethods import getTagFromText
import Configuration as config
from ReadFiles.ReadFile import ReadFile
import os


# Getting better results for cities
keepGoingCityDic = {'new', 'san', 'sao', 'la', 'tel', 'santa', 'hong', 'xian', 'cape', 'rio', 'buenos', 'panama','mexico', 'guatemala', 'abu'}
avoidCities = {'bartaman', 'dokumentation', 'nezavisimaya', 'calcutta', 'the', 'air'}



def getFlagDicFromDocument(documentAsString):
    '''
    This methods receives text and creates a dictionary of flags in the text
        * Using getTagFromText in BasicMethods
    :param documentAsString: Document text from file
    :return: A dictionary with relevant flags from the text
    '''
    flagDic = {}
    flagDic["text"] = getTagFromText(documentAsString, "<TEXT>", "</TEXT>")
    flagDic["docNo"] = getTagFromText(documentAsString, '<DOCNO>', '</DOCNO>')
    flagDic["city"] = getTagFromText(documentAsString, "<F P=104>", "</F>")
    flagDic["language"] = getTagFromText(documentAsString, "<F P=105>", "</F>")

    cityLine = flagDic.get('city')

    # Code from Parse - set city properly
    if len(cityLine) > 1:
        splittedCity = cityLine.replace('\n', ' ').strip(' ').split(' ')
        city = splittedCity[0]
        if city.lower() in keepGoingCityDic and len(splittedCity) > 1:
            city = city + ' ' + splittedCity[1].strip(' ')
            if len(splittedCity) > 2 and splittedCity[1].lower() in ['de']:
                city = city + ' ' + splittedCity[2].strip(' ')

        if city.isalpha() and city.lower() not in avoidCities:
            flagDic["text"] = flagDic["text"].replace(city, 'ZAXROY')
            flagDic["city"] = city
        else:
            flagDic["city"] = ''


    return flagDic



def createPreRunDics(fileList,fileReader):
    '''
    This method creates two dictionaries:
    1. File_Index list - every file name is connected to it's first doc index
    2. City dictionary - all the cities from doc tag "<F P=104>"
    :param fileList: List of file names from the corpus
    :param fileReader: FileReader class
    :return: A tuple: 1. file_index , 2. cityDic
    '''
    cityDic = {}
    filesIndexTupleList = []
    counter = 1


    for fileName in fileList:
        firstFileIndex = counter

        # Get a list of documents from file
        documentList = fileReader.readTextFile(fileName)
        for documentAsString in documentList:

            # Get relevant flags from this document
            flagDic = getFlagDicFromDocument(documentAsString)
            if flagDic:
                if not flagDic.get('text') is None:
                    if len(flagDic.get('text')) > 20:
                        if firstFileIndex == 0:
                            firstFileIndex = counter
                        else: counter += 1

                        # Add new city to the cities dictionary
                        if not flagDic.get('city') == '':
                            cityDic[flagDic.get('city')] = True

        # After all the documents, add a tuple of <FileName,index>
        filesIndexTupleList.append([fileName,firstFileIndex])


    return filesIndexTupleList, cityDic




# con = config.ConfigClass()
# reader = ReadFile(con)
#
# fileList = os.listdir(con.get__corpusPath())
# createPreRunDics(fileList,reader)










