import argparse
from datetime import datetime
import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import numpy as np
import pandas as pd

# https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]

            # Perform per-type checks and render accordingly.
            if isinstance(value, datetime):
                # Render time to YYY-MM-DD.
                return value.strftime("%Y-%m-%d")

            if isinstance(value, float) or isinstance(value, np.floating):
                # Render float to 2 dp
                return "%.2f" % value

            if isinstance(value, str):
                # Render strings with quotes
                return '"%s"' % value
            
            return str(value)
        
        if role == Qt.TextAlignmentRole:
            value = self._data.iloc[index.row(), index.column()]

            if isinstance(value, int) or isinstance(value, float) or isinstance(value, np.number):
                # Align right, vertical middle.
                return Qt.AlignVCenter + Qt.AlignRight

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, data_frame):
        super().__init__()

        self.table = QtWidgets.QTableView()

        self.model = TableModel(data_frame)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)


def main():
    parser = argparse.ArgumentParser(
                    prog='parquet_viewer',
                    description='Display an Apache Parquet File',
                    )
    parser.add_argument("filepath")

    args = parser.parse_args()

    df = pd.read_parquet(args.filepath)
    print(df.shape)

    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow(df)
    window.show()
    app.exec()

if __name__ == '__main__':
    main()