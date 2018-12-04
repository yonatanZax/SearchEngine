

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

                    findMeArray = re.findall(r'<F P=104>', documentAsString)
                    if len(findMeArray) > 0:
                        cityCount += 1


                counterTotal += 1



        print('Total docs:      ',counterTotal)
        # print('With docNo:  ', counterWithDocNo)
        # print('OnlyText docs:   ', counterOnlyText)
        # print('meter count:  ', counterMeter)
        # print('km count:  ', counterKM)
        print('City count: ',cityCount)




# from Configuration import ConfigClass
# configClass = ConfigClass()
# reader = ReadFile(configClass)
#
# reader.readAllDocs()



text = ''''''
# import re
# filteredText2 = re.sub(r"[A-Z]?[a-z]+ [A-Z]?[a-z]+ \([A-Z][A-Z]\)", "ZAX",text)
# filteredText3 = re.sub(r"[A-Z]?[a-z]+[ -][A-Z]?[a-z]+ [A-Z][a-z]+ \([A-Z][A-Z][A-Z]\)", "ZAX",text)
# filteredText4 = re.sub(r"[A-Z]?[a-z]+ [A-Z]?[a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ \([A-Z][A-Z][A-Z][A-Z]\)", "ZAX",text)
# filteredText3AND = re.sub(r"[A-Z]?[a-z]+\n? [A-Z]?[a-z]+\n? and\n? [A-Z]?[a-z]+\n? \([A-Z][A-Z][A-Z]\)", "ZAX",text)
# # print(filteredText2)
# # print(filteredText3)
# # print(filteredText4)
# # print(filteredText3AND)
# t = "Nippon Credit Bank (NCB)"
# filteredText3 = re.sub(r"[A-Z]?[a-z]+ [A-Z]?[a-z]+ [A-Z][a-z]+ \([A-Z][A-Z][A-Z]\)", "ZAX",t)
# print(filteredText3)
# t2 = "construct a local-area network (LAN) that will combine image "
# filteredText3 = re.sub(r"[A-Z]?[a-z]+[ -][A-Z]?[a-z]+ [A-Z]?[a-z]+ \([A-Z][A-Z][A-Z]\)", "ZAX",t2)
# print(filteredText3)
# test = "the Japan Broadcasting Corp. (NHK), Nippon Telegraph and Telephone (NTT),"
# filteredText3AND = re.sub(r"[A-Z]?[a-z]+\n? [A-Z]?[a-z]+\n? and\n? [A-Z]?[a-z]+\n? \([A-Z][A-Z][A-Z]\)", "ZAX",test)
# print(filteredText3AND)
