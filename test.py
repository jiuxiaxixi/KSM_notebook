#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we select a file with a
QFileDialog and display its contents
in a QTextEdit.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
                             QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
from pyqtgraph.Qt import QtCore
import pyqtgraph as pg
import sys


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
            #分割为List
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

class MainWindow(QMainWindow):
    timer = QtCore.QTimer()

    def __init__(self):
        super(MainWindow,self).__init__()
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        openFile = QAction(QIcon('open.png'), 'Open', self)
        self.statusBar()

        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('KSM Notebook')
        self.timer.timeout.connect(self.update)
        self.show()

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')
        self.filename=fname
        if fname[0]:
            self.f = open(fname[0], 'r', encoding='utf-8')
            dataframe = CAN_FRAME().get_dataframe_original(self.f.readlines())
            #print(dataframe.to_string())
            self.textEdit.append(dataframe.to_html())
            #self.text_append()
            #print(CAN_FRAME.dataframe_to_int(data))
            #self.timer.start(100)

    def update(self):
        data = self.f.readlines()
        if len(data) > 0:
            self.text_append(data)
            print("new data %d", len(data))

    def text_append(self, text_list):
        for line in range(len(text_list)):
            data=text_list[line].strip('\n')
            print(data)
            #self.textEdit.append(data)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())