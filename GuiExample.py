from tkinter import *
from tkinter import filedialog

import Configuration as config


class EngineBuilder(Frame):

    def __init__(self,master,numOfManagers, numOfTotalFiles):
        Frame.__init__(self, master)
        self.grid()
        self.filesDone = 0
        self.numOfTotalFiles = numOfTotalFiles
        self.numOfFilesPerIteration = config.filesPerIteration
        self.managersList = []
        for i in range(0,numOfManagers):
            self.managersList.append(0)

        label_0 = Label(self.master, text="Search Engine", width=20, font=("bold", 20))
        label_0.place(x=90, y=60)



        label_corpusPath = Label(self.master, text="Corpus path:", width=10, font=("bold", 10))
        label_corpusPath.place(x=50, y=130)
        self.entry_corpusPath_text = StringVar()
        self.entry_corpusPath_text.set(config.corpusPath)
        self.entry_corpusPath = Entry(self.master,textvariable=self.entry_corpusPath_text,width=30)
        self.entry_corpusPath.place(x=180, y=130)


        label_postingPath = Label(self.master, text="Posting path:", width=10, font=("bold", 10))
        label_postingPath.place(x=50, y=160)
        self.entry_postingPath_text = StringVar()
        self.entry_postingPath_text.set(config.savedFilePath)
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



        self.corpusPathButton = Button(self.master, text='Find', width=5, fg='black',command= corpusPath).place(x=380, y=125)
        self.postingPathButton = Button(self.master, text='Find', width=5, fg='black',command= postingPath).place(x=380, y=155)









        label_4 = Label(self.master, text="Language", width=10, font=("bold", 10))
        label_4.place(x=50, y=190)

        # list1 = ['English', 'Spanish', 'Hebrew'];
        # c = StringVar()
        # droplist = OptionMenu(root, c, *list1)
        # droplist.config(width=15)
        # c.set('Select')
        # droplist.place(x=180, y=190)




        def deleteEngine():
            print("Deleting...")


        def buildEngine():
            print("Corpus path:     ",self.entry_corpusPath.get())
            config.corpusPath = self.entry_corpusPath.get()
            print("Posting path:     ",self.entry_postingPath.get())
            config.savedFilePath = self.entry_postingPath.get()


            # Todo - disable button


            print("\n***    ManagerRun    ***")
            from Main import managerRun
            from threading import Thread
            th = Thread(target=managerRun)
            th.start()
            print('Start')
            # managerRun()


        self.deleteButton = Button(self.master, text='Delete', width=10, bg='red', fg='white',command= deleteEngine).place(x=100, y=250)
        self.buildButton = Button(self.master, text='Build', width=10, bg='green', fg='white',command= buildEngine).place(x=200, y=250)

        label_stemming = Label(self.master, text="Stemming", width=10, font=("bold", 10))
        label_stemming.place(x=320, y=250)
        var1 = IntVar()
        self.stemmingCheckBox = Checkbutton(self.master, variable=var1,onvalue = 1, offvalue = 0).place(x=300, y=250)


        self.label_progress = Label(self.master, text="Progress:     [||||||||||||||||||||||||||||||||||||||||          ] 80% ", width=50, font=("bold", 10))
        self.label_progress.place(x=50, y=320)





        label_postingPath = Label(self.master, text="Dictionary:", width=20, font=("bold", 10))
        label_postingPath.place(x=30, y=380)


        def uploadDictionary():
            print("Uploading dictionary...")


        def showDictionary():
            print("Show dictionary...")


        self.uploadDicButton = Button(self.master, text='Upload', width=10, bg='blue', fg='white',command= uploadDictionary).place(x=170, y=380)
        self.showDicButton = Button(self.master, text='Show', width=10, bg='blue', fg='white',command= showDictionary).place(x=270, y=380)






        #
        # def buttonClick():
        #     print("query:   " + self.entry_1.get())
        #
        #
        # self.submitButton = Button(self.master, text='Search', width=10, bg='blue', fg='white',command= buttonClick).place(x=280, y=225)
        # self.submitButton.grid()

        # label_docText = Label(self.master,
        #                 text="Text:    ............\n  ......\n    .......\n   ................\n  .....\n     .......\n   ........",
        #                 width=20, font=("bold", 10))
        # label_docText.place(x=70, y=300)

    def updateFileCounter(self, managerID):
        label = "Progress:     ["

        self.managersList[managerID] += self.numOfFilesPerIteration
        filesDone = 0
        for i in range(0,len(self.managersList)):
            filesDone += self.managersList[i]
        numOfLines = int(self.filesDone/self.numOfTotalFiles) * 50
        linesAsString = ''
        for i in range(0,numOfLines):
            linesAsString += '|'
        for i in range(numOfLines,50):
            linesAsString += ' '

        self.label_progress['label'] = label + linesAsString + '] ' + str(numOfLines*2) + '% '



if __name__ == "__main__":



    root = Tk()
    root.geometry('500x550')
    root.title("SearchEngine")



    guiFrame = EngineBuilder(root)
    guiFrame.mainloop()























