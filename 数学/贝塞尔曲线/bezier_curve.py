import pyqtgraph as pg
import numpy as np
from PyQt5.QtCore import Qt


def update_curve():
    point1 = target1.pos()
    point2 = target2.pos()
    point3 = control_point.pos()

    curve1.setData([point1.x(), point3.x()], [point1.y(), point3.y()])
    curve2.setData([point2.x(), point3.x()], [point2.y(), point3.y()])

    t_vals = np.linspace(0, 1, 100)
    bezier_x = [bezier_curve(t, point1.x(), point3.x(), point2.x()) for t in t_vals]
    bezier_y = [bezier_curve(t, point1.y(), point3.y(), point2.y()) for t in t_vals]
    bezier_curve_plot.setData(bezier_x, bezier_y)


def bezier_curve(t, P0, P1, P2):
    return (1 - t) ** 2 * P0 + 2 * (1 - t) * t * P1 + t**2 * P2


app = pg.mkQApp("bezier_curve")
pw = pg.PlotWidget()

point1, point2 = (5, 5), (25, 10)
point3 = (12, 12)

target1 = pg.TargetItem(pos=point1, size=10, symbol="x", pen="#F4511E")
target2 = pg.TargetItem(pos=point2, size=10, symbol="x", pen="#F4511E")
control_point = pg.TargetItem(pos=point3, size=10, symbol="t1")
curve1 = pw.plot(pen={"style": Qt.DashLine})
curve2 = pw.plot(pen={"style": Qt.DashLine})
bezier_curve_plot = pw.plot()

target1.sigPositionChanged.connect(update_curve)
target2.sigPositionChanged.connect(update_curve)
control_point.sigPositionChanged.connect(update_curve)

pw.addItem(target1)
pw.addItem(target2)
pw.addItem(control_point)

update_curve()
pw.setXRange(0, 30)
pw.setYRange(0, 20)
pw.show()


if __name__ == "__main__":
    pg.exec()
