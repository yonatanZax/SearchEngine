from Indexing.Indexer import Indexer
from ReadFiles.ReadFile import ReadFile
from Parsing.Parse import Parse
# import MyExecutors


class MyManager:

    def __init__(self, managerID, filesPerIteration, folderList, toStem=False, indexer = None):
        self.ID = managerID
        self.filesPerIteration = filesPerIteration
        self.folderList = folderList
        self.indexer = indexer
        if self.indexer is None:
            self.indexer = Indexer(managerID)
        self.fileReader = ReadFile()
        self.parser = Parse()
        # self.lock = RLock()
        self.result = None
        self.toStem = toStem

    def start(self, pool=None):
        if pool is None:
            x= 0
            # self.result = MyExecutors._instance.CPUExecutor.apply_async(self.run())
        else:
            self.result = pool.map(self.run())

    def run(self):
        # self.lock.acquire()
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

        print ("Manager " + str(self.ID) + " finished")

    def get(self):
        print ("Got manager " + str(self.ID))

        # self.result.get()
        # self.lock.acquire()
        # self.lock.release()