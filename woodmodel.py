# This Python file uses the following encoding: utf-8

from PySide2 import QtCore


column_names = ["id", "part", "type1", "type2", "category", "the_class", "material",
"specie", "circumference", "length"]


class WoodModel(QtCore.QAbstractTableModel):

    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(column_names)

    def add_wood(self, wood):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(wood)
        self.endInsertRows()


    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                raw_value = getattr(self._data[index.row()], column_names[index.column()])
                if index.column() in range(1, 8):
                    return raw_value.name
                else:
                    return str(raw_value)
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return column_names[col]
        return None

