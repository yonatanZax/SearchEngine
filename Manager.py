from Indexing.Indexer import Indexer
from ReadFiles.ReadFile import ReadFile
from Parsing.Parse import Parse
from Indexing.FileWriter import FileWriter
class MyManager:



    def __init__(self, managerID, filesPerIteration, folderList, lettersList, config):
        self.ID = managerID

        self.config = config

        self.filesPerIteration = filesPerIteration
        self.folderList = folderList

        self.indexer = Indexer(managerID,config=config)
        self.fileReader = ReadFile(config=self.config)
        self.fileWriter = FileWriter(self.config)
        self.parser = Parse(config=self.config)
        self.lettersList = lettersList
        self.toStem = self.config.toStem




    def run(self):

        counter = 0
        for folder in self.folderList:

            counter += 1
            documentsList = self.fileReader.readTextFile(folder)
            for document in documentsList:
                parsedDocument = self.parser.parseDoc(document)
                if parsedDocument is None:
                    continue
                self.indexer.addNewDoc(parsedDocument)

            if counter == self.filesPerIteration:
                self.indexer.flushMemory()
                counter = 0


        if counter != 0:
            self.indexer.flushMemory()

        print("Manager " , str(self.ID) , " Finished parsing all files")

        self.indexer.merge()

        print("Manager " , str(self.ID) , " Finished merging his files")

        # self.conn.send(self.indexer.city_dictionary)
        # self.conn.close()
        # self.q.put(self.indexer.city_dictionary)
        # print ("Manager " + str(self.ID) + " finished")


    # def merge(self,numberOfManagers):
    #     import Configuration as config
    #     from Indexing.KWayMerge import Merger
    #     from Indexing import FileWriter
    #     import os
    #
    #     merger = Merger()
    #
    #     for letter in self.lettersList:
    #         for managerID in range(0,numberOfManagers):
    #             filesInLetterFolder = os.listdir(config.savedFilePath + "\\" + letter)
    #             fileToMergeList = []
    #             for letterFile in filesInLetterFolder:
    #                 if letterFile[1] == str(managerID):
    #                    fileToMergeList.append(letterFile)
    #             mergedList = merger.merge(fileToMergeList)
    #             FileWriter.writeMergedFileTemp(mergedList, config.savedFilePath + "\\" + letter + "\\" + str(letter[0]) + str(managerID))
    #
    #         filesInLetterFolder = os.listdir(config.savedFilePath + "\\" + letter)
    #         mergedList = merger.merge(filesInLetterFolder)
    #         FileWriter.writeMergedFile(mergedList, config.savedFilePath + "\\" + letter + "\\")

    def merge(self):
        from Indexing.KWayMerge import Merger
        import os

        merger = Merger(self.config)

        sumOfTerms = 0

        for letter in self.lettersList:

            filesInLetterFolder = os.listdir(self.config.savedFilePath + "\\" + letter)
            mergedList = merger.merge(filesInLetterFolder)

            sumOfTerms += len(mergedList)

            self.fileWriter.writeMergedFile(mergedList, self.config.savedFilePath + "\\" + letter + "\\")

        return sumOfTerms


    def getCityDictionary(self):
        return self.indexer.city_dictionary

    def getRun(self):
        # TODO - return the cities dictionary
        print ("Got manager " , str(self.ID) , ' run')

    def getMerge(self):
        print ("Got manager " , str(self.ID) , ' merge')
