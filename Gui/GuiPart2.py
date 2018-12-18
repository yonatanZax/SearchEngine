import shutil
import string
from tkinter import *
from tkinter import filedialog

from threading import Thread

import os
from Searching.Searcher import Searcher


from BasicMethods import get2DArrayFromFile, getTagFromText
from Gui.TkinterTable import TableView


class QuerySearcher(Frame):

    def __init__(self, master, mainManager, config,data):
        self.config = config
        self.mainManager = mainManager
        self.data = data
        self.searcher = Searcher(config,self.data)


        Frame.__init__(self, master)
        self.grid()
        # self.filesDone = 0
        self.numOfFilesPerIteration = config.get__filesPerIteration()

        self.XstartPixel = 60
        self.YstartPixel = 10


        label_0 = Label(self.master, text="Search Engine", width=20, font=("bold", 30))
        label_0.place( x = self.XstartPixel + 20, y = self.YstartPixel + 40)

        self.part1Button = Button(self.master, text='Part1', width=10, bg='blue', fg='white',command= self.switchPart1)
        self.part1Button.place(x = self.XstartPixel + 450, y = self.YstartPixel + 0)



        label_query = Label(self.master, text="Query:", width=10, font=("bold", 10))
        label_query.place( x = self.XstartPixel + 50, y = self.YstartPixel + 130)
        self.entry_query_text = StringVar()
        self.entry_query_text.set("")
        self.entry_query = Entry(self.master, textvariable=self.entry_query_text, width=30)
        self.entry_query.place(x =self.XstartPixel + 180, y =self.YstartPixel + 130)


        label_queryFilePath = Label(self.master, text="Query file:", width=10, font=("bold", 10))
        label_queryFilePath.place( x = self.XstartPixel + 50,  y = self.YstartPixel + 160)
        self.entry_queryFilePath_text = StringVar()
        self.entry_queryFilePath_text.set("")
        self.entry_queryFilePath = Entry(self.master,textvariable=self.entry_queryFilePath_text,width=30)
        self.entry_queryFilePath.place( x = self.XstartPixel + 180, y = self.YstartPixel + 160)



        def queryPath():
            print("Choose query file path...")
            query_path = filedialog.askopenfilename()
            self.entry_queryFilePath_text.set(query_path)


        self.queryFilePathButton = Button(self.master, text='Browse', width=7, fg='black',command= queryPath)
        self.queryFilePathButton.place( x = self.XstartPixel + 380, y = self.YstartPixel + 155)



        label_4 = Label(self.master, text="City:", width=10, font=("bold", 10))
        label_4.place( x = self.XstartPixel + 50, y = self.YstartPixel + 190)


        list1 = ['NYC', 'TEL-AVIV', 'PARIS']
        c = StringVar()
        self.droplist = OptionMenu(self.master, c, *list1)
        self.droplist.config(width=15)
        c.set('Select')
        self.droplist.place( x = self.XstartPixel + 180, y = self.YstartPixel + 190)



        label_stemming = Label(self.master, text="Stemming", width=10, font=("bold", 10))
        label_stemming.place( x = self.XstartPixel + 200, y = self.YstartPixel + 250)
        self.checked = BooleanVar()
        self.stemmingCheckBox = Checkbutton(self.master, variable = self.checked)
        self.stemmingCheckBox.place( x = self.XstartPixel + 180, y = self.YstartPixel + 250)


        label_Semantics = Label(self.master, text="Semantics", width=10, font=("bold", 10))
        label_Semantics.place( x = self.XstartPixel + 200, y = self.YstartPixel + 280)
        self.checked = BooleanVar()
        self.SemanticsCheckBox = Checkbutton(self.master, variable = self.checked)
        self.SemanticsCheckBox.place( x = self.XstartPixel + 180, y = self.YstartPixel + 280)


        self.runQueryButton = Button(self.master, text='Run query', width=15, bg='green', fg='white',command= self.runQuery)
        self.runQueryButton.place( x = self.XstartPixel + 180, y = self.YstartPixel + 340)

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




    def switchPart1(self):
        import Gui.GuiMainView as Part1
        self.master.destroy()
        self.master = Tk()
        Part1.setWindowSizeAndPosition(self.master)
        self.master.title("SearchEngine")
        guiFrame = Part1.EngineBuilder(self.master, mainManager=self, config=self.config)
        guiFrame.mainloop()


    def findYishuyot(self):
        pass


    def runQuery(self):
        docList = self.searcher.getDocsForQuery(self.entry_query_text.get())
        docListText = ""
        for file_score in docList:
            docListText += '\t' + str(file_score[0]) + ' : ' + str("{0:.2f}".format(round(file_score[1],2))) + '\n'

        self.txtbox.delete('1.0',END)
        self.txtbox.insert('1.0',docListText)


    def writeResultsForTREC(self, results, qID:str = '0', runID:str = '0'):
        resultStr = self.searcher.getResultFormatFromResultList(qID=qID, runID=runID, results=results)


    def runMultipleQueries(self, runID:str = '0'):
        queriesList_ID_query = self.readQueriesFiles()
        trec_eval_results_str = ''
        for query_ID_query in queriesList_ID_query:
            docList = self.searcher.getDocsForQuery(query_ID_query[1])
            trec_eval_results_str += self.searcher.getResultFormatFromResultList(qID=queriesList_ID_query[0], runID=runID, results=docList)

    #     TODO - write to a file we need to set in config
        print(trec_eval_results_str)


    def readQueriesFiles(self)-> list:
        queriesFilePath = self.entry_queryFilePath_text.get()
        queriesFile = open(queriesFilePath, 'r', )
        queriesFileArr = queriesFile.read().split('</top>')[:-1]
        queriesList_ID_query = []
        for queryStr in queriesFileArr:
            queryID = getTagFromText(queryStr,'<num> Number:')
            query = getTagFromText(queryStr,'<title>')
            queriesList_ID_query.append((queryID, query))
        return queriesList_ID_query


    def saveTrec_Eval(self):
        pass



    @ staticmethod
    def listener(thread,action):
        thread.join()
        action()




    def enableButtons(self):
        self.runQueryButton.configure(state = NORMAL)
        self.findYishuyotButton.configure(state = NORMAL)
        self.saveTrec_EvalButton.configure(state = NORMAL)

        self.statusLabel['text'] = 'Status: Ready to Search\Shut down'

    def disableButtons(self):
        self.runQueryButton.configure(state = DISABLED)
        self.findYishuyotButton.configure(state = DISABLED)
        self.saveTrec_EvalButton.configure(state = DISABLED)








