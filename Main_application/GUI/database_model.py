import pandas
from PySide6.QtCore import QAbstractTableModel,Qt
from PySide6.QtGui import QColor

class DataModel(QAbstractTableModel):
    def __init__(self, data: pandas.DataFrame) -> None:
        super().__init__()
        self._data = data
        self._colors = ["#FF2222","#15C655"]
    
    def data(self, index, role):
        if(index.isValid()):
            if((role == Qt.DisplayRole) or (role == Qt.EditRole)):
                value = self._data.iloc[index.row(), index.column()]
                return str(value)
            
            if(role == Qt.ForegroundRole):
                value = self._data.iloc[index.row(), index.column()]
                
                if(value == "Unsuccessful"):
                    return QColor(self._colors[0])
                
                if(value == "Successful"):
                    return QColor(self._colors[1])
            
            if(role == Qt.TextAlignementRole):
                return Qt.AlignVCenter + Qt.AlignHCenter
    
    def setData(self, index, value, role):
        if(role == Qt.EditRole):
            value = self._data.iloc[index.row(),index.column()]
            return str(value)
    
    def rowCount(self, index):
        return int(self._data.shape[0])
    
    def columnCount(self, index):
        return int(self._data.shape[1])
    
    def headerData(self, section, orientation, role):
        if(role == Qt.DisplayRole):
            if(orientation == Qt.Horizontal):
                return str(self._data.columns[section])
            
            if(orientation == Qt.Vertical):
                return str(self._data.index[section])
