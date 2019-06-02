from PyQt5 import QtCore
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtGui import QFont, QBrush, QColor
import pandas as pd
import numpy as np
import re


class DicObj:
    def __init__(self, lines, values, index, books):
        self.lines = lines
        self.values = values
        self.index = index
        self.books = books
        data = pd.DataFrame()
        data["words"] = lines
        data["values"] = values
        data["index"] = index
        data["books"] = books
        self.data = data

    def print_this(self):
        print(self.data)

    def save_this(self):
        self.data.to_csv("Bible_data.csv")

    @staticmethod
    def read_csv(path):
        my_data = pd.read_csv(path)
        return my_data

    def create_output(self, check):
        pass


class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, key_word, df=pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df.reset_index()
        self.key_word = key_word

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if (role != QtCore.Qt.DisplayRole) and (role != QtCore.Qt.BackgroundRole):
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        # questa parte modifica il colore della casella se il dato "word" espresso coincide con il dato in input (se non numerico!)
        # per ora è True solo con == "אדם" e basta: inserire la "word" ricercata (se parola e non numero!) nel metodo in gimatria_gui.py
        if role == QtCore.Qt.BackgroundRole:
            # print("merda zero")
            if self.data(self.index(index.row(), 2), QtCore.Qt.DisplayRole):
                # merda = self.data(self.index(7, 2))
                # print("merda", merda, self.index(7,2).data())
                # print(self.key_word, "key word in second phase")
                return QBrush(QColor(245,156,12)) if self.index(index.row(), index.column()).data() == self.key_word else False
            return self.data(index, role)

        #print(index, "indexx", index.row(), index.column(), index.isValid)
        #self._df.reset_index()
        #print("indexrow", self._df.iloc[0:20,0:3])
        #self._df.set_index("books")
        #print("\n||", self._df.iloc[0:10,0:2], "loc su dataframe")

        #self._df.set_index("index")
        return QtCore.QVariant(str(self._df.ix[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

class BoldDelegate(QStyledItemDelegate):
    def __init__ (self, parent = None):
        QStyledItemDelegate.__init__(parent=parent)
        pass

if __name__ == "__main__":
    pass
