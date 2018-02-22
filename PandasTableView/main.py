from PyQt5 import QtCore, QtGui, QtWidgets

from PandasModel import PandasModel
from can_frame_res import CAN_FRAME

class Filter(QtCore.QObject):
    def __init__(self):
        super(QtCore.QObject, self).__init__()

    def eventFilter(self, obj, event):
        print (event.type())
        return False

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=None)
        vLayout = QtWidgets.QVBoxLayout(self)
        hLayout = QtWidgets.QHBoxLayout()
        self.pathLE = QtWidgets.QLineEdit(self)
        hLayout.addWidget(self.pathLE)
        self.loadBtn = QtWidgets.QPushButton("Select File", self)
        hLayout.addWidget(self.loadBtn)
        vLayout.addLayout(hLayout)
        self.pandasTv = QtWidgets.QTableView(self)
        vLayout.addWidget(self.pandasTv)
        self.commandTransLE = QtWidgets.QLineEdit(self)
        vLayout.addWidget(self.commandTransLE)
        self.loadBtn.clicked.connect(self.loadFile)
        #self.pandasTv.setMouseTracking(True)
        #self.pandasTv.setSortingEnabled(True)
        # self.pandasTv.setAttribute(84 ,on=True)
        # self.pandasTv.clicked.connect(self.itemClick)
        #self.filter=Filter()
        #self.pandasTv.installEventFilter(self.filter)
        self.pandasTv.clicked.connect(self.cell_was_clicked)

    def loadFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "txt Files (*.txt)");
        self.pathLE.setText(fileName)
        #df = pd.read_csv(fileName)
        self.f = open(fileName, 'r', encoding='utf-8')
        dataframe = CAN_FRAME().get_dataframe_original(self.f.readlines())
        self.model = PandasModel(dataframe)
        self.pandasTv.setModel(self.model)
        self.setTableSize(70, 70, 40, self.pandasTv)

    def setTableSize(self, timeSize, idSize, dataSize, table):
        table.setColumnWidth(0, timeSize)
        table.setColumnWidth(1, idSize)
        for i in range(2, 11):
            table.setColumnWidth(i, dataSize)

        table.setMinimumSize(timeSize+idSize+dataSize*10+15,300)
        self.pandasTv.scrollToBottom()

    #获取model中的数据和
    def cell_was_clicked(self, item):
        cellContent = item.data()
        cellrow = item.row()
        #print()  # test
        sf = "You clicked on {}".format(cellContent)+" ".format(cellrow)
        self.commandTransLE.setText(self.model.getAframe(item.row()))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())