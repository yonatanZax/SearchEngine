
import Configuration as config
from Parsing.Parse import Parse
import threading
import hashlib


class ReadFile:

    def __init__(self, mainPath, indexer):
        self.path = mainPath
        self.myIndexer = indexer
        self.fileList = []
        self.fileListSemaphore = threading.Semaphore()
        self.listCounter = 0
        self.mutex = threading.RLock()
        print('ReadFile created')


    def readTextFile(self, filePath):

        try:
            myFile = open(filePath,'r')
            fileAsText = myFile.read()
            documents = fileAsText.split('</DOC>')
            parser = Parse(self.myIndexer)
            print(documents[0])
            parser.parseDoc(documents[0])

        except IOError:
            print('Error while reading file ', filePath)

    def splitFileToDocumentString(self, filePathString):
        return None

    def getNextFileStringFromList(self):
        return None



    def readFile(self):
        print('ReadFile')




path = 'D:/SearchEngine/corpus/FB396001/FB396001'
fileReader = ReadFile(path, None)
fileReader.readTextFile(path)
