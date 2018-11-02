
import os
import Configuration as config
from Indexing.Indexer import Indexer
from ReadFiles.ReadFile import ReadFile



def initProject():
    print('Create folders')




def main():
    print("***   Main Start   ***")


    corpusPath = config.getAbsolutePathToDataFolderAndFileType('corpus')
    listOfFolders = os.listdir(corpusPath)

    for folder in listOfFolders:
        print(folder)
        folderPath = corpusPath + '\\' + folder
        filePath = folderPath + '\\' + folder
        myIndexer = Indexer()
        readFile = ReadFile(myIndexer, corpusPath)
        readFile.readTextFile(filePath=filePath)
        print(myIndexer.dictionary)


    print('***   Done   ***')








if __name__ == "__main__":
    main()