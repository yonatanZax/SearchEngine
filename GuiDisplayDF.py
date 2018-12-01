#       *****               Display Dataframe GUI               *****


'''
Credits:

https://pythonspot.com/pyqt5-table/

https://stackoverflow.com/questions/47020995/pyqt5-updating-dataframe-behind-qtablewidget



'''

import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView
from PyQt5.QtCore import pyqtSlot, QTimer


class TableWidget(QTableWidget):
    def __init__(self, df, parent=None):
        QTableWidget.__init__(self, parent)
        self.df = df
        nRows = len(self.df.index)
        nColumns = len(self.df.columns)
        self.setRowCount(nRows)
        self.setColumnCount(nColumns)
        self.setHorizontalHeaderLabels(['DOCID', 'max_tf', 'uniqueTermCount','DocLength','city'])

        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                cell = self.df.iloc[i, j]
                self.setItem(i, j, QTableWidgetItem(str(cell)))

        self.cellChanged.connect(self.onCellChanged)

    @pyqtSlot(int, int)
    def onCellChanged(self, row, column):
        text = self.item(row, column).text()
        number = float(text)
        self.df.set_value(row, column, number)


class App(QWidget):

    def __init__(self,dataframe = None):
        super().__init__()
        self.title = 'Dictionary'
        self.df = dataframe
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 1000
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)


        # Show widget
        self.show()

    def createTable(self):
        # Create Dataframe
        import numpy as np
        p_file = 'D:\SearchEngine\SavedFiles - fullCorpus 29.11\WithoutStem\docIndex'
        dashboard_df = pd.read_csv(p_file, sep='|', error_bad_lines=False, index_col=False, dtype='unicode')
        df = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)))
        self.tableWidget = TableWidget(dashboard_df, self)

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())




class DisplayDataFrame:

    def __init__(self,dataframe = None):
        self.df = dataframe

    def runAndCloseFast(self):
        app = QApplication(sys.argv)
        ex = App()
        # timer = QTimer()
        # timer.start(500)  # You may change this if you wish.
        # timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.
        # Your code here.
        # sys.exit(app.exec_())
        app.exec_()

    def run(self):
        app = QApplication(sys.argv)
        ex = App()
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())