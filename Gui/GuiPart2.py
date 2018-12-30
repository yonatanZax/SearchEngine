import shutil
import string
from tkinter import *
from tkinter import filedialog

from threading import Thread

import os

import nltk

from Main import MainClass
from Searching.Searcher import Searcher


from BasicMethods import get2DArrayFromFile, getTagFromText
from Gui.TkinterTable import TableView


class QuerySearcher(Frame):

    def __init__(self, master, mainManager, config,cityList,dataNoStem, dataWithStem):
        self.config = config
        self.mainManager = mainManager
        self.cityList = cityList
        self.dataNoStem = dataNoStem
        self.dataWithStem = dataWithStem
        self.docsForDominant = []

        self.resultsToWrite = ""


        Frame.__init__(self, master)
        self.grid()
        # self.filesDone = 0
        self.numOfFilesPerIteration = config.get__filesPerIteration()

        self.XstartPixel = 60
        self.YstartPixel = 10


        self.part1Button = Button(self.master, text='Part1', width=10, bg='blue', fg='white',command= self.switchPart1)
        self.part1Button.place(x = self.XstartPixel + 450, y = self.YstartPixel + 0)

        label_0 = Label(self.master, text="Search Engine", width=20, font=("bold", 30))
        label_0.place( x = self.XstartPixel + 20, y = self.YstartPixel + 30)





        label_query = Label(self.master, text="Query:", width=10, font=("bold", 10))
        label_query.place( x = self.XstartPixel + 50, y = self.YstartPixel + 105)
        self.entry_query_text = StringVar()
        self.entry_query_text.set("")
        self.entry_query = Entry(self.master, textvariable=self.entry_query_text, width=30)
        self.entry_query.place(x =self.XstartPixel + 180, y =self.YstartPixel + 105)


        label_queryFilePath = Label(self.master, text="Query file:", width=10, font=("bold", 10))
        label_queryFilePath.place( x = self.XstartPixel + 50,  y = self.YstartPixel + 135)
        self.entry_queryFilePath_text = StringVar()
        self.entry_queryFilePath_text.set("")
        self.entry_queryFilePath = Entry(self.master,textvariable=self.entry_queryFilePath_text,width=30)
        self.entry_queryFilePath.place( x = self.XstartPixel + 180, y = self.YstartPixel + 135)



        def queryPath():
            # print("Choose query file path...")
            query_path = filedialog.askopenfilename()
            self.entry_queryFilePath_text.set(query_path)


        self.queryFilePathButton = Button(self.master, text='Browse', width=7, fg='black',command= queryPath)
        self.queryFilePathButton.place( x = self.XstartPixel + 380, y = self.YstartPixel + 130)



        label_querySaveFilePath = Label(self.master, text="Save Query:", width=10, font=("bold", 10))
        label_querySaveFilePath.place( x = self.XstartPixel + 50,  y = self.YstartPixel + 165)
        self.entry_querySaveFilePath_text = StringVar()
        self.entry_querySaveFilePath_text.set("")
        self.entry_querySaveFilePath = Entry(self.master,textvariable=self.entry_querySaveFilePath_text,width=30)
        self.entry_querySaveFilePath.place( x = self.XstartPixel + 180, y = self.YstartPixel + 165)


        def querySavePath():
            # print("Choose query file path...")
            querySave_path = filedialog.askdirectory()
            self.entry_querySaveFilePath_text.set(querySave_path)


        self.querySavePathButton = Button(self.master, text='Browse', width=7, fg='black',command= querySavePath)
        self.querySavePathButton.place( x = self.XstartPixel + 380, y = self.YstartPixel + 160)



        label_4 = Label(self.master, text="City:", width=10, font=("bold", 10))
        label_4.place( x = self.XstartPixel + 50, y = self.YstartPixel + 190)


        self.sb = Scrollbar(orient="vertical")
        cityBox = Text(master, width=23, height=5, yscrollcommand=self.sb.set)
        cityBox.place(x = self.XstartPixel + 180, y = self.YstartPixel + 190)

        self.checkVar_CityList = []
        self.checkBoxList = []
        for city in sorted(self.cityList):
            var = BooleanVar()
            self.checkVar_CityList.append([var, city])
            box = Checkbutton(text=str(city), var=var, padx=0, pady=0, bd=0)
            self.checkBoxList.append(box)


        cityBox.insert("end", "**  Cities  **\n  ")

        for cb in self.checkBoxList:
            cityBox.window_create("end", window=cb)
            cityBox.insert("end", "\n  ")
            cb.bind("<Button-1>", self.selectstart)
            cb.bind("<Shift-Button-1>", self.selectrange)








        # list1 = ['NYC', 'TEL-AVIV', 'PARIS']
        # c = StringVar()
        # self.droplist = OptionMenu(self.master, c, *list1)
        # self.droplist.config(width=15)
        # c.set('Select')
        # self.droplist.place( x = self.XstartPixel + 180, y = self.YstartPixel + 220)



        label_stemming = Label(self.master, text="Stemming", width=10, font=("bold", 10))
        label_stemming.place( x = self.XstartPixel + 200, y = self.YstartPixel + 290)
        self.checkedStem = BooleanVar()
        self.stemmingCheckBox = Checkbutton(self.master, variable = self.checkedStem)
        self.stemmingCheckBox.place( x = self.XstartPixel + 180, y = self.YstartPixel + 290)


        label_Semantics = Label(self.master, text="Semantics", width=10, font=("bold", 10))
        label_Semantics.place( x = self.XstartPixel + 200, y = self.YstartPixel + 310)
        self.checkedSemantics = BooleanVar()
        self.semanticsCheckBox = Checkbutton(self.master, variable = self.checkedSemantics)
        self.semanticsCheckBox.place(x =self.XstartPixel + 180, y =self.YstartPixel + 310)


        self.runQueryButton = Button(self.master, text='Run query', width=15, bg='green', fg='white',command= self.runQueryListener)
        self.runQueryButton.place( x = self.XstartPixel + 100, y = self.YstartPixel + 350)

        self.runQueryFromFileButton = Button(self.master, text='Run query from file', width=15, bg='green', fg='white',command= self.runQueryFromFileListener)
        self.runQueryFromFileButton.place( x = self.XstartPixel + 260, y = self.YstartPixel + 350)

        self.findYishuyotButton = Button(self.master, text='חיפוש יישויות', width=15, bg='blue', fg='white',command= self.findYishuyot)
        self.findYishuyotButton.place( x = self.XstartPixel + 180, y = self.YstartPixel + 390)



        self.label_buildDetails = Label(self.master, text="",width=50 ,font=("bold",10))
        self.label_buildDetails.place( x = self.XstartPixel + 50, y = self.YstartPixel + 420)


        Label(self.master, text="Output:", width=10, font=("bold", 10)).place( x = self.XstartPixel + 20, y = self.YstartPixel + 420)


        from tkinter import scrolledtext
        self.txtbox = scrolledtext.ScrolledText( width = 45, height = 9)
        self.txtbox.place( x = self.XstartPixel + 60, y = self.YstartPixel + 450)


        self.saveTrec_EvalButton = Button(self.master, text='Save to TREC_EVAL', width=20, bg='blue', fg='white',command= self.saveTrec_Eval)
        self.saveTrec_EvalButton.place( x = self.XstartPixel + 160, y = self.YstartPixel + 610)

        self.statusLabel = Label(self.master, text="Status: Ready to Search\Shut down", width = 40, font = ("bold", 10))
        self.statusLabel.place( x = self.XstartPixel + 60, y = self.YstartPixel + 650)


        self.disableButtons()
        searcherThread = Thread(target=self.initSearcher)
        searcherThread.start()



    def initSearcher(self):
        self.searcher = Searcher(self.config, self.dataNoStem, self.dataWithStem)
        self.enableButtons()

    def switchPart1(self):
        import Gui.GuiMainView as Part1
        self.master.destroy()
        self.master = Tk()
        Part1.setWindowSizeAndPosition(self.master)
        self.master.title("SearchEngine")
        mainManager = MainClass(self.config)
        guiFrame = Part1.EngineBuilder(self.master, mainManager = mainManager, config = self.config, dataNoStem = self.dataNoStem, dataWithStem = self.dataWithStem)
        guiFrame.mainloop()




    # Cities CheckBox
    def selectstart(self, event):
        self.start = self.checkBoxList.index(event.widget)

    def selectrange(self, event):
        start = self.start
        end = self.checkBoxList.index(event.widget)
        sl = slice(min(start, end) + 1, max(start, end))
        for cb in self.checkBoxList[sl]:
            cb.toggle()
        self.start = end

    def getSelectedCities(self):
        selectedCities = []
        for var in self.checkVar_CityList:
            if var[0].get():
                selectedCities.append(var[1])

        return selectedCities





    def findYishuyot(self):
        from BasicMethods import getDicFromFile

        # Set stem in config
        self.config.setToStem(self.checkedStem.get())


        pathToDominantIndex = self.config.getSavedFilesPath() + '/docDominantIndex'

        if not os.path.exists(pathToDominantIndex):
            if self.checkedStem.get():
                self.statusLabel['text'] = 'Status (stem): dominant dic doesnt exists'
            else:
                self.statusLabel['text'] = 'Status (noStem): dominant dic doesnt exists'

            return

        docsFromQuery = self.docsForDominant
        dominantDic = dict()

        dominantDicFromFile = getDicFromFile(path=pathToDominantIndex)

        for qid_docNoArray in docsFromQuery:
            i = 0
            while i + 1 < len(qid_docNoArray):
                docNo = qid_docNoArray[i+1]
                i += 2

                dominantTerms = dominantDicFromFile[docNo][0]
                splitedTerms = dominantTerms.split(',')
                for score_term in splitedTerms:
                    if dominantDic.get(docNo) is None:
                        dominantDic[docNo] = [score_term.rstrip('\n')]
                    else:
                        dominantDic[docNo] += [score_term.rstrip('\n')]






        t = Thread(target=self.displayDominant, args=([dominantDic]))
        t.start()



    def displayDominant(self,dataArray):
        self.disableButtons()

        data = dataArray
        headLine = ['DocNo','Term_Score1','Term_Score2','Term_Score3','Term_Score4','Term_Score5']

        print('Display dominant table')

        self.statusLabel['text'] = 'Status: preparing a nice table to view dominant terms'

        self.displayClass = TableView(data, headLine)

        t = Thread(target=self.displayClass.run, args=())
        displayThread = Thread(target=self.listener, args=(t, self.enableButtons))
        t.start()
        displayThread.start()



    def runQueryListener(self):

        self.disableButtons()

        t = Thread(target=self.runQuery, args=())
        runQueryThread = Thread(target=self.listener, args=(t, self.enableButtons))
        t.start()
        runQueryThread.start()




    def runQueryFromFileListener(self):

        self.disableButtons()

        t = Thread(target=self.runQueryFromFile, args=())
        runQueryFromFileThread = Thread(target=self.listener, args=(t, self.enableButtons))
        t.start()
        runQueryFromFileThread.start()



    def runQuery(self):



        # Get the query
        path = self.entry_query_text.get()
        if path == '':
            self.statusLabel['text'] = "Status: Query line is empty"
            return

        semantics = self.checkedSemantics.get()
        useStem = self.checkedStem.get()

        if useStem and self.dataWithStem is None:
            self.statusLabel['text'] = "Status: Data with stem is None"
            return

        if not useStem and self.dataNoStem is None:
            self.statusLabel['text'] = "Status: Data without stem is None"
            return


        # Set stem in config
        self.config.setToStem(self.checkedStem.get())


        docList = self.searcher.getDocsForQueryWithExpansion(self.entry_query_text.get(),self.getSelectedCities(), semantics, useStem = useStem)
        resultsToPrint = "  qID  |         DocNo          |  Score   \n"


        windowSizes = [7,24,10]


        for file_score in docList:
            values = ['0', str(file_score[0]), str("{0:.3f}".format(round(file_score[1], 3)))]

            # Insert to dominant list




            for i in range(0,len(values)):
                dif = windowSizes[i] - len(values[i])
                before = int(dif/2)
                values[i] = ' '*before + values[i] + ' '*(dif-before)

            resultsToPrint += "%s|%s|%s\n" % (values[0],values[1],values[2])
            # resultsToPrint += "  %s  |  %s  |  %s  \n" % ('0', str(file_score[0]), str("{0:.3f}".format(round(file_score[1], 3))))

        # Write the results to the output window
        self.txtbox.delete('1.0',END)
        self.txtbox.insert('1.0',resultsToPrint)


    def runQueryFromFile(self):


        import os
        # Get the file's path
        path = self.entry_queryFilePath_text.get()
        if path == '':
            self.statusLabel['text'] = "Status: Please enter a valid path to query"
            return

        if not os.path.exists(path):
            self.statusLabel['text'] = "Status: Path %s , is not valid" % (path)
            return


        # Set stem in config
        self.config.setToStem(self.checkedStem.get())





        # # Best Values - 185
        # self.config.BM25_K = 1.6
        # self.config.BM25_B = 0.7
        #
        # # Best - 188
        # self.config.Axu_Value = 10
        #
        #







        #
        # # Write ManyFiles
        #
        # pathToSaveKB = 'C:/SaveKB'
        # changePathCounter = 0
        # pathToDic = pathToSaveKB + '/AxuDic.txt'
        # pathTrecEval = pathToSaveKB + '/trecAxu.txt'
        # if not os.path.exists(pathToSaveKB):
        #     os.mkdir(pathToSaveKB)

        #
        #
        # print("*** Started Axu run ***")
        # # StartValue
        # self.config.Axu_Value = 1.0
        #
        #
        #
        # while self.config.Axu_Value < 10.0:
        #     changePathCounter += 1
        #     lineToPrint = "num: " + str(changePathCounter) + ' values: ' + ' Axu ' + str(self.config.Axu_Value) +  '\n'
        #     print(lineToPrint)
        #
        #     trecFile = open(pathTrecEval, 'a')
        #     lineToWrite = "@echo %s" % (lineToPrint)
        #     lineToWrite += "treceval qrels.txt results_%s.txt\n" % (changePathCounter)
        #     trecFile.write(lineToWrite)
        #     trecFile.close()
        #
        #     dicFile = open(pathToDic, 'a')
        #     dicFile.write(lineToPrint)
        #     dicFile.close()
        #
        #     # Get result string from the file
        #     trec_eval_results_toWrite, trec_eval_results_toPrint = self.runMultipleQueries()
        #     self.resultsToWrite = trec_eval_results_toWrite
        #
        #     fileNamePath = pathToSaveKB + "/results_%s.txt" % (changePathCounter)
        #
        #     myFile = open(fileNamePath, 'w')
        #     myFile.write(trec_eval_results_toWrite)
        #     myFile.close()
        #
        #     self.config.Axu_Value += 0.5
        #
        #
        #
        #
        # print("*** Finished Axu run ***")
        #


        # print("*** Started KB run ***")


        # while self.config.BM25_K < 2.0:
        #
        #
        #     self.config.BM25_B = 0.6
        #     while self.config.BM25_B < 1.0:
        #
        #
        #         changePathCounter += 1
        #         lineToPrint = "num: " + str(changePathCounter) + ' values: ' + ' K ' + str(self.config.BM25_K) + ' B ' + str(
        #             self.config.BM25_B ) + '\n'
        #         print(lineToPrint)
        #
        #         trecFile = open(pathTrecEval, 'a')
        #         lineToWrite = "@echo %s" % (lineToPrint)
        #         lineToWrite += "treceval qrels.txt results_%s.txt\n" % (changePathCounter)
        #         trecFile.write(lineToWrite)
        #         trecFile.close()
        #
        #         dicFile = open( pathToDic, 'a')
        #         dicFile.write(
        #             "num: " + str(changePathCounter) + ' values: ' + ' K ' + str(self.config.BM25_K) + ' B ' + str(
        #                 self.config.BM25_B) + '\n')
        #         dicFile.close()
        #
        #
        #
        #         # Get result string from the file
        #         trec_eval_results_toWrite, trec_eval_results_toPrint = self.runMultipleQueries()
        #         self.resultsToWrite = trec_eval_results_toWrite
        #
        #         fileNamePath = pathToSaveKB + "/results_%s.txt" % (changePathCounter)
        #
        #         myFile = open(fileNamePath,'w')
        #         myFile.write(trec_eval_results_toWrite)
        #         myFile.close()
        #
        #         self.config.BM25_B += 0.1
        #
        #     self.config.BM25_K += 0.1
        #
        #
        # print("*** Finished KB run ***")






        # Get result string from the file
        trec_eval_results_toWrite, trec_eval_results_toPrint = self.runMultipleQueries()
        self.resultsToWrite = trec_eval_results_toWrite

        # Write the results to the output window
        self.txtbox.delete('1.0', END)
        self.txtbox.insert('1.0',trec_eval_results_toPrint)







    def runMultipleQueries(self, runID:str = '0'):
        queriesList_ID_query = self.readQueriesFiles()
        trec_eval_results_toWrite = ''
        trec_eval_results_toPrint = "  qID  |          DocNo         |  Score   \n"

        useStem = self.checkedStem.get()

        if useStem and self.dataWithStem is None:
            self.statusLabel['text'] = "Status: Data with stem is None"
            return '', ''

        if not useStem and self.dataNoStem is None:
            self.statusLabel['text'] = "Status: Data without stem is None"
            return '', ''


        # reset dominant doc
        self.docsForDominant = []

        for query_ID_query in queriesList_ID_query:

            docList = self.searcher.getDocsForQueryWithExpansion(query_ID_query[1],self.getSelectedCities(),self.checkedSemantics.get(), useStem = useStem)
            toWrite, toPrint, resultsForDominant = self.searcher.getResultFormatFromResultList(qID=query_ID_query[0], runID=runID, results=docList)
            trec_eval_results_toWrite += toWrite

            # Save query_doc to future display
            #  resultsForDominant = [str(qID),docNo]
            self.docsForDominant += [resultsForDominant]

            trec_eval_results_toPrint += toPrint

    #     TODO - write to a file we need to set in config

        return trec_eval_results_toWrite , trec_eval_results_toPrint




    def getNarrTermsFromQuery(self,queryStr)->list:
        from Parsing.NarrativeParsing import getNarrWithRegex

        queryNarr = getTagFromText(queryStr, "<narr> Narrative:", "</Narr>")


        stopWordsDic = {}

        try:
            import os
            path = self.config.stopWordPath
            with open(path) as f:
                for word in f.read().splitlines():
                    stopWordsDic[word] = True
                del stopWordsDic["may"]
        except IOError:
            print("Can't find stop word path:")



        stopPath = self.config.get__stopWordPath()
        stopFile = open(stopPath,'r')
        stopWordList = stopFile.readlines()

        stopFile.close()
        termsFromNarr = getNarrWithRegex(queryNarr,stopWords=stopWordsDic)

        return termsFromNarr

        #
        # print("\nNarr:\n")
        # print(termsFromNarr)



    def readQueriesFiles(self)-> list:



        queriesFilePath = self.entry_queryFilePath_text.get()
        queriesFile = open(queriesFilePath, 'r', )
        queriesFileArr = queriesFile.read().split('</top>')[:-1]
        queriesList_ID_query = []
        for queryStr in queriesFileArr:
            queryID = getTagFromText(queryStr,'<num> Number:')
            query = getTagFromText(queryStr,'<title>')

            # get narrative
            termFromNarrative = " ".join(self.getNarrTermsFromQuery(queryStr + "</Narr>"))
            query += " " +termFromNarrative

            queriesList_ID_query.append((queryID, query))
        return queriesList_ID_query






    def saveTrec_Eval(self):

        # Get the text is the output window
        textToWrite = self.resultsToWrite
        if  textToWrite == '':
            self.statusLabel['text'] = "Status: Nothing to save.."

        # Get the path to save file
        savePath = self.entry_querySaveFilePath_text.get()
        if savePath == '':
            self.statusLabel['text'] = "Status: path to save is empty"
            return

        if not os.path.exists(savePath):
            self.statusLabel['text'] = "Status: path %s is invalid" % (savePath)
            return

        # Check if file exists
        filePath = savePath + '/results.txt'
        if os.path.exists(filePath):
            os.remove(filePath)

        # Write the file
        try:
            myFile = open(filePath,'a')
            myFile.write(textToWrite)
            myFile.close()

        except Exception as ex:
            print(ex)



    @ staticmethod
    def listener(thread,action):
        thread.join()
        action()




    def enableButtons(self):
        self.runQueryButton.configure(state = NORMAL)
        self.runQueryFromFileButton.configure(state = NORMAL)
        self.findYishuyotButton.configure(state = NORMAL)
        self.saveTrec_EvalButton.configure(state = NORMAL)

        self.statusLabel['text'] = 'Status: Ready to Search\Shut down'

    def disableButtons(self):
        self.runQueryButton.configure(state = DISABLED)
        self.runQueryFromFileButton.configure(state = DISABLED)
        self.findYishuyotButton.configure(state = DISABLED)
        self.saveTrec_EvalButton.configure(state = DISABLED)








