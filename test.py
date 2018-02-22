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
import sys
from can_frame_res import CAN_FRAME


class MainWindow(QMainWindow):
    timer = QtCore.QTimer()

    def __init__(self):
        super().__init__()
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