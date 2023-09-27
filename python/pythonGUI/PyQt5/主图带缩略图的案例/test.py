import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QLabel,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt
import pyqtgraph as pg

from PyQt5.QtCore import QRect


class MyPlotWidget(pg.PlotWidget):
    def __init__(self, x, y, symbol="o"):
        super().__init__()
        self.x = x
        self.y = y
        self.curve = self.plot(x, y, symbol=symbol)
        self.show()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.tab_widget = PlotTabWidget()
        layout.addWidget(self.tab_widget)

        self.preview_layout = QHBoxLayout()
        self.preview_widget = QWidget()
        self.preview_widget.setLayout(self.preview_layout)
        self.preview_widget.setFixedHeight(200)

        layout.addWidget(self.preview_widget)
        for i in range(self.tab_widget.count()):
            plot_widget = self.tab_widget.widget(i)
            # 捕获PlotWidget的图像
            pixmap = plot_widget.grab(QRect(0, 0, 100, 100))
            # 缩放Pixmap到缩略图大小
            pixmap = pixmap.scaled(100, 100)

            label = QLabel()
            label.setPixmap(pixmap)
            label.mousePressEvent = lambda event, i=i: self.switch_tab(event, i)
            self.preview_layout.addWidget(label)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)

        self.setGeometry(200, 200, 1200, 800)
        self.setWindowTitle("Example")
        self.show()

    def switch_tab(self, event, index):
        self.tab_widget.setCurrentIndex(index)


class PlotTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pw1 = MyPlotWidget([1, 2, 3], [3, 2, 1])
        self.addTab(self.pw1, "标签1")

        self.pw2 = MyPlotWidget([1, 2, 3], [1, 2, 1])
        self.addTab(self.pw2, "标签2")

        self.pw3 = MyPlotWidget([1, 2, 3], [3, 2, 1])
        self.addTab(self.pw3, "标签3")

        self.pw4 = MyPlotWidget([1, 2, 3], [1, 0, 1])
        self.addTab(self.pw4, "标签4")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
