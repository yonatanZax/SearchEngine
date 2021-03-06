import shutil
import string
import tkinter
from tkinter import *
from tkinter import filedialog
from threading import Thread
import os

from BasicMethods import get2DArrayFromFile , getDicFromFile
from Gui.TkinterTable import TableView


class EngineBuilder(Frame):


    def __init__(self, master, mainManager, config, dataNoStem=None,dataWithStem = None):
        self.master = master
        self.config = config
        self.dataNoStem = dataNoStem
        self.dataStem = dataWithStem
        self.mainManager = mainManager
        Frame.__init__(self, master)
        self.grid()

        self.numOfFilesPerIteration = config.get__filesPerIteration()

        self.XstartPixel = 60
        self.YstartPixel = 10


        label_0 = Label(self.master, text="Search Engine", width=20, font=("bold", 30))
        label_0.place( x = self.XstartPixel + 20, y = self.YstartPixel + 40)


        self.part2Button = Button(self.master, text='Part2', width=10, bg='blue', fg='white',command= self.switchPart2)
        self.part2Button.place(x = self.XstartPixel + 450, y = self.YstartPixel + 0)
        self.part2Button.configure(state = DISABLED)


        label_corpusPath = Label(self.master, text="Corpus path:", width=10, font=("bold", 10))
        label_corpusPath.place( x = self.XstartPixel + 50, y = self.YstartPixel + 130)
        self.entry_corpusPath_text = StringVar()
        self.entry_corpusPath_text.set(config.get__corpusPath())
        self.entry_corpusPath = Entry(self.master,textvariable=self.entry_corpusPath_text,width=30)
        self.entry_corpusPath.place( x = self.XstartPixel + 180, y = self.YstartPixel + 130)


        label_postingPath = Label(self.master, text="Posting path:", width=10, font=("bold", 10))
        label_postingPath.place( x = self.XstartPixel + 50,  y = self.YstartPixel + 160)
        self.entry_postingPath_text = StringVar()
        self.entry_postingPath_text.set(config.get__savedFileMainFolder())
        self.entry_postingPath = Entry(self.master,textvariable=self.entry_postingPath_text,width=30)
        self.entry_postingPath.place( x = self.XstartPixel + 180, y = self.YstartPixel + 160)


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
        self.corpusPathButton.place( x = self.XstartPixel + 380, y = self.YstartPixel + 125)
        self.postingPathButton = Button(self.master, text='Find', width=5, fg='black',command= postingPath)
        self.postingPathButton.place( x = self.XstartPixel + 380, y = self.YstartPixel + 155)




        label_4 = Label(self.master, text="Language:", width=10, font=("bold", 10))
        label_4.place( x = self.XstartPixel + 50, y = self.YstartPixel + 190)


        list1 = ['English', 'Spanish', 'Hebrew']
        c = StringVar()
        self.droplist = OptionMenu(self.master, c, *list1)
        self.droplist.config(width=15)
        c.set('Select')
        self.droplist.place( x = self.XstartPixel + 180, y = self.YstartPixel + 190)


        self.deleteButton = Button(self.master, text='Delete', width=10, bg='red', fg='white',command= self.deleteEngine)
        self.deleteButton.place( x = self.XstartPixel + 100, y = self.YstartPixel + 250)
        self.buildButton = Button(self.master, text='Build', width=10, bg='green', fg='white',command= self.buildEngine)
        self.buildButton.place( x = self.XstartPixel + 200, y = self.YstartPixel + 250)


        label_stemming = Label(self.master, text="Stemming", width=10, font=("bold", 10))
        label_stemming.place( x = self.XstartPixel + 320, y = self.YstartPixel + 250)
        self.checked = BooleanVar()
        self.stemmingCheckBox = Checkbutton(self.master, variable = self.checked)
        self.stemmingCheckBox.place( x = self.XstartPixel + 300, y = self.YstartPixel + 250)


        # Create progress bar

        self.label_postingProgress = Label(self.master, text=" ", width=50, font=("bold", 10))
        self.label_postingProgress.place(x =self.XstartPixel + 40, y =self.YstartPixel + 300)

        self.label_mergeProgress = Label(self.master, text=" ", width=50, font=("bold", 10))
        self.label_mergeProgress.place(x =self.XstartPixel + 40, y =self.YstartPixel + 320)



        # Set Progress bar
        self.setProgressBar()




        label_postingPath = Label(self.master, text="Dictionary:", width=20, font=("bold", 10))
        label_postingPath.place( x = self.XstartPixel + 30, y = self.YstartPixel + 380)



        self.uploadDicButton = Button(self.master, text='Upload', width=10, bg='blue', fg='white',command= self.loadDictionary)
        self.uploadDicButton.place( x = self.XstartPixel + 170, y = self.YstartPixel + 380)
        self.showDicButton = Button(self.master, text='Show', width=10, bg='blue', fg='white',command= self.displayDicionary)
        self.showDicButton.place(x = self.XstartPixel + 270, y = self.YstartPixel + 380)

        self.label_buildDetails = Label(self.master, text="",width=50 ,font=("bold",10))
        self.label_buildDetails.place( x = self.XstartPixel + 50, y = self.YstartPixel + 420)


        Label(self.master, text="Summary:", width=10, font=("bold", 10)).place( x = self.XstartPixel + 20, y = self.YstartPixel + 420)


        from tkinter import scrolledtext
        self.txtbox = scrolledtext.ScrolledText( width = 45, height = 10)
        self.txtbox.place( x = self.XstartPixel + 60, y = self.YstartPixel + 450)

        self.statusLabel = Label(self.master, text="Status: Ready to Build\Shut down", width = 40, font = ("bold", 10))
        self.statusLabel.place( x = self.XstartPixel + 60, y = self.YstartPixel + 650)






    def switchPart2(self):


        if self.entry_postingPath.get() == '':
            self.statusLabel['text'] = 'Status: Enter a path to posting'
            return


        saveMainFolderPath = str(self.entry_postingPath.get())
        if not os.path.exists(saveMainFolderPath):
            self.statusLabel['text'] = 'Status: %s path not exists' % (saveMainFolderPath,)
            return

        if '/SavedFiles' not in saveMainFolderPath :
            saveMainFolderPath += '/SavedFiles'
            self.config.setSaveMainFolderPath(saveMainFolderPath)



        if self.dataStem is None and self.dataNoStem is None:
            self.statusLabel['text'] = 'Status: No data available, please upload'
            return

        pathToStopWords = saveMainFolderPath + "/" + self.config.stopWordFile
        if os.path.exists(pathToStopWords):
            self.config.stopWordPath = pathToStopWords

        else:
            self.statusLabel['text'] = 'Status: No stop words file'
            return


        self.config.setToStem(False)
        self.checked.set(False)


        from Gui.GuiPart2 import QuerySearcher
        self.master.destroy()
        self.master = Tk()
        setWindowSizeAndPosition(self.master)
        self.master.title("SearchEngine")
        guiFrame = QuerySearcher(self.master, mainManager=self, config=self.config,cityList=self.getCityList(),dataNoStem=self.dataNoStem,dataWithStem=self.dataStem)
        guiFrame.mainloop()


    def getCityList(self):
        cityIndexPath = self.config.getSavedFilesPath() + '/cityIndex'
        list = []

        if os.path.exists(cityIndexPath):
            myFile = open(cityIndexPath,'r')
            listFromFile = myFile.readlines()

            for line in listFromFile:
                splitedLine = line.split('|')
                list.append(splitedLine[0])

        return list



    def setProgressBar(self):

        # Set Progress bar
        linesAsString = ''
        for i in range(0, 51):
            if i % 4 == 0:
                continue
            linesAsString += ' '
        self.posting_progressLabel = "Posting Progress:     ["
        self.merge_progressLabel = "Merge Progress:       ["
        self.label_postingProgress['text'] = self.posting_progressLabel + linesAsString + '] 00%'
        self.label_mergeProgress['text'] = self.merge_progressLabel + linesAsString + '] 00%'



    def updateProgress(self, posting_merge):
        flag = True
        import os
        import time

        sleepTime = 2

        while flag:

            time.sleep(sleepTime)
            counter = 0

            path = self.config.get__savedFilePath() + '/Progress/%s' % (posting_merge)
            if not os.path.exists(path):
                break
            listOfFiles = os.listdir(path)
            if len(listOfFiles) == 0:
                continue

            dicByManagerID = {}
            for file in sorted(listOfFiles):
                splitedFile = file.split('_')
                managerID = splitedFile[0]
                managerFileCount = int(splitedFile[1])

                if managerID == '-1':
                    # sleepTime = 10
                    shutil.rmtree(path)
                    os.mkdir(path)
                    dicByManagerID = {}
                    dicByManagerID['-1'] = managerFileCount
                    break
                if dicByManagerID.get(managerID) is None:
                    dicByManagerID[managerID] = managerFileCount
                else:
                    if managerFileCount > dicByManagerID[managerID]:
                        dicByManagerID[managerID] = managerFileCount


            for value in dicByManagerID.values():
                counter += value



            if posting_merge == 'Posting':
                percent = (counter / self.config.get_numOfFiles()) * 50
                percent = int(percent)

            elif posting_merge == 'Merge':

                percent = (counter / (self.config.get_numOfFiles() + 27*50)) * 50
                percent = int(percent)



            if percent >= 49:
                linesAsString = ''
                for i in range(0, 51):
                    linesAsString += '|'
                self.label_postingProgress['text'] = self.posting_progressLabel + linesAsString + '] 100%'
                return

            linesAsString = ''
            for i in range(0,percent + 1):
                linesAsString += '|'
            for i in range(percent + 1,51):
                if i % 4 == 0:
                    continue
                linesAsString += ' '


            percentString = str(percent * 2)

            if len(percentString) == 1:
                percentString = '0' + percentString

            if posting_merge == 'Posting':
                self.label_postingProgress['text'] = self.posting_progressLabel + linesAsString + '] ' + percentString + '% '
            elif posting_merge == 'Merge':
                self.label_mergeProgress['text'] = self.merge_progressLabel + linesAsString + '] ' + percentString + '% '



    def load(self):



        savedMainFolder = self.config.get__savedFileMainFolder()
        savedNoStem = savedMainFolder + '/WithoutStem'
        savedWithStem = savedMainFolder + '/WithStem'


        lettersList = list(string.ascii_lowercase)
        lettersList.append('#')


        totalDict_noStem = dict()
        totalDict_withStem = dict()

        for letter in lettersList:

            pathNoStem = savedNoStem + '/' + letter + '/' + 'mergedFile_dic'
            if os.path.exists(pathNoStem):

                letterDicFromFile = getDicFromFile(path=pathNoStem)

                if len(totalDict_noStem) == 0:
                    totalDict_noStem = letterDicFromFile
                else:
                    totalDict_noStem.update(letterDicFromFile)


            pathWithStem = savedWithStem + '/' + letter + '/' + 'mergedFile_dic'
            if os.path.exists(pathWithStem):

                letterDicFromFile = getDicFromFile(path=pathWithStem)

                if len(totalDict_noStem) == 0:
                    totalDict_withStem = letterDicFromFile
                else:
                    totalDict_withStem.update(letterDicFromFile)

        if len(totalDict_noStem) == 0:
            self.dataNoStem = None
        else:
            self.dataNoStem = totalDict_noStem

        if len(totalDict_withStem) == 0:
            self.dataStem = None
        else:
            self.dataStem = totalDict_withStem


        pathToLanguages = self.config.get__savedFileMainFolder() + "/languages"
        if os.path.exists(pathToLanguages):
            languageFile = open(pathToLanguages, 'r')
            languageList = languageFile.readlines()

            self.setLanguagesDropList(languageList)



        self.part2Button.configure(state = NORMAL)





    def loadDictionary(self):


        if self.entry_postingPath.get() == '':
            self.statusLabel['text'] = 'Status: Enter a path to posting'
            return

        if not os.path.exists(self.entry_postingPath.get()):
            self.statusLabel['text'] = 'Status: Enter a valid path to posting'
            return


        self.config.setSaveMainFolderPath(self.setMainPathString(self.entry_postingPath.get()))


        check = self.checked.get()
        self.config.setToStem(check)

        if not os.path.exists(self.config.savedFilePath + '/a'):
            if check:
                self.statusLabel['text'] = 'Status (stem is checked): build before load'
            else:
                self.statusLabel['text'] = 'Status (stem not checked): build before load'

            return


        self.disableButtons()
        self.statusLabel['text'] = 'Status: Loading terms'

        print('Load dictionary')

        t = Thread(target=self.load, args=())
        displayThread = Thread(target=self.listener, args=(t, self.enableButtons))
        t.start()
        displayThread.start()




    def displayDicionary(self):
        if self.entry_postingPath.get() == '':
            self.statusLabel['text'] = 'Status: Enter a path to posting'
            return

        if not os.path.exists(self.entry_postingPath.get()):
            self.statusLabel['text'] = 'Status: Enter a valid path to posting'
            return

        check = self.checked.get()
        self.config.setToStem(check)
        data = None


        if self.config.toStem:
            if self.dataStem is None:

                self.statusLabel['text'] = 'Status (stem is checked): upload before Show'
                return
            else:
                data = self.dataStem

        else:
            if self.dataNoStem is None:

                self.statusLabel['text'] = 'Status (stem not checked): upload before Show'
                return
            else:
                data = self.dataNoStem



        self.disableButtons()
        self.part2Button.configure(state = NORMAL)

        print('Display dictionary')

        self.statusLabel['text'] = 'Status: preparing a nice table to view terms'

        self.displayClass = TableView(data, ['Term', 'df', 'sumTF', '# Posting'])




        t = Thread(target=self.displayClass.run,args=())
        displayThread = Thread(target=self.listener,args =(t,self.enableButtons))
        t.start()
        displayThread.start()


    def deleteEngine(self):
        import shutil
        saveMainFolderPath = str(self.entry_postingPath.get())


        if self.entry_postingPath.get() == '':
            self.statusLabel['text'] = 'Status: %s invalid path to delete' % (saveMainFolderPath,)
            return


        pathToDelete = saveMainFolderPath + '/SavedFiles'
        if not os.path.exists(pathToDelete):

            self.statusLabel['text'] = 'Status: %s invalid path to delete' % (saveMainFolderPath,)
            return



        shutil.rmtree(pathToDelete)
        print("Folder was deleted successfully..")
        self.setProgressBar()
        self.enableButtons()
        self.statusLabel['text'] = 'Deleted: Folder %s ' % (pathToDelete)




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


        saveMainFolderPath = self.setMainPathString(saveMainFolderPath)
        self.config.setSaveMainFolderPath(saveMainFolderPath,True)


        print("Posting path:     ", saveMainFolderPath)


        self.disableButtons()

        print("\n***    ManagerRun    ***\n")


        self.setProgressBar()

        from datetime import datetime
        time = datetime.now().strftime('%H:%M:%S')
        self.statusLabel['text'] = '%s - Started building.. might take a while' % (time)

        from threading import Thread
        from concurrent.futures import ThreadPoolExecutor

        executor = ThreadPoolExecutor()
        future = executor.submit(self.mainManager.managerRun)


        threadWaitUntilBuildDone = Thread(target=self.buildListener, args=(future,))
        threadWaitUntilBuildDone.start()


        threadPostingProgress = Thread(target=self.updateProgress , args=('Posting',))
        threadPostingProgress.start()


        threadMergeProgress = Thread(target=self.updateProgress, args=('Merge',))
        threadMergeProgress.start()


    @ staticmethod
    def listener(thread,action):
        thread.join()
        action()



    def buildListener(self,future):
        from Parsing.ConvertMethods import converSecondsToTime

        timeItTook, maxParsingTime, totalMerging, totalNumberOfTerms, totalNumberOfDocuments ,mergedLanguagesSet = future.result()

        self.setLanguagesDropList(mergedLanguagesSet)



        self.setBuildDetails(timeItTook, maxParsingTime, totalMerging, totalNumberOfTerms, totalNumberOfDocuments)


        print("Number of Terms: " , str(totalNumberOfTerms))
        print("Number of Docs: " , str(totalNumberOfDocuments))
        print("Parsing Time: " , str(converSecondsToTime(maxParsingTime)))
        print("Merging Time: " , str(converSecondsToTime(totalMerging)))
        print("Everything took: " , str(converSecondsToTime(timeItTook)))
        self.enableButtons()



    def setBuildDetails(self, timeItTook, maxParsingTime, totalMerging, totalNumberOfTerms, totalNumberOfDocuments):
        from Parsing.ConvertMethods import converSecondsToTime
        stem = ''
        if self.config.toStem:
            stem = '\n** Run with stemming - Details **\n'
        else:
            stem = '\n** Run without stemming - Details **\n'
        detailString = stem
        detailString += "\tNumber of Terms:  " + str(totalNumberOfTerms) + "\n"
        detailString += "\tNumber of Docs:   " + str(totalNumberOfDocuments) + "\n"
        detailString += "\tParsing Time:     " + str(converSecondsToTime(maxParsingTime)) + "\n"
        detailString += "\tMerging Time:     " + str(converSecondsToTime(totalMerging)) + "\n"
        detailString += "\tEverything took:  " + str(converSecondsToTime(timeItTook)) + "\n"

        linesAsString = ''
        for i in range(0, 51):
            linesAsString += '|'
        self.label_postingProgress['text'] = self.posting_progressLabel + linesAsString + '] 100%'
        self.label_mergeProgress['text'] = self.merge_progressLabel + linesAsString + '] 100%'

        self.txtbox.insert('end',detailString)



    def enableButtons(self):
        self.buildButton.configure(state = NORMAL)
        self.deleteButton.configure(state = NORMAL)
        self.showDicButton.configure(state = NORMAL)
        self.uploadDicButton.configure(state = NORMAL)


    def disableButtons(self):
        self.buildButton.configure(state = DISABLED)
        self.deleteButton.configure(state = DISABLED)
        self.showDicButton.configure(state = DISABLED)
        self.uploadDicButton.configure(state = DISABLED)
        self.part2Button.configure(state = DISABLED)



    def setMainPathString(self,newPath):
        if newPath.endswith("SavedFiles"):
            return newPath
        else:
            return newPath + '/SavedFiles'



    def setLanguagesDropList(self,languageList):

        if len(languageList) > 0:
            self.droplist.destroy()
            c = StringVar()
            self.droplist = OptionMenu(self.master, c, *languageList)
            self.droplist.config(width=15)
            c.set('Select')
            self.droplist.place(x=self.XstartPixel + 180, y=self.YstartPixel + 190)







def setWindowSizeAndPosition(root):

    w = 600  # width for the Tk root
    h = 700  # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # set the dimensions of the screen
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    return root















