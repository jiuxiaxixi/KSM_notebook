from PyQt5 import QtCore, QtWidgets
from PandasModel import PandasModel
from KsmCommand import  KsmCommand
from CanFrame import CanFrame


class Widget(QtWidgets.QWidget):
    timer = QtCore.QTimer()
    timer2 = QtCore.QTimer()
    def __init__(self, parent=None):
        self.kc = KsmCommand('6000.xlsx') # 读取配置信息
        self.fileisLoad = False
        QtWidgets.QWidget.__init__(self, parent=None)
        v_layout = QtWidgets.QVBoxLayout(self)
        h_layout = QtWidgets.QHBoxLayout()
        self.pathLE = QtWidgets.QLineEdit(self)
        h_layout.addWidget(self.pathLE)
        self.loadBtn = QtWidgets.QPushButton("选择文件", self)
        h_layout.addWidget(self.loadBtn)
        v_layout.addLayout(h_layout)
        self.pandasTv = QtWidgets.QTableView(self)
        v_layout.addWidget(self.pandasTv)
        self.id = QtWidgets.QLineEdit(self)
        self.command = QtWidgets.QLineEdit(self)
        self.id.setMaximumWidth(50)
        self.command.setMaximumWidth(50)
        h_layout.addWidget(self.id)
        h_layout.addWidget(self.command)

        self.autoReFlashBtn = QtWidgets.QCheckBox('自动刷新',self)
        h_layout.addWidget(self.autoReFlashBtn)
        self.loadBtn.clicked.connect(self.loadFile)
        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setMaximumHeight(100)
        v_layout.addWidget(self.textEdit)

        #self.pandasTv.clicked.connect(self.cell_was_clicked)
        self.pandasTv.activated.connect(self.cell_was_clicked)
        self.pandasTv.pressed.connect(self.cell_was_clicked)
        self.pandasTv.doubleClicked.connect(self.doubleClicked_to_filter)
        self.autoReFlashBtn.stateChanged.connect(self.autoReFlashBtnCheck)
        self.timer.timeout.connect(self.update)
        self.autoReFlashBtn.toggle()
        self.times = 0

    def doubleClicked_to_filter(self,item):
        data = self.model.get_a_row(item.row())
        print(item.row(),item.column())
        if(item.column() == 1):
            self.id.setText(data['id'])
            self.proxyModelid.setFilterRegExp(data['id'])
        if (item.column() == 2):
            self.command.setText(data['d0'])
            self.proxyModeCommand.setFilterRegExp(data['d0'])
        if (item.column() > 2):
            self.id.setText("")
            self.command.setText("")
            self.proxyModeCommand.setFilterRegExp("")
            self.proxyModelid.setFilterRegExp("")


    def loadFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "txt Files (*.txt)");
        self.pathLE.setText(fileName)
        self.f = open(fileName, 'r', encoding='utf-8')
        dataframe = CanFrame().get_dataframe_original(self.f.readlines())
        #print(dataframe['d2'].as_matrix())
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
        #self.commandTransLE.setText(self.kc.get_command_res(data['id'],data['d0']))
        self.textEdit.setText(self.kc.get_command_res(data['id'],data['d0'],data['d1']))

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
            self.model.updateDisplay(CanFrame().get_dataframe_original(data))
            self.pandasTv.scrollToBottom()


if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())