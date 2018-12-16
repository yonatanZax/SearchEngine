from tkinter import ttk

try:
    from Tkinter import *
    from ttk import *
except ImportError:  # Python 3
    from tkinter import *
    from tkinter.ttk import *


class App(Frame):

    def __init__(self, parent,dataTwoDArray,headLineAsArray):
        Frame.__init__(self, parent)
        self.data = dataTwoDArray
        self.headLine = headLineAsArray

        self.parent = parent
        self.CreateGUI()
        self.LoadTable()
        width = 150 * len(headLineAsArray)
        width = "%sx800" % (width)
        parent.geometry(width)



    def CreateGUI(self):
        self.treeview = Treeview(self.parent)
        headers = self.headLine[1:]
        self.treeview['columns'] = tuple(self.headLine)
        self.treeview.heading("#0", text='Index', anchor='center')
        self.treeview.column("#0", anchor="w",width=70)

        head = self.headLine[0]
        self.treeview.heading(head, text=head)
        self.treeview.column(head, anchor='w', width=150)
        for head in headers:
            self.treeview.heading(head, text=head)
            self.treeview.column(head, anchor='center', width=100)

        self.treeview.pack(side='left',fill='y')

        self.scrollbar = ttk.Scrollbar(self.parent)
        self.scrollbar.pack(side='right', fill='y')
        #
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command = self.treeview.yview)



    def LoadTable(self):
        counter = 0
        for key, value in self.data.items():
            counter += 1
            tempList = [key] + value
            self.treeview.insert('', 'end', text=counter, values=tuple(tempList))



class TableView:

    def __init__(self,dataArray,headLineAsArray):
        self.data = dataArray
        self.headLine = headLineAsArray

    def run(self):
        root = Tk()
        App(root,self.data, self.headLine)
        root.mainloop()

