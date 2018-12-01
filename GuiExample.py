from tkinter import *
from tkinter import filedialog

from Configuration import ConfigClass
from threading import Thread

class EngineBuilder(Frame):

    def __init__(self, master, mainManager, config, numOfTotalFiles):
        self.config = config
        self.mainManager = mainManager
        Frame.__init__(self, master)
        self.grid()
        # self.filesDone = 0
        # self.numOfTotalFiles = numOfTotalFiles
        self.numOfFilesPerIteration = config.get__filesPerIteration()

        from GuiDisplayDF import DisplayDataFrame

        self.displayClass = DisplayDataFrame()
        # self.displayClass.runAndCloseFast()






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








        label_4 = Label(self.master, text="Language", width=10, font=("bold", 10))
        label_4.place(x=50, y=190)

        # TODO - make drop list work

        list1 = ['English', 'Spanish', 'Hebrew'];
        c = StringVar()
        droplist = OptionMenu(self.master, c, *list1)
        droplist.config(width=15)
        c.set('Select')
        droplist.place(x=180, y=190)




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


        def uploadDictionary():
            print("Uploading dictionary...")


        def showDictionary():
            print("Show dictionary...")


        self.uploadDicButton = Button(self.master, text='Upload', width=10, bg='blue', fg='white',command= uploadDictionary)
        self.uploadDicButton.place(x=170, y=380)
        self.showDicButton = Button(self.master, text='Show', width=10, bg='blue', fg='white',command= self.displayDicionary)
        self.showDicButton.place(x=270, y=380)

        # from tkinter import scrolledtext
        # self.txtbox = scrolledtext.ScrolledText(width= 200)
        #
        # self.txtbox.place(x= 100, y = 420)
        # # self.txtbox.





    def updateFileCounter(self):
        flag = True
        label = "Progress:     ["
        import os
        import time

        while flag:
            time.sleep(60)
            path = self.config.get__savedFilePath() + '\\a'
            if not os.path.exists(path):
                continue
            listOfFiles = os.listdir(path)
            filesPerIteration = self.config.get__filesPerIteration()
            allFilesCount = self.config.get__listOfFoldersLength()
            totalFileCount = len(listOfFiles) * filesPerIteration

            percent = (totalFileCount/allFilesCount)*50
            linesAsString = ''
            for i in range(0,percent):
                linesAsString += '|'
            for i in range(percent,50):
                linesAsString += ' '

            self.label_progress['label'] = label + linesAsString + '] ' + str(percent*2) + '% '






    def displayDicionary(self):


        t = Thread(target=self.displayClass.run)

        t.start()


    def deleteEngine(self):
        import shutil
        shutil.rmtree(self.config.get__savedFileMainFolder())
        print("Folder was deleted successfully..")
        self.buildButton.configure(state=NORMAL)
        self.deleteButton.configure(state=DISABLED)



    def buildEngine(self):
        print("Corpus path:     ", self.entry_corpusPath.get())
        corpusPath = str(self.entry_corpusPath.get())
        self.config.setCorpusPath(corpusPath)
        # self.disableBuildBtn()

        check = self.checked.get()
        self.config.setToStem(check)

        saveMainFolderPath = str(self.entry_postingPath.get())
        self.config.setSaveMainFolderPath(saveMainFolderPath)

        print("Posting path:     ", saveMainFolderPath)


        self.buildButton.configure(state=DISABLED)
        self.deleteButton.configure(state=NORMAL)

        print("\n***    ManagerRun    ***\n")

        from threading import Thread
        th = Thread(target=self.mainManager.managerRun)
        # threadProgress = Thread(target=updateFileCounter)
        th.start()
        # threadProgress.start()



# if __name__ == "__main__":
#
#
#
#     root = Tk()
#     root.geometry('500x550')
#     root.title("SearchEngine")
#
#
#
#     guiFrame = EngineBuilder(root)
#     guiFrame.mainloop()























