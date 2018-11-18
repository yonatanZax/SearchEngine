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
            self.indexer = Indexer()
        self.fileReader = ReadFile()
        self.parser = Parse()
        # self.lock = Lock()
        self.result = None
        self.toStem = toStem

    def start(self, pool=None):
        if pool is None:
            x= 0
            # self.result = MyExecutors._instance.CPUExecutor.apply_async(self.run())
        else:
            self.result = pool.apply_async(self.run())

    def run(self):
        counter = 0
        flushResultList = []
        for folder in self.folderList:
            if counter < self.filesPerIteration:
                counter += 1
                documentsList = self.fileReader.readTextFile(folder)
                for document in documentsList:

                    parsedDocument = self.parser.parseDoc(document)
                    self.indexer.addNewDoc(parsedDocument)

            else:
                flushResult = self.indexer.flushMemory()
                # flushResultList.append(flushResult)
                counter = 0
        if counter != 0:
            flushResult = self.indexer.flushMemory()
            # flushResultList.append(flushResult)
        for flushResult in flushResultList:
            flushResult.wait()

        print ("Manager " + str(self.ID) + " finished")

    def get(self):
        self.result.wait()