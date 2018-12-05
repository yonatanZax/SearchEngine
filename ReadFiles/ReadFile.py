

class ReadFile:

    def __init__(self, config):
        self.config = config
        self.path = self.config.get__corpusPath()

    @staticmethod
    def _readTextFromFile( filePath):

        file = open(filePath,'r')
        fileText = file.read()
        file.close()
        return fileText


    def readTextFile(self, fileName):
        folderPath = self.path + '\\' + fileName
        filePath = folderPath + '\\' + fileName
        fileAsText = self._readTextFromFile(filePath)
        documents = fileAsText.split('</DOC>')[:-1]
        return documents




    def readAllDocs(self):
        import os
        import re

        counterTotal = 0
        counterWithDocNo = 0
        counterOnlyText = 0
        counterMeter = 0
        counterKM = 0
        cityCount = 0

        cityDic = {}


        listOfFolders = os.listdir(self.config.get__corpusPath())
        listOfFolders.remove(self.config.get__stopWordFile())

        for file in listOfFolders:
            documentList = self.readTextFile(file)



            for documentAsString in documentList:

                topOfText1 = documentAsString[0:int(len(documentAsString) / 6)]
                docNo = re.findall(r'<DOCNO>(.*?)</DOCNO>', topOfText1)
                if len(docNo) > 0:
                    docNo = docNo[0].strip(' ')
                    counterWithDocNo += 1
                    onlyText = documentAsString[documentAsString.find('<TEXT>') + len('<TEXT>'):documentAsString.rfind('</TEXT>')]


                    if len(onlyText) > 20:
                        counterOnlyText += 1
                        if "meter" in onlyText:
                            counterMeter += 1
                        if "km" in onlyText:
                            counterKM += 1

                    findMeArray = re.findall(r'<F P=104>(.*?)</F>', documentAsString)
                    if len(findMeArray) > 0:
                        splittedCity = findMeArray[0].strip(' ').split(' ')
                        city = splittedCity[0]
                        if city.lower() in ['new', 'san', 'sao', 'la', 'tel', 'santa', 'hong', 'xian', 'cape']:
                            city = city + ' ' + splittedCity[1].strip(' ')

                        cityDic[city] = 'city'



                counterTotal += 1



        # print('Total docs:      ',counterTotal)
        # print('With docNo:  ', counterWithDocNo)
        # print('OnlyText docs:   ', counterOnlyText)
        # print('meter count:  ', counterMeter)
        # print('km count:  ', counterKM)
        # print('City count: ',cityCount)
        for city in cityDic.keys():
            city = city.replace("\n", '').replace('\t', '').replace('{', '').replace('}', '').replace('[', '').replace(
                ']',
                '').replace(
                '\"', '').replace('\'', '').replace('(', '').replace(')', '').replace('?', '').replace('!', '').replace(
                '#',
                '').replace(
                '@', '').replace('/', '').replace('\\', '').replace('_', '').replace('>', '').replace('<', '').replace(
                '`',
                '').replace(
                '~', '').replace(';', '').replace(':', '').replace('*', '').replace('+', '').replace('|', '').replace(
                '&',
                '').replace(
                '=', '')
            if len(city) > 1 and city.isalpha():
                print(city)




# from Configuration import ConfigClass
# configClass = ConfigClass()
# reader = ReadFile(configClass)
#
# reader.readAllDocs()


