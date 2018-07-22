from PyQt5 import QtCore
from DfProcess import DfProcess
import pandas as pd

class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, df = pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df_display = df
        self._filterDf = df
        self._df = df
        self.filterCommand = ''
        self.filterValue   = ''

    def setDataFrame(self, df):
        self._df_display = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df_display.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df_display.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        if index.row() >= self.rowCount():
            return QtCore.QVariant()
        if index.column() >= self.columnCount():
            return QtCore.QVariant()

        if str(self._df_display.ix[index.row(), index.column()]) == '0':
            return ''
        return QtCore.QVariant(str(self._df_display.ix[index.row(), index.column()]))

    def flags(self, index):
            flags = QtCore.QAbstractTableModel.flags(self, index)
            return flags

    def setData(self, index, value, role):
        row = self._df_display.index[index.row()]
        col = self._df_display.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df_display.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df_display.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df_display.columns)

    def sort(self, column, order):
        colname = self._df_display.columns.values[column]
        self.layoutAboutToBeChanged.emit()
        self._df_display.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df_display.reset_index(inplace=True, drop=True) # <-- this is the change
        self.layoutChanged.emit()

    def updateDisplay(self, df):
        self.layoutAboutToBeChanged.emit()
        #增加数据
        self._df = self._df.append(df, ignore_index=True) #change data
        #增加过滤后数据的显示
        if self.filterValue != '' or self.filterCommand != '':
            fdf = DfProcess().filter2_df('id', self.filterCommand, 'd0', self.filterValue, df)
            self._df_display = self._df_display.append(fdf,ignore_index=True)
        else:
            self._df_display = self._df_display.append(df, ignore_index=True)  # change data
        self.layoutChanged.emit()

    def setfilter(self, command, value):
        self.filterCommand = command
        self.filterValue = value
        self.layoutAboutToBeChanged.emit()

        tempdf = DfProcess().filter2_df('id', command, 'd0', value, self._df)
        self._df_display = pd.DataFrame();
        self._df_display = self._df_display.append(tempdf, ignore_index=True)
        #print (self._df_display)

        if command == '' and value == '':
            self._df_display = self._df

        self.layoutChanged.emit()
        # 重新设置数据

        # 刷新显示
        #self.updateDisplay()

    def getDateFrame(self):
        return self._df_display

    # 返回一帧的字符串
    def get_a_frame_str(self, row):
        self.get_a_row(row)
        return " ".join(str(x) for x in self._df_display.iloc[row].tolist())

    # 返回一行
    def get_a_row(self, row):
        print(row, len(self._df_display))

        if len(self._df_display) > row:
            return self._df_display.iloc[row]
        else:
            return self._df.iloc[row]

    def command_res(self, list):
        for i in len(list):
            s = s, list[i]
