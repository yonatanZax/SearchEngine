from BasicMethods import getTagFromText
import Configuration as config
from ReadFiles.ReadFile import ReadFile
import os


# Getting better results for cities
keepGoingCityDic = {'new', 'san', 'sao', 'la', 'tel', 'santa', 'hong', 'xian', 'cape', 'rio', 'buenos', 'panama','mexico', 'guatemala', 'abu'}
avoidCities = {'bartaman', 'dokumentation', 'nezavisimaya', 'calcutta', 'the', 'air'}



def getTagDicFromDocument(documentAsString):
    '''
    This methods receives text and creates a dictionary of tags in the text
        * Using getTagFromText in BasicMethods
    :param documentAsString: Document text from file
    :return: A dictionary with relevant flags from the text
    '''
    tagDic = {}
    onlyText = getTagFromText(documentAsString, "<TEXT>", "</TEXT>")
    findTextSquared = onlyText.find('[Text]')
    if findTextSquared > 0:
        onlyText = onlyText[findTextSquared + len('[Text]'):]


    tagDic["text"] = onlyText



    tagDic["docNo"] = getTagFromText(documentAsString, '<DOCNO>', '</DOCNO>')
    tagDic["city"] = getTagFromText(documentAsString, "<F P=104>", "</F>")
    tagDic["language"] = getTagFromText(documentAsString, "<F P=105>", "</F>")

    cityLine = tagDic.get('city')

    # Code from Parse - set city properly
    if len(cityLine) > 1:
        splittedCity = cityLine.replace('\n', ' ').strip(' ').split(' ')
        city = splittedCity[0]
        if city.lower() in keepGoingCityDic and len(splittedCity) > 1:
            city = city + ' ' + splittedCity[1].strip(' ')
            if len(splittedCity) > 2 and splittedCity[1].lower() in ['de']:
                city = city + ' ' + splittedCity[2].strip(' ')

        if city.isalpha() and city.lower() not in avoidCities:
            tagDic["text"] = tagDic["text"].replace(city, 'ZAXROY')
            tagDic["city"] = city
        else:
            tagDic["city"] = ''


    return tagDic



def createPreRunData(fileList: list, fileReader: ReadFile) -> (list,list,dict):
    '''
    This method creates two dictionaries:
    0. File_Index list - every file name is connected to it's first doc index
    1. doc_index list - every docNo is connected to it's index
    2. City dictionary - all the cities from doc tag "<F P=104>"
    :param fileList: List of file names from the corpus
    :param fileReader: FileReader class
    :return: A tuple: 0. file_index , 1. doc_index, 2. cityDic
    '''
    cityDic = {}
    allDocsTuple = []
    filesIndexTupleList = []
    counter = 0


    for fileName in fileList:
        firstFileIndex = counter

        # Get a list of documents from file
        documentList = fileReader.readTextFile(fileName)
        for documentAsString in documentList:

            # Get relevant flags from this document
            tagDic = getTagDicFromDocument(documentAsString)
            if tagDic:
                if not tagDic.get('text') is None:

                    if len(tagDic.get('text')) > 10:

                        # Add new doc to 'allDocsDic'
                        allDocsTuple.append([tagDic['docNo'], str(counter)])

                        counter += 1

                        # Add new city to the cities dictionary
                        if not tagDic.get('city') == '':
                            cityDic[tagDic.get('city')] = True

                # For testing only
                #     else:
                #         print('test')
                #
                # else:
                #     print('test')

        # After all the documents, add a tuple of <FileName,index>
        filesIndexTupleList.append([fileName,firstFileIndex])



    return filesIndexTupleList,allDocsTuple, cityDic




# con = config.ConfigClass()
# reader = ReadFile(con)
#
# fileList = os.listdir(con.get__corpusPath())
# createPreRunDics(fileList,reader)

