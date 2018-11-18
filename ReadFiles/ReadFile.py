
import os
import Configuration as config


class ReadFile:

    def __init__(self):
        self.path = config.corpusPath
        self.listOfFolders = os.listdir(self.path)

    def readAllFiles(self):

        # MyExecutors._instance.IOExecutor.map(self.readTextFile, self.listOfFolders, 10)
        # TODO - make this method run on parts of the folders at a time
        for folder in self.listOfFolders:
            # print (folder)

            # MyExecutors._instance.CPUExecutor.apply_async(self.readTextFile, args=(folder,))
            self.readTextFile(folder)
            # self.readTextFile(folder)

            # self.readTextFile(filePath=filePath)
            # print(myIndexer.dictionary)

    def _readTextFromFile(self, filePath):
        # result = MyExecutors._instance.IOExecutor.apply_async(func=self._getText, args=(filePath,))
        # fileText = result.get()
        fileText = self._getText(filePath)
        return fileText

    def _getText(self,filePath):
        file = open(filePath,'r')
        fileText = file.read()
        file.close()
        return fileText

    def readTextFile(self, fileName):

        # try:
            folderPath = self.path + '\\' + fileName
            filePath = folderPath + '\\' + fileName
            fileAsText = self._readTextFromFile(filePath)
            documents = fileAsText.split('</DOC>')[:-1]
            return documents


            # parser = Parse(self.myIndexer)
            for doc in documents:
                # MyExecutors._instance.CPUExecutor.apply_async(self.manager.parser.parseDoc(doc))
                self.manager.parser.parseDoc(doc)

        # except IOError:
        #     print('ERROR: ReadFile - readTextFile - IOError')
        # except IndexError:
        #     print('ERROR: ReadFile - readTextFile - IndexError')
        # except Exception:
        #     print('ERROR: ReadFile - readTextFile - Exception')












