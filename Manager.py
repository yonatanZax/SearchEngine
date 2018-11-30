from Indexing.Indexer import Indexer
from ReadFiles.ReadFile import ReadFile
from Parsing.Parse import Parse
from Indexing.FileWriter import FileWriter
class MyManager:



    def __init__(self, managerID, filesPerIteration, folderList, lettersList, config, indexer = None):
        self.ID = managerID

        self.config = config

        self.filesPerIteration = filesPerIteration
        self.folderList = folderList
        self.indexer = indexer
        if self.indexer is None:
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

        self.indexer.merge()

        print ("Manager " + str(self.ID) + " finished")



    def merge(self):
        from Indexing.KWayMerge import Merger
        import os

        merger = Merger(self.config)

        for letter in self.lettersList:

            filesInLetterFolder = os.listdir(self.config.savedFilePath + "\\" + letter)
            mergedList = merger.merge(filesInLetterFolder)


            self.fileWriter.writeMergedFile(mergedList, self.config.savedFilePath + "\\" + letter + "\\")



    def getRun(self):
        print ("Got manager " + str(self.ID) + ' run')

    def getMerge(self):
        print ("Got manager " + str(self.ID) + ' merge')
