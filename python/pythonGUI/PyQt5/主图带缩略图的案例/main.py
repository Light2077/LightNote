import sys
import typing
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)
import pyqtgraph as pg


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
        layout = QVBoxLayout(self)

        # 多个绘图的标签
        self.tab_widget = PlotTabWidget()
        layout.addWidget(self.tab_widget)

        preview_widget = PreviewWidget(self, self.tab_widget)
        layout.addWidget(preview_widget)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)

        # 设置窗口位置和宽高
        self.setGeometry(200, 200, 1200, 800)
        # 设置窗口标题
        self.setWindowTitle("Example")
        # 设置窗口图标
        self.show()


class PlotTabWidget(QTabWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.pw1 = MyPlotWidget([1, 2, 3], [3, 2, 1])
        self.addTab(self.pw1, "标签1")

        self.pw2 = MyPlotWidget([1, 2, 3], [1, 2, 1])
        self.addTab(self.pw2, "标签2")

        self.pw3 = MyPlotWidget([1, 2, 3], [3, 2, 1])
        self.addTab(self.pw3, "标签3")

        self.pw4 = MyPlotWidget([1, 2, 3], [1, 0, 1])
        self.addTab(self.pw4, "标签4")


class PreviewWidget(QWidget):
    def __init__(self, parent=None, plot_tab_widget=None) -> None:
        super().__init__(parent)

        self.plot_tab_widget = plot_tab_widget
        r2a = pg.PolyLineROI([[0, 0], [0, 3], [3, 3], [3, 0]], closed=True)
        pw = pg.PlotWidget()
        # x, y = self.plot_tab_widget.pw1.curve.getData()
        # self.pw1 = MyPlotWidget(x, y)

        # x, y = self.plot_tab_widget.pw2.curve.getData()
        # self.pw2 = MyPlotWidget(x, y)

        # x, y = self.plot_tab_widget.pw3.curve.getData()
        # self.pw3 = MyPlotWidget(x, y)

        # x, y = self.plot_tab_widget.pw4.curve.getData()
        # self.pw4 = MyPlotWidget(x, y)

        # layout = QHBoxLayout()
        # layout.addWidget(self.pw1)
        # layout.addWidget(self.pw2)
        # layout.addWidget(self.pw3)
        # layout.addWidget(self.pw4)

        # self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
