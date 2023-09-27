import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
import pyqtgraph as pg


class MyPlotWidget(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.curve = self.plot([1, 2, 3], [2, 1, 3], symbol="o")
        self.show()

    def get_thumbnail(self):
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        thumbnail = QPixmap(100, 100)
        painter = QPainter(thumbnail)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.drawPixmap(0, 0, 100, 100, pixmap)
        painter.end()
        return thumbnail


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        pw = MyPlotWidget()
        thumbnail = pw.get_thumbnail()

        preview_widget = QLabel()
        preview_widget.setPixmap(thumbnail)

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
