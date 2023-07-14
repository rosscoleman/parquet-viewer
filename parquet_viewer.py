import argparse
from datetime import datetime
import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
import numpy as np
import pandas as pd

# https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def replace_data(self, df):
        # self.dataChanged.emit(topLeft, bottomRight) was not working
        self.beginResetModel()
        self._data = df
        self.endResetModel()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]

            # Perform per-type checks and render accordingly.
            if isinstance(value, datetime):
                # Render time to YYY-MM-DD.
                return value.strftime("%Y-%m-%d")

            if isinstance(value, float) or isinstance(value, np.floating):
                # Render float to 2 dp
                return "%.4f" % value

            if isinstance(value, str):
                # Render strings with quotes
                return '"%s"' % value

            return str(value)

        if role == Qt.TextAlignmentRole:
            value = self._data.iloc[index.row(), index.column()]

            if (
                isinstance(value, int)
                or isinstance(value, float)
                or isinstance(value, np.number)
            ):
                # Align right, vertical middle.
                return Qt.AlignVCenter + Qt.AlignRight

    def rowCount(self, index):
        return self._data.shape[0] if self._data is not None else 0

    def columnCount(self, index):
        return self._data.shape[1] if self._data is not None else 0

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, data_frame=None):
        super().__init__()

        self.table = QtWidgets.QTableView()

        self.model = TableModel(data_frame)
        self.table.setModel(self.model)

        self._createActions()
        self._connectActions()
        self._createMenuBar()

        self.setCentralWidget(self.table)

    def _createActions(self):
        # Creating action using the first constructor
        self.newAction = QAction(self)
        self.openAction = QAction("&Open...", self)
        self.exitAction = QAction("&Exit", self)

    def _connectActions(self):
        self.openAction.triggered.connect(self.openFile)
        self.exitAction.triggered.connect(self.close)

    def _createMenuBar(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.exitAction)
        menuBar.addMenu(fileMenu)

    def openFile(self):
        (fileName, selectedFilter) = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Parquet File", "", "Parquet Files (*.parquet)"
        )

        print(fileName)
        df = pd.read_parquet(fileName, dtype_backend="pyarrow")
        self.model.replace_data(df)


def main():
    parser = argparse.ArgumentParser(
        prog="parquet_viewer",
        description="Display an Apache Parquet File",
    )
    parser.add_argument("-f", "--file", required=False)

    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)

    if args.file:
        df = pd.read_parquet(args.file, dtype_backend="pyarrow")

        print(df.shape)
        window = MainWindow(df)
    else:
        window = MainWindow()
        window.openFile()

    window.resize(800, 600)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
