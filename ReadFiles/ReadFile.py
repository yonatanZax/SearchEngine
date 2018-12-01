

class ReadFile:

    def __init__(self, config):
        self.config = config
        self.path = self.config.get__corpusPath()


    def _readTextFromFile(self, filePath):

        fileText = self._getText(filePath)
        return fileText


    def _getText(self,filePath):
        file = open(filePath,'r')
        fileText = file.read()
        file.close()
        return fileText

    def readTextFile(self, fileName):
        folderPath = self.path + '\\' + fileName
        filePath = folderPath + '\\' + fileName
        fileAsText = self._readTextFromFile(filePath)
        documents = fileAsText.split('</DOC>')[:-1]
        return documents











