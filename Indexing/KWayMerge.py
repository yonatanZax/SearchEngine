import heapq
import Configuration as config
from datetime import datetime



class Merger:
    """
    Algorithm based on: http://stackoverflow.com/questions/5055909/algorithm-for-n-way-merge
    """

    def __init__(self):
        try:
            # 1. create priority queue

            self._heap = []

        except Exception as err_msg:
            print ("Error while creating Merger: %s" % str(err_msg))

    # TODO - make sure the files already come as full path or check how you want them to come

    # TODO - delete the headline of the temporary posting files

    # TODO - add the dictionary adding logic here

    def merge(self, input_files):
        '''
        This method receive a list of file paths representing temporary posting files and merges each term considering
        the DF, SUMTF, and documents
        :param input_files: the files path representing temporary posting files
        :return: a list, where each object in the list is a line for a term
        '''
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

            # 2. Iterate through each file f
            # enqueue the tuple (nextTermIn(file), index of file, file) using the first value as priority key
            for file in filesByLines:
                text = str(file[0])
                heapq.heappush(self._heap,(text, 0,file))


            FinalList = []
            currentVal = heapq.heappop(self._heap)

            # do the first iteration
            read_line = currentVal[0]
            splittedCurVal = read_line.split('|')
            currentValTerm = splittedCurVal[0]
            currentValDF = int(splittedCurVal[1])
            currentValSUMTF = int(splittedCurVal[2])
            currentValPOSTING = splittedCurVal[3].strip('\n')
            currentValIndex = currentVal[1] + 1
            if len(read_line) != 0:
                # add next element from current file
                heapq.heappush(self._heap, (currentVal[2][currentValIndex],currentValIndex,currentVal[2]))

            # 3. While queue not empty
            # dequeue head (m, i,f) of queue
            # if f not depleted
            # enqueue (nextTermIn(file), index of file, file)
            while self._heap:
                # get the smallest key
                smallest = heapq.heappop(self._heap)

                # if its the same as the one we have seen add it's information
                if self.sameTerm(currentValTerm, smallest[0]):
                    splittedSmallest = smallest[0].split('|')
                    currentValDF += int(splittedSmallest[1])
                    currentValSUMTF += int(splittedSmallest[2])
                    currentValPOSTING += splittedSmallest[3].strip('\n')

                elif self.sameTermDifferentForm(currentValTerm, smallest[0]):
                    currentValTerm = splittedCurVal[0].lower()
                    splittedSmallest = smallest[0].split('|')
                    currentValDF += int(splittedSmallest[1])
                    currentValSUMTF += int(splittedSmallest[2])
                    currentValPOSTING += splittedSmallest[3].strip('\n')

                # otherwise save the information in FinalList and set the new current value
                else:
                    # write to output file
                    FinalList.append(currentValTerm + '|' + str(currentValDF) + '|' + str(currentValSUMTF) + '|' + currentValPOSTING)
                    currentVal = smallest
                    splittedCurVal = currentVal[0].split('|')
                    currentValTerm = splittedCurVal[0]
                    currentValDF = int(splittedCurVal[1])
                    currentValSUMTF = int(splittedCurVal[2])
                    currentValPOSTING = splittedCurVal[3].strip('\n')
                    # currentValIndex = currentVal[1] + 1

                smallestIndex = smallest[1] + 1

                # read next line from current file
                read_line = smallest[2][smallest[1]]
                # check that this file has not ended
                if len(read_line) != 0 :
                    # add next element from current file
                    if smallestIndex < len(smallest[2]):
                        heapq.heappush(self._heap, (smallest[2][smallestIndex],smallestIndex,smallest[2]))

            # clean up
            FinalList.append(currentValTerm + '|' + str(currentValDF) + '|' + str(currentValSUMTF) + '|' + currentValPOSTING)
            # for line in FinalList:
            #     print (line)
            # print ("Number of terms:" + str(len(FinalList)))
            return FinalList
        except Exception as err_msg:
            print ("Error while merging: %s" % str(err_msg))

    @staticmethod
    def sameTerm(currentValTerm, smallest):
        '''
        compares the term we currently save and the line we currently look at
        :param currentValTerm: the term we current save
        :param smallest: the line we currently look at
        :return: true if its the term and the term in the line are identical
                false if they're not
        '''
        smallestTerm = smallest.split('|')[0]
        return currentValTerm == smallestTerm

    @staticmethod
    def sameTermDifferentForm(currentValTerm, smallest):
        '''
        compares the term we currently save and the line we currently look at
        :param currentValTerm: the term we current save
        :param smallest: the line we currently look at
        :return: true if its the term and the term in the line are identical but in different form
                false if they're not
        '''
        smallestTerm = smallest.split('|')[0].lower()
        return currentValTerm.lower() == smallestTerm


