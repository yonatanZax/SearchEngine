
from tkinter import *
from tkinter import messagebox
import os

class GUI:

    def __init__(self,mainManager,config,numOfTotalFiles):
        # self.language_list = languages_list
        # TODO: add list to drop_down_menu
        self.root = Tk()
        self.root.title('IR2018')
        self.root.geometry('500x600')
        self.master = Frame(self.root)
        self.mainManager = mainManager




        # *** Labels ***
        label_0 = Label(self.master, text="Search Engine", width=20, font=("bold", 20))
        label_0.place(x=90, y=60)
        label_corpusPath = Label(self.master, text="Corpus path:", width=10, font=("bold", 10))
        label_corpusPath.place(x=50, y=130)
        label_postingPath = Label(self.master, text="Posting path:", width=10, font=("bold", 10))
        label_postingPath.place(x=50, y=160)
        label_4 = Label(self.master, text="Language", width=10, font=("bold", 10))
        label_4.place(x=50, y=190)
        label_stemming = Label(self.master, text="Stemming", width=10, font=("bold", 10))
        label_stemming.place(x=320, y=250)
        self.label_progress = Label(self.master,
                                    text="Progress:     [||||||||||||||||||||||||||||||||||||||||          ] 80% ",
                                    width=50, font=("bold", 10))
        self.label_progress.place(x=50, y=320)
        label_postingPath = Label(self.master, text="Dictionary:", width=20, font=("bold", 10))
        label_postingPath.place(x=30, y=380)



        # *** Entries - text boxes ***
        self.entry_corpusPath_text = StringVar()
        self.entry_corpusPath_text.set(config.get__corpusPath())
        self.entry_corpusPath = Entry(self.master, textvariable=self.entry_corpusPath_text, width=30)
        self.entry_corpusPath.place(x=180, y=130)

        self.entry_postingPath_text = StringVar()
        self.entry_postingPath_text.set(config.get__savedFileMainFolder())
        self.entry_postingPath = Entry(self.master, textvariable=self.entry_postingPath_text, width=30)
        self.entry_postingPath.place(x=180, y=160)



        # *** Stem checkbox ***
        self.stemmingCheckBox = Checkbutton(self.master)
        self.stemmingCheckBox.place(x=300, y=250)


        # *** Buttons ***
        self.buildButton = Button(self.master, text='Build', width=10, bg='green', fg='white',command= self.buildEngine).place(x=200, y=250)
        self.deleteButton = Button(self.master, text='Delete', width=10, bg='red', fg='white',command= self.deleteEngine).place(x=100, y=250)
        self.show_dict_button = Button(self.master, text='Show')
        self.load_dict_button = Button(self.master, text='Load')

        # *** Status bar ***


        # *** Language drop-down menu ***
        list1 = ['English', 'Spanish', 'Hebrew'];
        c = StringVar()
        droplist = OptionMenu(self.master, c, *list1)
        droplist.config(width=15)
        c.set('Select')
        droplist.place(x=180, y=190)



        self.root.mainloop()




    def buildEngine(self):
        print("Corpus path:     ", self.entry_corpusPath.get())
        corpusPath = str(self.entry_corpusPath.get())
        self.config.setCorpusPath(corpusPath)
        # self.disableBuildBtn()
        print(self.stemmingCheckBox)

        saveMainFolderPath = str(self.entry_postingPath.get())
        self.config.setSaveMainFolderPath(saveMainFolderPath)
        print("Posting path:     ", saveMainFolderPath)

        # Todo - disable button

        print("\n***    ManagerRun    ***")
        from threading import Thread
        th = Thread(target=self.mainManager.managerRun)
        # threadProgress = Thread(target=updateFileCounter)
        th.start()
        # threadProgress.start()
        print('Start')




    def deleteEngine(self):
        import shutil
        shutil.rmtree(self.config.get__savedFileMainFolder())
        print("Folder was deleted successfully..")

    def update_option_menu(self, alist):
        menu = self.drop_down_menu["menu"]
        menu.delete(0, "end")
        for string in alist:
            menu.add_command(label=string,
                             command=lambda value=string: self.variable.set(value))


from Configuration import ConfigClass
from Main import MainClass
example = GUI(config=ConfigClass(),mainManager=MainClass(),numOfTotalFiles=10)
print('Sup')