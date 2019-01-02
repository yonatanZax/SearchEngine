
import os
from BasicMethods import getTagFromText
from PreRun import getTagDicFromDocument
from Configuration import ConfigClass
from ReadFiles.ReadFile import ReadFile
#import DataFrames.frames as df

originalDataPath = "../qData"
qrelsPath = "%s/qrels.txt" % (originalDataPath,)
saveFolder = "%s/DataFolder" % (originalDataPath,)

if not os.path.exists(saveFolder):
    os.mkdir(saveFolder)


def getQueryTermsFromFile():
    queryFilePath = "%s/queries.txt" % (originalDataPath,)

    myFile = open(queryFilePath,'r')
    fileAsString = myFile.read()
    listQueryId_terms = []
    queries = fileAsString.split('</top>')[:-1]

    for q in queries:
        id =  getTagFromText(q,'<num> Number: ')
        terms = getTagFromText(q, '<title> ').split(' ')
        listQueryId_terms.append([id,terms])

    return listQueryId_terms


def getDocsData(fileReader,listOfFolders,id_termsList):

    qIdHAS_termHAS_docNoANDcount = {}

    for fileName in listOfFolders:

        # Get a list of documents from file
        documentList = fileReader.readTextFile(fileName)
        for documentAsString in documentList:

            # Get relevant flags from this document
            tagDic = getTagDicFromDocument(documentAsString)
            if tagDic:
                if not tagDic.get('text') is None:

                    if len(tagDic.get('text')) > 10:
                        text = tagDic.get('text')
                        for id_terms in id_termsList:
                            id = id_terms[0]
                            terms = id_terms[1]
                            for t in terms:
                                count = text.count(t)
                                if count > 3:
                                    docNo = tagDic.get('docNo')

                                    value = qIdHAS_termHAS_docNoANDcount.get(id)
                                    if value is not None:
                                        termInQueryId = value.get(t)
                                        if termInQueryId is not None:
                                            termInQueryId.append([docNo , str(count)])
                                        else:
                                            value[t] = [[docNo , str(count)]]
                                    else:
                                        termHas_docNoANDcount = {t:[[docNo , str(count)]]}
                                        qIdHAS_termHAS_docNoANDcount[id] = termHas_docNoANDcount








    print('here')
    for qId,terms in qIdHAS_termHAS_docNoANDcount.items():
        temp2dArray = []
        columnNamesAsArray = []
        listOfColumns = []
        for term, array in terms.items():

            columnNamesAsArray.append(term + ' docNo')
            columnNamesAsArray.append(term + ' count')
            temp2dArray = [['docNo'],['count']]
            for values in array:
                temp2dArray[0].append(values[0])
                temp2dArray[1].append(values[1])

            for col in temp2dArray:
                listOfColumns.append(col[1:])



#        frameToWrite = df.createDataFrameByColumns(columnNamesAsArray,listOfColumns)

        pathToWrite = saveFolder + '/' + qId + '.txt'
        if os.path.exists(pathToWrite):
            os.remove(pathToWrite)

 #       df.writeDataframeToFile(frameToWrite, pathToWrite)





def organizeDataFile():

    fileList = os.listdir(saveFolder)

    for file in fileList:

        myFile = open(saveFolder + '/' + file,'r')
        lines = myFile.readlines()
        headLine = lines[0].strip('\n').strip('|')
        splitHeadLine = headLine.split('|')
        listToWrite = ['DocNo']
        dicList = []
        docSet = set()
        for i in range(0, len(splitHeadLine)):
            if i % 2 == 0:
                dic = {}
                listToWrite += [splitHeadLine[i+1]]
                dicList.append(dic)

        for line in lines[1:]:
            splitedLine = line.strip('\n').split('|')[1:]
            for i in range(0,len(splitedLine)):
                if i%2 == 0:
                    if splitedLine[i] == '':continue
                    docSet.add(splitedLine[i])
                    dicList[int(i/2)][splitedLine[i]] = splitedLine[i+1]


        listToWrite = [listToWrite]
        for doc in docSet:
            values = []
            for dic in dicList:
                fromDoc = dic.get(doc)
                if fromDoc is not None:
                    values.append(fromDoc)
                else:
                    values.append('0')

            listToWrite.append([doc] + values)



        destFile = open(saveFolder + '/fixed_' + file ,'a')
        for line in listToWrite:
            destFile.write('|'.join(line) + '\n')
                # pass
        destFile.close()
        print('ok')


# organizeDataFile()




def splitQrelsFile():

    myFile = open(qrelsPath,'r')
    lines = myFile.readlines()
    myFile.close()
    dic_q_docs = {}
    for line in lines:
        splitedLine = line.strip('\n').split(' ')
        if splitedLine[-1] == '1':
            if dic_q_docs.get(splitedLine[0]) is None:
                dic_q_docs[splitedLine[0]] = [splitedLine[2]]
            else:
                dic_q_docs[splitedLine[0]].append(splitedLine[2])



    for key, values in dic_q_docs.items():

        file = open(originalDataPath + '/qrels_' + key + '.txt','a')
        for v in values:
            file.write(v + '\n')

        file.close()



# splitQrelsFile()




def splitDocs():
    configClass = ConfigClass()
    fileReader = ReadFile(configClass)

    corpusPath = "D:\corpus - full"
    pathToSave = "D:\AllDocs"

    if not os.path.exists(pathToSave):
        os.mkdir(pathToSave)

    listOfFolders = os.listdir(corpusPath)
    myFile = open(pathToSave + '/corpusDocs.txt', 'a')



    for folder in listOfFolders:
        filePath = os.path.join(folder)
        docs = fileReader.readTextFile(filePath)

        for doc in docs:
            docNo = getTagFromText(doc, '<DOCNO>','</DOCNO>')
            myFile.write(docNo + ',' + folder + '\n')


    myFile.close()



# splitDocs()





def checkThis(readFile,listOfFolders):
    listQueryId_terms = getQueryTermsFromFile()

    getDocsData(readFile,listOfFolders,listQueryId_terms)


# config = ConfigClass()
# readFile = ReadFile(config)
# listOfFolders = os.listdir(config.get__corpusPath())
# listOfFolders.remove('stop_words.txt')
# checkThis(readFile,listOfFolders)



