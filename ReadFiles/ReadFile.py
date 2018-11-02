
import Configuration as config
import os
from Parsing.Parse import Parse
from Indexing.Document import Document
from Indexing.Indexer import Indexer
from MyExecutors import MyExecutors
import MyExecutors


class ReadFile:

    def __init__(self, indexer, mainPath):
        self.path = mainPath
        self.myIndexer = indexer
        self.listOfFolders = os.listdir(self.path)

    def readAllFiles(self):

        # MyExecutors._instance.IOExecutor.map(self.readTextFile, self.listOfFolders, 10)

        for folder in self.listOfFolders:
            print(folder)

            MyExecutors._instance.IOExecutor.apply(func=self.readTextFile, args=(folder,))


            # self.readTextFile(filePath=filePath)
            # print(myIndexer.dictionary)

    def readTextFile(self, fileName):

        # try:
            folderPath = self.path + '\\' + fileName
            filePath = folderPath + '\\' + fileName
            myFile = open(filePath,'r')
            fileAsText = myFile.read()
            documents = fileAsText.split('</DOC>')[:-1]
            parser = Parse(self.myIndexer)
            for doc in documents:
                parser.parseDoc(doc)

            myFile.close()







