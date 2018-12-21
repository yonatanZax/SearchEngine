import shutil
import string
from tkinter import *
from tkinter import filedialog

from threading import Thread

import os

from Main import MainClass
from Searching.Searcher import Searcher


from BasicMethods import get2DArrayFromFile, getTagFromText
from Gui.TkinterTable import TableView


class QuerySearcher(Frame):

    def __init__(self, master, mainManager, config,cityList,data):
        self.config = config
        self.mainManager = mainManager
        self.cityList = cityList
        self.data = data
        self.dataNoStem = None
        self.dataWithStem = None

        self.resultsToWrite = ""


        Frame.__init__(self, master)
        self.grid()
        # self.filesDone = 0
        self.numOfFilesPerIteration = config.get__filesPerIteration()

        self.XstartPixel = 60
        self.YstartPixel = 10

        menubar = Menu(master)
        show_all = BooleanVar()
        show_all.set(True)
        self.citySelection = []
        view_menu = Menu(menubar)
        # view_menu = Menu(menubar,tearoff=0)

        for city in self.cityList:
            show_done = BooleanVar()
            self.citySelection.append([show_done,city])
            view_menu.add_checkbutton(label=str(city) , onvalue=True, offvalue=0, variable=show_done)

        menubar.add_cascade(label='Filter cities', menu=view_menu)
        master.config(menu=menubar)

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



        # label_stemming = Label(self.master, text="Stemming", width=10, font=("bold", 10))
        # label_stemming.place( x = self.XstartPixel + 200, y = self.YstartPixel + 260)
        # self.checkedStem = BooleanVar()
        # self.stemmingCheckBox = Checkbutton(self.master, variable = self.checkedStem)
        # self.stemmingCheckBox.place( x = self.XstartPixel + 180, y = self.YstartPixel + 260)


        label_Semantics = Label(self.master, text="Semantics", width=10, font=("bold", 10))
        label_Semantics.place( x = self.XstartPixel + 200, y = self.YstartPixel + 290)
        self.checkedSemantics = BooleanVar()
        self.semanticsCheckBox = Checkbutton(self.master, variable = self.checkedSemantics)
        self.semanticsCheckBox.place(x =self.XstartPixel + 180, y =self.YstartPixel + 290)


        self.runQueryButton = Button(self.master, text='Run query', width=15, bg='green', fg='white',command= self.runQuery)
        self.runQueryButton.place( x = self.XstartPixel + 100, y = self.YstartPixel + 340)

        self.runQueryFromFileButton = Button(self.master, text='Run query from file', width=15, bg='green', fg='white',command= self.runQueryFromFile)
        self.runQueryFromFileButton.place( x = self.XstartPixel + 260, y = self.YstartPixel + 340)

        self.findYishuyotButton = Button(self.master, text='חיפוש יישויות', width=15, bg='blue', fg='white',command= self.findYishuyot)
        self.findYishuyotButton.place( x = self.XstartPixel + 180, y = self.YstartPixel + 380)



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
        self.searcher = Searcher(self.config, self.data)
        self.enableButtons()

    def switchPart1(self):
        import Gui.GuiMainView as Part1
        self.master.destroy()
        self.master = Tk()
        Part1.setWindowSizeAndPosition(self.master)
        self.master.title("SearchEngine")
        mainManager = MainClass(self.config)
        guiFrame = Part1.EngineBuilder(self.master, mainManager=mainManager, config=self.config)
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





    def findYishuyot(self):
        # for selected in self.citySelection:
        #     if selected[0].get() == 1:
        #         print(selected[1])


        from Gui.checkbox1 import App
        root2 = Tk()
        app = App(root2,self.cityList)
        root2.mainloop()
        pass


    def runQuery(self):
        # Get the query
        path = self.entry_query_text.get()
        if path == '':
            self.statusLabel['text'] = "Status: Query line is empty"

        docList = self.searcher.getDocsForQuery(self.entry_query_text.get())
        resultsToPrint = ""
        for file_score in docList:
            resultsToPrint += "  %s  |  %s  |  %s  \n" % ('0', str(file_score[0]), str("{0:.3f}".format(round(file_score[1], 3))))

        self.txtbox.delete('1.0',END)
        self.txtbox.insert('1.0',resultsToPrint)


    def runQueryFromFile(self):
        import os
        # Get the file's path
        path = self.entry_queryFilePath_text.get()
        if path == '':
            self.statusLabel['text'] = "Status: Please enter a valid path to query"

        if not os.path.exists(path):
            self.statusLabel['text'] = "Status: Path %s , is not valid" % (path)

        # Get result string from the file
        trec_eval_results_toWrite, trec_eval_results_toPrint = self.runMultipleQueries()
        self.resultsToWrite = trec_eval_results_toWrite

        # Write the results to the output window
        self.txtbox.insert('1.0',trec_eval_results_toPrint)




    def writeResultsForTREC(self, results, qID:str = '0', runID:str = '0'):
        resultStr = self.searcher.getResultFormatFromResultList(qID=qID, runID=runID, results=results)


    def runMultipleQueries(self, runID:str = '0'):
        queriesList_ID_query = self.readQueriesFiles()
        trec_eval_results_toWrite = ''
        trec_eval_results_toPrint = ''
        for query_ID_query in queriesList_ID_query:
            if self.checkedSemantics.get():
                docList = self.searcher.getDocsForQueryWithExpansion(query_ID_query[1])
            else:
                docList = self.searcher.getDocsForQuery(query_ID_query[1])
            toWrite, toPrint = self.searcher.getResultFormatFromResultList(qID=query_ID_query[0], runID=runID, results=docList)
            trec_eval_results_toWrite += toWrite
            trec_eval_results_toPrint += toPrint

    #     TODO - write to a file we need to set in config
        return trec_eval_results_toWrite , trec_eval_results_toPrint
        # print(trec_eval_results_str)


    def readQueriesFiles(self)-> list:
        queriesFilePath = self.entry_queryFilePath_text.get()
        queriesFile = open(queriesFilePath, 'r', )
        queriesFileArr = queriesFile.read().split('</top>')[:-1]
        queriesList_ID_query = []
        for queryStr in queriesFileArr:
            queryID = getTagFromText(queryStr,'<num> Number:')
            query = getTagFromText(queryStr,'<title>')
            # query += ' ' + getTagFromText(queryStr,'<desc>','<narr>')
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

        if not os.path.exists(savePath):
            self.statusLabel['text'] = "Status: path %s is invalid" % (savePath)

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








