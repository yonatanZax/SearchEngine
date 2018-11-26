import heapq
import Configuration as config
from datetime import datetime

def key(item):
    return item.termLowerCase


class MergeDataClass:

    def __init__(self,termLowerCase, term, DF, sumDF, Posting,Index = 0,file = None):
        self.termLowerCase=termLowerCase
        self.term=term
        self.selfDF=DF
        self.sumDF=sumDF
        self.Posting=Posting
        self.Index=Index
        self.file=file

    def __lt__(self, other):
        return self.termLowerCase < other.termLowerCase

    def __getitem__(self, item):
        if item == 0:
            return self.termLowerCase
        if item == 1:
            return self.term
        if item == 2:
            return self.selfDF
        if item == 3:
            return self.sumDF
        if item == 4:
            return self.Posting
        if item == 5:
            return self.Index
        if item == 6:
            return self.file


class MyHeap(object):
   def __init__(self, initial=None, key=lambda x:x):
       self.key = key
       if initial:
           self.data = [(key(item), item) for item in initial]
           heapq.heapify(self.data)
       else:
           self.data = []

   def push(self, item):
       heapq.heappush(self.data, item)

   def pop(self):
       # return heapq.heappop(self.data)[1]
        return heapq.heappop(self.data)

class Merger:
    """
    Algorithm based on: http://stackoverflow.com/questions/5055909/algorithm-for-n-way-merge
    """

    def __init__(self):
        try:
            # 1. create priority queue

            self._heap = MyHeap(key=key)

        except Exception as err_msg:
            print ("Error while creating Merger: %s" % str(err_msg))

    # TODO - make sure the files already come as full path or check how you want them to come

    # TODO - delete the headline of the temporary posting files

    # TODO - add the dictionary adding logic here


    def merge(self, input_files):
        import os
        """        This method receive a list of file paths representing temporary posting files and merges each term considering
        the DF, SUMTF, and documents
        :param input_files: the files path representing temporary posting files
        :return: a list, where each object in the list is a line for a term
        """
        try:
            # open all files
            open_files = []
            [open_files.append(open(config.savedFilePath + "\\" + file__[0] + "\\" + file__, 'r')) for file__ in input_files]
            filesByLines = []
            i = 0
            # read all the files to a list and close the files
            for file in open_files:
                filesByLines.append(file.readlines())
                i += 1
                file.close()
                os.remove(file.name)

            # 2. Iterate through each file f
            # enqueue the tuple (nextTermIn(file), index of file, file) using the first value as priority key
            for file in filesByLines:
                text = str(file[0])
                splittedLine = text.split('|')
                # the format is: termLowerCase=0, term=1, DF=2, sumDF=3, Posting=4,Index=5,file=6
                self._heap.push(MergeDataClass(splittedLine[0].lower(), splittedLine[0], splittedLine[1], splittedLine[2], splittedLine[3], 0, file))


            FinalList = {}


            # do the first iteration
            currentVal = self._heap.pop()

            currentValTermLower = str(currentVal[0])
            currentValTerm = str(currentVal[1])
            currentValDF = int(currentVal[2])
            currentValSUMTF = int(currentVal[3])
            currentValPosting = currentVal[4].strip('\n')
            currentValIndex = int(int(currentVal[5]) + 1)
            currentValFile = currentVal[6]


            # read next line from current file
            read_line = currentVal[6][currentValIndex]
            # check that this file has not ended
            if len(read_line) != 0:
                splittedLine = read_line.split('|')
                # add next element from current file
                if currentValIndex < len(currentVal[6]):
                    self._heap.push(MergeDataClass(str(splittedLine[0].lower()), splittedLine[0], splittedLine[1], splittedLine[2], splittedLine[3], currentValIndex, currentVal[6]))

            # 3. While queue not empty
            # dequeue head (m, i,f) of queue
            # if f not depleted
            # enqueue (nextTermIn(file), index of file, file)
            while self._heap.data:
                # get the smallest key
                smallest = self._heap.pop()
                smallestTermLower = smallest[0]
                smallestTerm = smallest[1]
                smallestDF = smallest[2]
                smallestSUMTF = smallest[3]
                smallestPosting = smallest[4].strip('\n')
                smallestIndex = int(smallest[5]) + 1
                smallestFile = smallest[6]

                # if its the same as the one we have seen add it's information
                if self.sameTerm(currentValTermLower, smallestTermLower):
                    currentValDF += int(smallestDF)
                    currentValSUMTF += int(smallestSUMTF)
                    currentValPosting += smallestPosting
                    # if their form is different change the form to the lowercase form
                    if not self.sameTerm(currentValTerm, smallestTerm):
                        currentValTerm = currentValTermLower


                # otherwise save the information in FinalList and set the new current value
                else:
                    # write to output file
                    # FinalList.append((str(currentValTerm) + '|' + str(currentValDF) + '|' + str(currentValSUMTF) , currentValPosting))
                    self.addToDic(FinalList,MergeDataClass(currentValTermLower,currentValTerm,currentValDF,currentValSUMTF,currentValPosting))
                    currentValTermLower = smallestTermLower
                    currentValTerm = smallestTerm
                    currentValDF = int(smallestDF)
                    currentValSUMTF = int(smallestSUMTF)
                    currentValPosting = smallestPosting
                    currentValIndex = int(smallestIndex)


                # read next line from current file
                # check that this file has not ended

                # add next element from current file
                if smallestIndex < len(smallestFile):
                    read_line = smallestFile[smallestIndex]
                    splittedLine = read_line.split('|')
                    self._heap.push(MergeDataClass(str(splittedLine[0].lower()), splittedLine[0], splittedLine[1], splittedLine[2], splittedLine[3], smallestIndex, smallestFile))

            # clean up
            # FinalList.append((str(currentValTerm) + '|' + str(currentValDF) + '|' + str(currentValSUMTF),currentValPosting))
            self.addToDic(FinalList, MergeDataClass(currentValTermLower, currentValTerm, currentValDF, currentValSUMTF, currentValPosting))

            # for line in FinalList:
            #     print (line)
            # print ("Number of terms:" + str(len(FinalList)))
            return FinalList.values()
        except Exception as err_msg:
            print ("Error while merging: %s" % str(err_msg))
            raise err_msg

    @staticmethod
    def sameTerm(currentValTerm, smallest):
        """
        compares the term we currently save and the line we currently look at
        :param currentValTerm: the term we current save
        :param smallest: the line we currently look at
        :return: true if its the term and the term in the line are identical
                false if they're not
        """
        return currentValTerm == smallest

    @staticmethod
    def addToDic(dictionary,item):
        # if the item doesn't appear in the dictionary at all
        termTuple = dictionary.get(item[0])
        if termTuple is None:
            dictionary[item[0]] = (str(item[1]) + '|' + str(item[2]) + '|' + str(item[3]),item[4])
        else:
            # meaning the term is in the dictionary
            termDictionaryPartSplitted = termTuple[0].split('|')
            termInDic = termDictionaryPartSplitted[0]
            termDF = int(termDictionaryPartSplitted[1]) + int(item[2])
            termSUMDF = int(termDictionaryPartSplitted[2]) + int(item[3])

            # they don't look the same need to change how it appear
            if termInDic != item[1]:
                termInDic = item[0]

            dictionary[item[0]] = (str(termInDic) + '|' + str(termDF) + '|' + str(termSUMDF), termTuple[1] + item[4])




def test():
    merger = Merger()
    list = merger.merge(['b0_0','b0_1','b1_0','b1_1',])
    for l in list:
        print (l)

# test()
