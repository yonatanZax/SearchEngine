from Indexing.Indexer import Indexer
from ReadFiles.ReadFile import ReadFile
from Parsing.Parse import Parse
from Indexing.FileWriter import FileWriter
from datetime import datetime
from concurrent.futures import as_completed
import os



class MyManager:

    def __init__(self, managerID, filesIndexTupleList, lettersList, config):

        # Init class fields
        self.ID = managerID
        self.config = config
        self.filesIndexTupleList = filesIndexTupleList

        self.indexer = Indexer(managerID,config=config)
        self.fileReader = ReadFile(config=self.config)
        self.fileWriter = FileWriter(self.config)
        self.parser = Parse(config=self.config)
        self.lettersList = lettersList



    def updateProgressBar(self, value, posting_merge):

        # Write file to indicate the progress bar

        path = self.config.get__savedFilePath() + '/Progress/%s' % (posting_merge)
        fileName = str(self.ID) + '_' + str(value)

        if os.path.exists(path):
            myFile = open(path + '/' + fileName, 'w')
            myFile.close()



    def run(self):
        """
        The main function of the manager
        runs the parsing, indexing and merging of his files
        :return:numberOfDocuments:int, parsingTime.seconds:int, mergingTime.seconds:int
        """

        # init values
        start = datetime.now()
        counter = 0
        numberOfDocuments = 0
        totalCount = 0

        # Iterate over files in list - read, parse, index
        filesPerIteration = self.config.filesPerIteration
        for fileName, index in self.filesIndexTupleList:
            documentIndex = 0
            counter += 1
            documentsList = self.fileReader.readTextFile(fileName)
            # Iterate over every document in the file
            for document in documentsList:
                # parse the document

                parsedDocument = self.parser.parseDoc(document)
                if parsedDocument is None:
                    continue
                numberOfDocuments += 1

                # index the document data
                self.indexer.addNewDoc(parsedDocument,docNoAsIndex=index + documentIndex)
                documentIndex += 1
            # every set number of times flush the data to the disk
            if counter == filesPerIteration:
                totalCount += counter
                self.updateProgressBar(totalCount,'Posting')
                self.indexer.flushMemory()
                counter = 0



        # is there is data that haven't been flush flush it now..
        if counter != 0:
            totalCount += counter
            self.updateProgressBar(totalCount,'Posting')
            self.indexer.flushMemory()

        finishedParsing = datetime.now()
        parsingTime = finishedParsing - start


        print("Manager " , str(self.ID) , " Finished parsing all files, Parsed: " , str(numberOfDocuments), " Docs, Took: ", str(parsingTime.seconds))
        # start merging the data that the manager created

        self.indexer.merge()

        finishedMerging = datetime.now()
        mergingTime = finishedMerging - finishedParsing

        # Done local merge!!
        print("Manager " , str(self.ID) , " Finished merging his files, Took: " , str(mergingTime.seconds))

        return numberOfDocuments, parsingTime.seconds, mergingTime.seconds


    def merge(self):
        """
        This function will start the merging final process. every manager will merge the letters he was responsible for
        :return: sumOfTerms:int, mergingTime.seconds:int
        """
        from Indexing.KWayMerge import Merger
        import os
        from concurrent.futures import ThreadPoolExecutor

        # Init fields
        start = datetime.now()
        merger = Merger(self.config)
        sumOfTerms = 0
        executor = ThreadPoolExecutor()
        futureList = []
        progressCounter = 0

        # Iterate over every letter the manager is responsible
        for letter in self.lettersList:

            filesInLetterFolder = os.listdir(self.config.savedFilePath + "\\" + letter)

            # Make global merge
            mergedList = merger.merge(filesInLetterFolder)

            # Update progress bar
            if mergedList is None:
                progressCounter += 50
                self.updateProgressBar(progressCounter + int(self.config.get_numOfFiles() / self.config.managersNumber),
                                       'Merge')
                continue

            # Add future to list
            future = executor.submit(self.fileWriter.writeMergedFile,mergedList, self.config.savedFilePath + "\\" + letter + "\\",)
            futureList.append(future)

            # update progress bar
            progressCounter += 50
            self.updateProgressBar(progressCounter + int(self.config.get_numOfFiles()/self.config.managersNumber),'Merge')

        # Get values from future list
        for future in as_completed(futureList):
            sumOfTerms += future.result()

        finish = datetime.now()

        mergingTime = finish - start

        # Close ThreadPoolExecutor
        executor.shutdown()

        return sumOfTerms, mergingTime.seconds


    def getCityDictionary(self):
        return self.indexer.city_dictionary

    def getRun(self):
        print ("Got manager " , str(self.ID) , ' run')

    def getMerge(self):
        print ("Got manager " , str(self.ID) , ' merge')


