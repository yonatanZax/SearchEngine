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
        numberOfDocuments = 0
        for folder in self.folderList:

            counter += 1
            documentsList = self.fileReader.readTextFile(folder)
            for document in documentsList:
                parsedDocument = self.parser.parseDoc(document)
                if parsedDocument is None:
                    continue
                numberOfDocuments += 1
                self.indexer.addNewDoc(parsedDocument)

            if counter == self.filesPerIteration:
                self.indexer.flushMemory()
                counter = 0


        if counter != 0:
            self.indexer.flushMemory()

        print("Manager " , str(self.ID) , " Finished parsing all files, Parsed: " , str(numberOfDocuments), " Docs")

        self.indexer.merge()

        print("Manager " , str(self.ID) , " Finished merging his files")

        return numberOfDocuments


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
        print ("Got manager " , str(self.ID) , ' run')

    def getMerge(self):
        print ("Got manager " , str(self.ID) , ' merge')


