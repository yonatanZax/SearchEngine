from Indexing.Indexer import Indexer
from ReadFiles.ReadFile import ReadFile
from Parsing.Parse import Parse
from Indexing.FileWriter import FileWriter
from datetime import datetime
from concurrent.futures import as_completed



class MyManager:

    def __init__(self, managerID, folderList, lettersList, config):
        self.ID = managerID

        self.config = config

        self.folderList = folderList

        self.indexer = Indexer(managerID,config=config)
        self.fileReader = ReadFile(config=self.config)
        self.fileWriter = FileWriter(self.config)
        self.parser = Parse(config=self.config)
        self.lettersList = lettersList



    def run(self):

        start = datetime.now()

        counter = 0
        numberOfDocuments = 0
        filesPerIteration = self.config.filesPerIteration
        for folder in self.folderList:

            counter += 1
            documentsList = self.fileReader.readTextFile(folder)
            for document in documentsList:
                parsedDocument = self.parser.parseDoc(document)
                if parsedDocument is None:
                    continue
                numberOfDocuments += 1
                self.indexer.addNewDoc(parsedDocument)

            if counter == filesPerIteration:
                self.indexer.flushMemory()
                counter = 0


        if counter != 0:
            self.indexer.flushMemory()

        finishedParsing = datetime.now()
        parsingTime = finishedParsing - start


        print("Manager " , str(self.ID) , " Finished parsing all files, Parsed: " , str(numberOfDocuments), " Docs, Took: ", str(parsingTime.seconds))

        self.indexer.merge()

        finishedMerging = datetime.now()
        mergingTime = finishedMerging - finishedParsing


        print("Manager " , str(self.ID) , " Finished merging his files, Took: " , str(mergingTime.seconds))

        return numberOfDocuments, parsingTime.seconds, mergingTime.seconds


    def merge(self):
        from Indexing.KWayMerge import Merger
        import os
        from concurrent.futures import ThreadPoolExecutor

        start = datetime.now()

        merger = Merger(self.config)

        sumOfTerms = 0

        executor = ThreadPoolExecutor()
        futureList = []

        for letter in self.lettersList:

            filesInLetterFolder = os.listdir(self.config.savedFilePath + "\\" + letter)
            mergedList = merger.merge(filesInLetterFolder)

            future = executor.submit(self.fileWriter.writeMergedFile,mergedList, self.config.savedFilePath + "\\" + letter + "\\",)
            futureList.append(future)

        for future in as_completed(futureList):
            sumOfTerms += future.result()

        finish = datetime.now()

        mergingTime = finish - start

        executor.shutdown()

        return sumOfTerms, mergingTime.seconds


    def getCityDictionary(self):
        return self.indexer.city_dictionary

    def getRun(self):
        print ("Got manager " , str(self.ID) , ' run')

    def getMerge(self):
        print ("Got manager " , str(self.ID) , ' merge')


