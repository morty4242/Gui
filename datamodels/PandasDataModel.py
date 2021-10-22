from dateutil.tz import tzlocal
from datetime import timedelta
from PyQt5 import QtCore
import logging as logger
import pandas as pd
import numpy as np

# TODO: optimize dataframe to dict when performance is slow
LOCAL_TIMEZONE = tzlocal()


class PandasDataModel(QtCore.QAbstractTableModel):
    def __init__(self, df_=pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self.df = df_
        # self.asset_map = {}
        # self.order_id_map = {}

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self.df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

        elif orientation == QtCore.Qt.Vertical:
            try:
                return self.df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self.df.iloc[index.row(), index.column()]))

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        row = self.df.index[index.row()]
        col = self.df.columns[index.column()]

        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self.df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self.df.set_value(row, col, value)
        self.dataChanged.emit(index, index, [])
        self.layoutChanged.emit()
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.df.columns)


class NewPandasDataModel(QtCore.QAbstractTableModel):
    def __int__(self, df_=pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self)
        self._data = df_

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == QtCore.Qt.Vertical:
                return str(self._data.index[section])
