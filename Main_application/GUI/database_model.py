import pandas
from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QColor, QLinearGradient, QBrush


class DataModel(QAbstractTableModel):
    def __init__(self, data: pandas.DataFrame) -> None:
        QAbstractTableModel.__init__(self)
        self._data = data
        self._colors = ["#FF2222", "#15C655"]
        self._columns = list(self._data.columns)

    def data(self, index, role):
        if index.isValid():
            if (role == Qt.DisplayRole) or (role == Qt.EditRole):
                value = self._data.iloc[index.row(), index.column()]
                return str(value)

            if role == Qt.ForegroundRole:
                value = self._data.iloc[index.row(), index.column()]

                if value == "Unsuccessful":
                    return self.create_gradient_brush()
                    # return QColor('rgb(255,255,255)')

                if value == "Successful":
                    return self.create_gradient_brush()
                    # return QColor('rgb(255,255,255)')

            if role == Qt.BackgroundRole:
                value = self._data.iloc[index.row(), index.column()]

                if value == "Unsuccessful":
                    return QColor(self._colors[0])

                if value == "Successful":
                    return QColor(self._colors[1])

            if role == Qt.TextAlignmentRole:
                return Qt.AlignVCenter + Qt.AlignHCenter

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return int(self._data.shape[0])

    def columnCount(self, index):
        return int(self._data.shape[1])

    @staticmethod
    def create_gradient_brush() -> QBrush:
        _gradient = QLinearGradient(1.0, 30.0, 1000.0, 230.0)
        _gradient.setColorAt(0.0, QColor('rgb(11, 141, 255)'))
        _gradient.setColorAt(1.0, QColor('rgb(238, 238, 238)'))
        _brush = QBrush(_gradient)
        # print(_brush.gradient())
        return _brush

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

        if role == Qt.ForegroundRole:
            # value = self._data.iloc[index.row(), index.column()]
            return QColor('rgb(255, 255, 255)')

        if role == Qt.BackgroundRole:
            return QColor('rgb(11, 141, 255)')
