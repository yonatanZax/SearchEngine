
import Configuration as config
from Parsing.Parse import Parse
from Indexing.Document import Document
from Indexing.Indexer import Indexer


class ReadFile():

    def __init__(self, indexer, mainPath):
        self.path = mainPath
        self.myIndexer = indexer


    def readTextFile(self,filePath):

        try:
            myFile = open(filePath,'r')
            fileAsText = myFile.read()
            documents = fileAsText.split('</DOC>')
            parser = Parse(self.myIndexer)
            for doc in documents:
                termsFromParser = parser.parseDoc(doc)
                if termsFromParser is None:
                    continue
                docNo = termsFromParser[0]
                listOfTerms = termsFromParser[1]
                newDoc = Document(docNo,listOfTerms)
                self.myIndexer.addNewDoc(newDoc)

                # print(docNo)

        except IOError:
            print('Error while reading file ', filePath)





# path = 'D:/SearchEngine/corpus/FB396101/FB396101'
# fileReader = ReadFile(path,Indexer())
# fileReader.readTextFile(path)
#
# print("done")
