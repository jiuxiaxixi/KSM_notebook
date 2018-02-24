from PyQt5 import QtCore, QtGui, QtWidgets

from PandasModel import PandasModel

import pandas as pd
import numpy as np


class CAN_FRAME() :

    def  get_dataframe_original(self, lines):
        l=[]
        columns = ['time', 'id', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'count']
        for line in range(len(lines)):
            self.line_res(lines[line].strip('\n') ,l)
        return pd.DataFrame(np.array(l), columns=columns)

    def  line_res(self, line,list):
        if len(line)>45:
            buf = line.split(' ')
            #remove blank space
            while '' in buf:
                buf.remove('')
            #add zeros to fit the size
            while len(buf) < 11:
                buf.insert(len(buf)-1, '0')
            if( len(buf) == 11):
                list.append(buf)

    def hex_to_dec(self, x):
        return int(x, 16)

    def dataframe_to_int(self,list,columns):
        dataframe= pd.DataFrame(np.array(list), columns=columns)
        dataframe_mapped=dataframe[[ 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7']].applymap(self.hex_to_dec)
        dataframe_mapped.insert(0,'time',dataframe['time'])
        dataframe_mapped.insert(1, 'id', dataframe['id'])
        dataframe_mapped.insert(2, 'd0', dataframe['d0'])
        dataframe_mapped.insert(dataframe_mapped.columns.__len__(), 'count', dataframe['count'])
        return  dataframe_mapped

    def get_data_frame(self,lines):
        l=[]
        columns = ['time', 'id', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'count']
        for line in range(len(lines)):
            self.line_res(lines[line].strip('\n'), l)
        return self.dataframe_to_int(l, columns)

class Widget(QtWidgets.QWidget):
    timer = QtCore.QTimer()

    def __init__(self, parent=None):
        self.fileisLoad = False
        QtWidgets.QWidget.__init__(self, parent=None)
        vLayout = QtWidgets.QVBoxLayout(self)
        hLayout = QtWidgets.QHBoxLayout()
        self.pathLE = QtWidgets.QLineEdit(self)
        hLayout.addWidget(self.pathLE)
        self.loadBtn = QtWidgets.QPushButton("choose", self)
        hLayout.addWidget(self.loadBtn)
        vLayout.addLayout(hLayout)
        self.pandasTv = QtWidgets.QTableView(self)
        vLayout.addWidget(self.pandasTv)
        self.commandTransLE = QtWidgets.QLineEdit(self)
        vLayout.addWidget(self.commandTransLE)
        self.autoReFlashBtn = QtWidgets.QCheckBox('flash',self)
        hLayout.addWidget(self.autoReFlashBtn)
        self.loadBtn.clicked.connect(self.loadFile)
        self.pandasTv.clicked.connect(self.cell_was_clicked)
        self.autoReFlashBtn.stateChanged.connect(self.autoReFlashBtnCheck)
        self.timer.timeout.connect(self.update)
        self.autoReFlashBtn.toggle()


    def loadFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "txt Files (*.txt)");
        self.pathLE.setText(fileName)
        self.f = open(fileName, 'r', encoding='utf-8')
        dataframe = CAN_FRAME().get_dataframe_original(self.f.readlines())
        self.model = PandasModel(dataframe)
        self.pandasTv.setModel(self.model)
       # self.setTableSize(70, 70, 30, 40, self.pandasTv)
        self.pandasTv.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.fileisLoad = True
        self.autoFlashTimerchange()
        self.pandasTv.scrollToBottom()

    def setTableSize(self, timeSize, idSize, dataSize, countSize, table):
        table.setColumnWidth(0, timeSize)
        table.setColumnWidth(1, idSize)

        for i in range(2, 10):
            table.setColumnWidth(i, dataSize)
        table.setColumnWidth(11, 40)
        table.setMinimumSize(timeSize+idSize+dataSize*10+countSize, 300)

        self.pandasTv.scrollToBottom()

        self.pandasTv.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView().ResizeToContents)

    def cell_was_clicked(self, item):
        cellContent = item.data()
        cellrow = item.row()
        #print()  # test
        sf = "You clicked on {}".format(cellContent)+" ".format(cellrow)
        self.commandTransLE.setText(self.model.getAframe(item.row()))

    def autoReFlashBtnCheck(self):
        if(self.autoReFlashBtn.isChecked()):
           self.autoReFlashFlag = True

        else:
            self.autoReFlashFlag = False
        if(self.fileisLoad):
            self.autoFlashTimerchange()


    def autoFlashTimerchange(self):
        if(self.autoReFlashFlag):
            self.timer.start(100)
        else:
            if(self.timer.isActive()):
                self.timer.stop()

    def update(self):
        data = self.f.readlines()
        if len(data) > 0:
            self.model.updateDisplay(CAN_FRAME().get_dataframe_original(data))
            self.pandasTv.scrollToBottom()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())