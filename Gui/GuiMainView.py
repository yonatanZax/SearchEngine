import string
from tkinter import *
from tkinter import filedialog

from threading import Thread

import os

from BasicMethods import get2DArrayFromFile
from Gui.TkinterTable import TableView


class EngineBuilder(Frame):

    def __init__(self, master, mainManager, config, numOfTotalFiles):
        self.config = config
        self.mainManager = mainManager
        Frame.__init__(self, master)
        self.grid()
        # self.filesDone = 0
        self.numOfTotalFiles = numOfTotalFiles
        self.numOfFilesPerIteration = config.get__filesPerIteration()


        label_0 = Label(self.master, text="Search Engine", width=20, font=("bold", 20))
        label_0.place(x=90, y=60)



        label_corpusPath = Label(self.master, text="Corpus path:", width=10, font=("bold", 10))
        label_corpusPath.place(x=50, y=130)
        self.entry_corpusPath_text = StringVar()
        self.entry_corpusPath_text.set(config.get__corpusPath())
        self.entry_corpusPath = Entry(self.master,textvariable=self.entry_corpusPath_text,width=30)
        self.entry_corpusPath.place(x=180, y=130)


        label_postingPath = Label(self.master, text="Posting path:", width=10, font=("bold", 10))
        label_postingPath.place(x=50, y=160)
        self.entry_postingPath_text = StringVar()
        self.entry_postingPath_text.set(config.get__savedFileMainFolder())
        self.entry_postingPath = Entry(self.master,textvariable=self.entry_postingPath_text,width=30)
        self.entry_postingPath.place(x=180, y=160)


        def corpusPath():
            print("Choose corpus path...")
            corpus_path = filedialog.askdirectory()
            self.entry_corpusPath_text.set(corpus_path)

            print(corpus_path)

        def postingPath():
            print("Choose posting path...")
            posting_path = filedialog.askdirectory()
            self.entry_postingPath_text.set(posting_path)



        self.corpusPathButton = Button(self.master, text='Find', width=5, fg='black',command= corpusPath)
        self.corpusPathButton.place(x=380, y=125)
        self.postingPathButton = Button(self.master, text='Find', width=5, fg='black',command= postingPath)
        self.postingPathButton.place(x=380, y=155)



        self.data = None
        self.headline = None




        label_4 = Label(self.master, text="Language", width=10, font=("bold", 10))
        label_4.place(x=50, y=190)


        list1 = ['English', 'Spanish', 'Hebrew']
        c = StringVar()
        self.droplist = OptionMenu(self.master, c, *list1)
        self.droplist.config(width=15)
        c.set('Select')
        self.droplist.place(x=180, y=190)




        self.deleteButton = Button(self.master, text='Delete', width=10, bg='red', fg='white',command= self.deleteEngine)
        self.deleteButton.place(x=100, y=250)
        self.buildButton = Button(self.master, text='Build', width=10, bg='green', fg='white',command= self.buildEngine)
        self.buildButton.place(x=200, y=250)


        label_stemming = Label(self.master, text="Stemming", width=10, font=("bold", 10))
        label_stemming.place(x=320, y=250)
        self.checked = BooleanVar()
        self.stemmingCheckBox = Checkbutton(self.master, variable = self.checked)
        self.stemmingCheckBox.place(x=300, y=250)


        self.label_progress = Label(self.master, text="Progress:     [||||||||||||||||||||||||||||||||||||||||          ] 80% ", width=50, font=("bold", 10))
        self.label_progress.place(x=50, y=320)



        label_postingPath = Label(self.master, text="Dictionary:", width=20, font=("bold", 10))
        label_postingPath.place(x=30, y=380)



        self.uploadDicButton = Button(self.master, text='Upload', width=10, bg='blue', fg='white',command= self.loadDictionary)
        self.uploadDicButton.place(x=170, y=380)
        self.showDicButton = Button(self.master, text='Show', width=10, bg='blue', fg='white',command= self.displayDicionary)
        self.showDicButton.place(x=270, y=380)

        self.label_buildDetails = Label(self.master, text="",width=50 ,font=("bold",10))
        self.label_buildDetails.place(x=50,y=420)


        Label(self.master, text="Summary:", width=10, font=("bold", 10)).place(x=20, y=420)


        from tkinter import scrolledtext
        self.txtbox = scrolledtext.ScrolledText(width= 45,height=7)
        self.txtbox.place(x= 60, y = 440)

        self.statusLabel = Label(self.master, text="Status: Ready to Build\Shut down", width=40, font=("bold", 10))
        self.statusLabel.place(x=60, y=570)








    def updatePostingProgress(self):
        flag = True
        label = "Progress:     ["
        import os
        import time
        counter = 0

        while flag:
            time.sleep(10)
            path = self.config.get__savedFilePath() + '/Progress/Posting'
            if not os.path.exists(path):
                break
            listOfFiles = os.listdir(path)
            if len(listOfFiles) == 0:
                continue
            for file in listOfFiles:
                splitedFile = file.split('_')
                counter += int(splitedFile[-1])

            if counter == self.numOfTotalFiles:
                return
            percent = (counter/self.numOfTotalFiles)*50
            percent = int(percent)
            linesAsString = ''
            for i in range(0,percent):
                linesAsString += '|'
            for i in range(percent,50):
                linesAsString += ' '

            self.label_progress['text'] = label + linesAsString + '] ' + str(percent*2) + '% '




    def load(self):


        savedFolderPath = self.config.get__savedFilePath()
        lettersList = list(string.ascii_lowercase)
        lettersList.append('#')

        totalList = []
        for letter in lettersList:
            path = savedFolderPath + '/' + letter + '/' + 'mergedFile_dic'
            if not os.path.exists(path):
                self.enableButtons()
                self.statusLabel['text'] = 'Need to build (Check if stem is clicked)'
                print('Location not found', path)
                return
            totalList = totalList + get2DArrayFromFile(path)

        self.headline = ['Term', 'df', 'sumTF', '# Posting']
        self.data = totalList


    def loadDictionary(self):


        if self.entry_postingPath.get() == '':
            self.statusLabel['text'] = 'Status: Enter a path to posting'
            return

        if not os.path.exists(self.entry_postingPath.get()):
            self.statusLabel['text'] = 'Status: Enter a valid path to posting'
            return

        self.config.setSaveMainFolderPath(self.entry_postingPath.get() + '/SavedFiles')

        check = self.checked.get()
        self.config.setToStem(check)

        if not os.path.exists(self.config.savedFilePath + '/a'):
            self.statusLabel['text'] = 'Status: Please build before trying to load'
            return




        self.disableButtons()
        print('Load dictionary')

        t = Thread(target=self.load, args=())
        displayThread = Thread(target=self.listener, args=(t, self.enableButtons))
        t.start()
        displayThread.start()




    def displayDicionary(self):

        self.disableButtons()
        print('Display dictionary')

        if self.data is None or self.headline is None:
            self.enableButtons()
            return


        self.displayClass = TableView(self.data, self.headline)




        t = Thread(target=self.displayClass.run,args=())
        displayThread = Thread(target=self.listener,args =(t,self.enableButtons))
        t.start()
        displayThread.start()


    def deleteEngine(self):
        import shutil
        shutil.rmtree(self.config.get__savedFileMainFolder())
        print("Folder was deleted successfully..")
        self.buildButton.configure(state=NORMAL)
        self.deleteButton.configure(state=DISABLED)
        self.showDicButton.configure(state = DISABLED)
        self.uploadDicButton.configure(state = DISABLED)



    def buildEngine(self):

        if self.entry_postingPath.get() == '' or self.entry_corpusPath.get() == '':
            self.statusLabel['text'] = 'Status: Enter a path to corpus and posting fields'
            return

        print("Corpus path:     ", self.entry_corpusPath.get())
        corpusPath = str(self.entry_corpusPath.get())
        if not os.path.exists(corpusPath):
            self.statusLabel['text'] = 'Status: Corpus path not exists'
            return
        if not os.path.exists(corpusPath + '/stop_words.txt'):
            self.statusLabel['text'] = 'Status: stop_words.txt doesnt exists in corpus path'
            return


        self.config.setCorpusPath(corpusPath)

        check = self.checked.get()
        self.config.setToStem(check)

        saveMainFolderPath = str(self.entry_postingPath.get())
        if not os.path.exists(saveMainFolderPath):
            self.statusLabel['text'] = 'Status: %s path not exists' % (saveMainFolderPath,)
            return

        self.config.setSaveMainFolderPath(saveMainFolderPath + '/SavedFiles',True)

        print("Posting path:     ", saveMainFolderPath)


        self.disableButtons()

        print("\n***    ManagerRun    ***\n")

        self.statusLabel['text'] = 'Building.. might take a while'

        from threading import Thread
        from concurrent.futures import ThreadPoolExecutor

        executor = ThreadPoolExecutor()
        future = executor.submit(self.mainManager.managerRun)


        threadWaitUntilBuildDone = Thread(target=self.buildListener, args=(future,))
        threadWaitUntilBuildDone.start()


        # threadProgress = Thread(target=updateFileCounter)
        # threadProgress.start()


    @ staticmethod
    def listener(thread,action):
        # print('Gui - waiting to join')
        thread.join()
        action()



    def buildListener(self,future):
        timeItTook, maxParsingTime, totalMerging, totalNumberOfTerms, totalNumberOfDocuments ,mergedLanguagesSet = future.result()
        print("Number of Terms: " , str(totalNumberOfTerms))
        print("Number of Docs: " , str(totalNumberOfDocuments))
        print("Parsing Time: " , str(maxParsingTime))
        print("Merging Time: " , str(totalMerging))
        print("Everything took: " , str(timeItTook) , " seconds")
        self.enableButtons()

        self.droplist.destroy()
        c = StringVar()
        self.droplist = OptionMenu(self.master, c, *mergedLanguagesSet)
        self.droplist.config(width=15)
        c.set('Select')
        self.droplist.place(x=180, y=190)
        self.setBuildDetails(timeItTook, maxParsingTime, totalMerging, totalNumberOfTerms, totalNumberOfDocuments)





    def setBuildDetails(self, timeItTook, maxParsingTime, totalMerging, totalNumberOfTerms, totalNumberOfDocuments):
        stem = ''
        if self.config.toStem:
            stem = '\n** Run with stemming - Details **\n'
        else:
            stem = '\n** Run without stemming - Details **\n'
        detailString = stem
        detailString += "\tNumber of Terms:  " + str(totalNumberOfTerms) + "\n"
        detailString += "\tNumber of Docs:   " + str(totalNumberOfDocuments) + "\n"
        detailString += "\tParsing Time:     " + str(maxParsingTime) + "\n"
        detailString += "\tMerging Time:     " + str(totalMerging) + "\n"
        detailString += "\tEverything took:  " + str(timeItTook) + " seconds\n"
        self.txtbox.insert('end',detailString)
        # self.label_buildDetails['text'] = detailString



    def enableButtons(self):
        self.buildButton.configure(state = NORMAL)
        self.deleteButton.configure(state = NORMAL)
        self.showDicButton.configure(state = NORMAL)
        self.uploadDicButton.configure(state = NORMAL)

        self.statusLabel['text'] = 'Status: Ready to Build\Shut down'

    def disableButtons(self):
        self.buildButton.configure(state = DISABLED)
        self.deleteButton.configure(state = DISABLED)
        self.showDicButton.configure(state = DISABLED)
        self.uploadDicButton.configure(state = DISABLED)























