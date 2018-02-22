from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
                             QAction, QFileDialog, QApplication)
import sys

app = QApplication(sys.argv)
    #ex = MainWindow()



# standard item model
model = QtGui.QStandardItemModel(5, 3)
model.setHorizontalHeaderLabels(['ID', 'DATE', 'VALUE'])
for row, text in enumerate(['Cell', 'Fish', 'Apple', 'Ananas', 'Mango']):
    item = QtGui.QStandardItem(text)
    model.setItem(row, 2, item)

# filter proxy model
filter_proxy_model = QtGui.QSortFilterProxyModel()
filter_proxy_model.setSourceModel(model)
filter_proxy_model.setFilterKeyColumn(2) # third column

# line edit for filtering
layout = QtGui.QVBoxLayout(window)
line_edit = QtGui.QLineEdit()
line_edit.textChanged.connect(filter_proxy_model.setFilterRegExp)
layout.addWidget(line_edit)

# table view
table = QtGui.QTableView()
table.setModel(filter_proxy_model)
layout.addWidget(table)

window.show()
app.exec_()