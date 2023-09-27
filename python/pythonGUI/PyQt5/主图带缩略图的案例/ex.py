import sys
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QVBoxLayout,
    QWidget,
    QGraphicsView,
    QGraphicsScene,
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import numpy as np


class MyPlotWidget(pg.PlotWidget):
    def __init__(self):
        super(MyPlotWidget, self).__init__()
        self.curve = self.plot([1, 2, 3], [2, 1, 3], symbol="o")
        self.show()

    def get_thumbnail(self):
        qimage = self.grab().toImage()
        thumb = qimage.scaled(300, 300, Qt.KeepAspectRatio, Qt.FastTransformation)
        return QPixmap.fromImage(thumb)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        pw = MyPlotWidget()

        thumbnail = pw.get_thumbnail()

        preview_widget = QGraphicsView()
        scene = QGraphicsScene()
        scene.addPixmap(thumbnail)
        preview_widget.setScene(scene)
        preview_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        preview_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(pw)
        layout.addWidget(preview_widget)

        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setGeometry(200, 200, 600, 800)
        self.setWindowTitle("test")
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
