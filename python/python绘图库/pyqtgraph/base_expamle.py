from PyQt5 import QtWidgets
import pyqtgraph as pg
import sys
import os

import numpy as np


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        x = np.random.normal(size=1000)
        y = np.random.normal(size=1000)
        self.graphWidget.plot(x, y, pen=None, symbol="o")


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()