import pyqtgraph as pg

class MyPlotWidget(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        curve = self.plot([1, 2, 3], [2, 1, 3], symbol="o")
        self.show()

if __name__ == "__main__":
    app = pg.mkQApp("example")
    pw = MyPlotWidget()
    pg.exec()