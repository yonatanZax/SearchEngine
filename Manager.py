from Indexing.Indexer import Indexer
from ReadFiles.ReadFile import ReadFile
from Parsing.Parse import Parse
import Configuration as config


class MyManager:

    def __init__(self, managerID, filesPerIteration, folderList, lettersList, toStem=False, indexer = None):
        self.ID = managerID
        self.filesPerIteration = filesPerIteration
        self.folderList = folderList
        self.indexer = indexer
        if self.indexer is None:
            self.indexer = Indexer(managerID)
        self.fileReader = ReadFile()
        self.parser = Parse()
        self.lettersList = lettersList
        self.toStem = toStem


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

    def merge(self,numberOfManagers):
        from Indexing.KWayMerge import Merger
        from Indexing import FileWriter
        import os

        merger = Merger()

        for letter in self.lettersList:

            filesInLetterFolder = os.listdir(config.savedFilePath + "\\" + letter)
            mergedList = merger.merge(filesInLetterFolder)


            FileWriter.writeMergedFile(mergedList, config.savedFilePath + "\\" + letter + "\\")



    def getRun(self):
        # TODO - return the cities dictionary
        print ("Got manager " + str(self.ID) + ' run')

    def getMerge(self):
        print ("Got manager " + str(self.ID) + ' merge')
