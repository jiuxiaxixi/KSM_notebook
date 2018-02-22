from PyQt5 import QtCore, QtGui, QtWidgets

from PandasModel import PandasModel
from can_frame_res import CAN_FRAME

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
        self.loadBtn.clicked.connect(self.loadFile)
        self.pandasTv.setSortingEnabled(True)

    def loadFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "txt Files (*.txt)");
        self.pathLE.setText(fileName)
        #df = pd.read_csv(fileName)
        self.f = open(fileName, 'r', encoding='utf-8')
        dataframe = CAN_FRAME().get_dataframe_original(self.f.readlines())
        model = PandasModel(dataframe)
        self.pandasTv.setModel(model)
        self.setTableSize(70, 70, 40, self.pandasTv)

    def setTableSize(self, timeSize, idSize, dataSize, table):
        table.setColumnWidth(0, timeSize)
        table.setColumnWidth(1, idSize)
        for i in range(2, 11):
            table.setColumnWidth(i,dataSize)
        #table.setFixedWidth()
        table.setMinimumSize(timeSize+idSize+dataSize*10+15,300)
        self.pandasTv.scrollToBottom()
        #self.pandasTv.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
       # self.pandasTv.setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff)
       # self.pandasTv.setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff)

        #self.pandasTv.resizeColumnsToContents()
        #self.pandasTv.setFixedSize(
            #self.pandasTv.horizontalHeader().length() + self.pandasTv.verticalHeader().width(), self.pandasTv.verticalHeader().length() + self.pandasTv.horizontalHeader().height())

       # header = self.pandasTv.horizontalHeader()
        #header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        #header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        #header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())