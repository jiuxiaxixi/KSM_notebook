import pyqtgraph as pg
import numpy as np
import sys
import os
import datetime
from PyQt5 import QtCore, QtWidgets
from PandasModel import PandasModel
from KsmCommand import  KsmCommand
from CanFrame import  CanFrame
from DfProcess import DfProcess

class Widget(QtWidgets.QWidget):
    timer = QtCore.QTimer()
    def __init__(self, parent=None):
        self.kc = KsmCommand('6000.xlsx') # 读取配置信息
        self.fileisLoad = False
        QtWidgets.QWidget.__init__(self, parent=None)
        v_layout = QtWidgets.QVBoxLayout(self)
        h_layout = QtWidgets.QHBoxLayout()
        self.pathLE = QtWidgets.QLineEdit(self)
        h_layout.addWidget(self.pathLE)
        self.loadBtn = QtWidgets.QPushButton("选择文件", self)
        self.saveBtn = QtWidgets.QPushButton("保存", self)
        self.drawBtn = QtWidgets.QPushButton("绘图",self)
        h_layout.addWidget(self.loadBtn)
        h_layout.addWidget(self.saveBtn)
        v_layout.addLayout(h_layout)
        self.pandasTv = QtWidgets.QTableView(self)
        v_layout.addWidget(self.pandasTv)
        self.id = QtWidgets.QLineEdit(self)
        self.command = QtWidgets.QLineEdit(self)
        self.id.setMaximumWidth(50)
        self.command.setMaximumWidth(50)
        h_layout.addWidget(self.id)
        h_layout.addWidget(self.command)
        h_layout.addWidget(self.drawBtn)

        self.autoReFlashBtn = QtWidgets.QCheckBox('自动刷新',self)
        h_layout.addWidget(self.autoReFlashBtn)
        self.loadBtn.clicked.connect(self.load_file)
        self.saveBtn.clicked.connect(self.save_file)
        self.drawBtn.clicked.connect(self.draw_filter_value)
        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setMaximumHeight(100)
        v_layout.addWidget(self.textEdit)

        self.pandasTv.activated.connect(self.cell_was_clicked)
        self.pandasTv.pressed.connect(self.cell_was_clicked)
        self.pandasTv.doubleClicked.connect(self.double_clicked_to_filter)
        self.autoReFlashBtn.stateChanged.connect(self.autoReFlashBtnCheck)

        self.timer.timeout.connect(self.update)
        self.autoReFlashBtn.toggle()
        self.id.textChanged.connect(self.filter_set)
        self.command.textChanged.connect(self.filter_set)
        self.times = 0



    def draw_filter_value(self):
        if self.id !=' ' and self.command != ' ':
            self.view = pg.GraphicsView()
            self.layout = pg.GraphicsLayout(border=(100, 100, 100))
            self.view.setCentralItem(self.layout)
            self.view.setWindowTitle('Software Oscilloscope')
            self.view.resize(800, 600)
            self.plot = self.layout.addPlot()
            #print()
            np=DfProcess().numpy_merge(self.model.getDateFrame(), 'd2', 'd3')
            #print(np)
            self.plot.plot(np)
            self.layout.nextRow()
            self.view.show()

    def filter_set(self):
        #print(self.id.text(), self.command.text())
        self.model.setfilter(self.id.text(), self.command.text())


    def double_clicked_to_filter(self,item):
        data = self.model.get_a_row(item.row())
        if item.column() == 1:
            self.id.setText(data['id'])

        if item.column() == 2:
            self.command.setText(data['d0'])

        if item.column() > 2:
            self.id.setText("")
            self.command.setText("")


    def load_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "txt Files (*.txt)")
        if filename != '':
            self.pathLE.setText(filename)
            self.f = open(filename, 'r', encoding='utf-8')
            self.model = PandasModel(CanFrame().get_dataframe_original(self.f.readlines()))
            self.pandasTv.setModel(self.model)
            self.setTableSize(70, 70, 30, 40, self.pandasTv)
            self.fileisLoad = True
            self.autoFlashTimerchange()
            self.pandasTv.scrollToBottom()

    def save_file(self):
        time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", time, "txt Files (*.txt)")
        print(filename)
        if filename != '':
            df = self.model.getDateFrame()
            DfProcess().save_to_text(filename, df)

    def setTableSize(self, timeSize, idSize, dataSize, countSize, table):
        table.setColumnWidth(0, timeSize)
        table.setColumnWidth(1, idSize)

        for i in range(2, 10):
            table.setColumnWidth(i, dataSize)
        table.setColumnWidth(11, 40)
        table.setMinimumSize(timeSize+idSize+dataSize*10+countSize, 300)

        self.pandasTv.scrollToBottom()

    def cell_was_clicked(self, item):
        data=self.model.get_a_row(item.row())
        #print(data)
        self.textEdit.setText(self.kc.get_command_res(data['id'],data['d0'],data['d1']))

    def autoReFlashBtnCheck(self):
        if self.autoReFlashBtn.isChecked():
           self.autoReFlashFlag = True
        else:
            self.autoReFlashFlag = False

        if self.fileisLoad:
            self.autoFlashTimerchange()

    def autoFlashTimerchange(self):
        if self.autoReFlashFlag:
            self.timer.start(100)
        else:
            if self.timer.isActive():
                self.timer.stop()

    def update(self):
        data = self.f.readlines()
        if len(data) > 0:
            print(data)
            dataframe = CanFrame().get_dataframe_original(data)
            self.model.updateDisplay(dataframe)
            for index, row in dataframe.iterrows():
                self.textEdit.append(self.kc.get_command_res_lite(row['id'], row['d0'], row['d1']))

            self.pandasTv.scrollToBottom()

    def commandLoadFile(self,fileName):

        if os.access(fileName, os.F_OK):
            self.pathLE.setText(fileName)
            self.f = open(fileName, 'r', encoding='utf-8')
            dataframe = CanFrame().get_dataframe_original(self.f.readlines())
            self.model = PandasModel(dataframe)
            self.proxyModelid = QtCore.QSortFilterProxyModel()
            self.proxyModelid.setSourceModel(self.model)
            self.proxyModelid.setFilterKeyColumn(1)
            self.proxyModeCommand = QtCore.QSortFilterProxyModel()
            self.proxyModeCommand.setSourceModel(self.proxyModelid)
            self.proxyModeCommand.setFilterKeyColumn(2)
            self.pandasTv.setModel(self.proxyModeCommand)
            self.setTableSize(70, 70, 30, 40, self.pandasTv)
            self.fileisLoad = True
            self.autoFlashTimerchange()
            self.pandasTv.scrollToBottom()
        else:
            self.pathLE.setText(fileName+"文件不存在")

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    if(len(sys.argv)==2):
        file = sys.argv[1]
        w.commandLoadFile(file)
    sys.exit(app.exec_())