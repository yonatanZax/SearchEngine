
import os
from datetime import datetime
from Manager import MyManager
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from Configuration import ConfigClass
from Indexing.CountriesAPI import CityAPI


config = None

def main():

    mainManager = MainClass()
    mainManager.GUIRun()


class MainClass:

    def __init__(self):

        self.config = ConfigClass()
        self.cityAPI = CityAPI()

    def GUIRun(self):
        from Gui import GuiMainView

        print("***   Main Start   ***")
        root = GuiMainView.Tk()
        root.geometry('600x700')
        # root.geometry('800x1000')
        root.title("SearchEngine")

        guiFrame = GuiMainView.EngineBuilder(root, mainManager=self, config=self.config)
        guiFrame.mainloop()

    def managerRun(self):
        import string
        startTime = datetime.now()
        managersNumber = self.config.get__managersNumber()
        listOfFolders = os.listdir(self.config.get__corpusPath())
        listOfFolders.remove(self.config.get__stopWordFile())

        lettersList = list(string.ascii_lowercase)
        lettersList.append('#')

        managersList = []
        pool = ProcessPoolExecutor()

        for i in range(0, managersNumber):

            folderListPerManager = []
            for j in range(i,len(listOfFolders),managersNumber):
                folderListPerManager.append(listOfFolders[j])

            lettersListPerManager = []

            for j in range(i,len(lettersList), managersNumber):
                lettersListPerManager.append(lettersList[j])

            manager = MyManager(managerID=i, folderList=folderListPerManager,
                                lettersList=lettersListPerManager, config=self.config)

            managersList.append(manager)


        dictionary_city_cityData = {}

        totalNumberOfDocuments = 0
        maxParsingTime = 0
        maxMergingTime = 0

        threadPoolExecutor = ThreadPoolExecutor()
        citiesFutureDic = {}

        mergedLanguagesSet = set()

        future_manager_dic = {pool.submit(self.run, manager): manager for manager in managersList}
        for future_manager in as_completed(future_manager_dic):
            manager = future_manager_dic[future_manager]
            manager.getRun()
            tempCityData , languagesList, numberOfDocs , parsingTime, mergingTime  = future_manager.result()
            totalNumberOfDocuments += numberOfDocs
            maxParsingTime = max(maxParsingTime, parsingTime)
            maxMergingTime = max(maxMergingTime, mergingTime)

            for city, cityData in tempCityData.items():
                if dictionary_city_cityData.get(city) is None:
                    if cityData is None:
                        print("NoneDataCity: " + city)
                        continue
                    dictionary_city_cityData[city] = cityData
                    future = threadPoolExecutor.submit(self.cityAPI.getInformationAsString, city)
                    citiesFutureDic[city] = future
                else:
                    dictionary_city_cityData[city] += cityData

            for language in languagesList:
                if language not in mergedLanguagesSet:
                    mergedLanguagesSet.add(language)
        finishTime = datetime.now()
        timeItTook = finishTime - startTime

        print("Term Posting took: " + str(timeItTook.seconds) + " seconds")

        firstManagerToFinish = True


        # UpdateProgress
        self.updateProgressBar(len(listOfFolders),'Posting')



        totalNumberOfTerms = 0
        maxSecondMergeTime = 0

        future_manager_dic = {pool.submit(self.managerMerge, manager): manager for manager in managersList}
        for future_manager in as_completed(future_manager_dic):
            manager = future_manager_dic[future_manager]
            manager.getMerge()
            numberOfTerms, mergingTime = future_manager.result()
            totalNumberOfTerms += numberOfTerms
            maxSecondMergeTime = max(maxSecondMergeTime, mergingTime)
            if firstManagerToFinish:
                firstManagerToFinish = False
                self.getCitiesDataAndWriteItASync(dictionary_city_cityData, citiesFutureDic)




        finishTime = datetime.now()
        timeItTook = finishTime - startTime

        totalMerging = maxSecondMergeTime + maxMergingTime

        pool.shutdown()
        print("Number of files Processed: " , str(len(listOfFolders)))

        return timeItTook.seconds, maxParsingTime, totalMerging, totalNumberOfTerms, totalNumberOfDocuments, sorted(mergedLanguagesSet)

    @staticmethod
    def run( manager):
        # print("in run main")
        numberOfDocs , parsingTime, finishedMerging = manager.run()
        languagesDic = list(manager.indexer.languagesDic.keys())
        return manager.indexer.city_dictionary, languagesDic, numberOfDocs , parsingTime, finishedMerging



    @staticmethod
    def managerMerge(manager):

        return manager.merge()


    def getCitiesDataAndWriteItASync(self, dictionary_city_cityData, citiesFutureDic):
        writeLine = ''
        listToWrite = []

        for city, future in citiesFutureDic.items():
            try:
                information = future.result()
                if information is None:
                    continue
                cityData = dictionary_city_cityData[city]
                locations = cityData.getDocLocationsAsString()
                listToWrite.append('|'.join([city, information, locations]))
                writeLine = '\n'.join(listToWrite)
            except Exception as ex:
                print('ERROR in API', str(ex))

        if len(writeLine) > 0:
            try:
                path = self.config.savedFilePath + '/cityIndex'
                myFile = open(path, 'a', encoding='utf-8')
                myFile.write(writeLine)
                myFile.close()
            except IOError as ex:
                print(str(ex))
            except UnicodeEncodeError as ex:
                print('ERROR in writing', str(ex))


    def updateProgressBar(self, value, posting_merge):
        path = self.config.get__savedFilePath() + '/Progress/%s' % (posting_merge)
        fileName = '-1_' + str(value)

        if os.path.exists(path):
            myFile = open(path + '/' + fileName, 'w')
            myFile.close()




    #
    # def getCitiesDataAndWriteIt(self,dictionary_city_cityData):
    #     """
    #     writing format: City|Country|Currency|Population|Doc:#loc:loc*,Doc:loc:loc**
    #     :param dictionary_city_cityData:
    #     :return:
    #     """
    #     # writeLine = ''
    #     # for city, cityData in sorted(dictionary_city_cityData.items()):
    #     #     info1 = city
    #     #     info2 = self.cityAPI.getInformationAsString(city)
    #     #     info3 = cityData.getDocLocationsAsString()
    #     #     writeLine += '|'.join([info1,info2,info3,'\n'])
    #     # print(writeLine)
    #     writeLine = ''
    #     listToWrite = []
    #     start = datetime.now()
    #     try:
    #         for city, cityData in sorted(dictionary_city_cityData.items()):
    #             information = self.cityAPI.getInformationAsString(city)
    #             if information is None:
    #                 continue
    #             locations =  cityData.getDocLocationsAsString()
    #             listToWrite.append('|'.join([city, information, locations]))
    #         writeLine = '\n'.join(listToWrite)
    #     except Exception as ex:
    #         print('ERROR in API' , str(ex) )
    #
    #     if len(writeLine) > 0:
    #         try:
    #             path = self.config.savedFilePath + '/cityIndex'
    #             myFile = open(path, 'a', encoding='utf-8')
    #             myFile.write(writeLine)
    #             myFile.close()
    #         except IOError as ex:
    #             print (str(ex))
    #         except UnicodeEncodeError as ex:
    #             print('ERROR in writing' , str(ex))
    #
    #     finish = datetime.now()
    #     timeItTook = finish - start
    #
    #     return timeItTook.seconds
    #
    #
    # def getCitiesDataAndWriteItWithSession(self,dictionary_city_cityData):
    #     """
    #     writing format: City|Country|Currency|Population|Doc:#loc:loc*,Doc:loc:loc**
    #     :param dictionary_city_cityData:
    #     :return:
    #     """
    #     writeLine = ''
    #     listToWrite = []
    #     try:
    #         dictionaryFromAPI = self.cityAPI.getDetailsWithGeobytesWithSession(dictionary_city_cityData.keys())
    #
    #         for cityName in dictionaryFromAPI.keys():
    #             listToWrite.append('|'.join([cityName, dictionaryFromAPI[cityName], dictionary_city_cityData[cityName].getDocLocationsAsString()]))
    #         writeLine = '\n'.join(listToWrite)
    #
    #     except Exception as ex:
    #         print('ERROR in API' , str(ex) )
    #
    #     if len(writeLine) > 0:
    #         try:
    #             path = self.config.savedFilePath + '/cityIndex'
    #             myFile = open(path, 'a', encoding='utf-8')
    #             myFile.write(writeLine)
    #             myFile.close()
    #         except IOError as ex:
    #             print (str(ex))
    #         except UnicodeEncodeError as ex:
    #             print('ERROR in writing' , str(ex))
    #


if __name__ == "__main__":
    main()