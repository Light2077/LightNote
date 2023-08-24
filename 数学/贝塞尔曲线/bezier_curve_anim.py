import pyqtgraph as pg
import numpy as np
from PyQt5.QtCore import Qt, QTimer


def update_curve():
    global t

    point1 = target1.pos()
    point2 = target2.pos()
    point3 = control_point.pos()

    curve1.setData([point1.x(), point3.x()], [point1.y(), point3.y()])
    curve2.setData([point2.x(), point3.x()], [point2.y(), point3.y()])

    t_vals = np.linspace(0, 1, 100)
    bezier_x = [
        bezier_curve(t_val, point1.x(), point3.x(), point2.x()) for t_val in t_vals
    ]
    bezier_y = [
        bezier_curve(t_val, point1.y(), point3.y(), point2.y()) for t_val in t_vals
    ]
    bezier_curve_plot.setData(bezier_x, bezier_y)
    # 可视化绿线
    x1 = bezier_curve_1(t, point1.x(), point3.x())
    y1 = bezier_curve_1(t, point1.y(), point3.y())
    x2 = bezier_curve_1(t, point3.x(), point2.x())
    y2 = bezier_curve_1(t, point3.y(), point2.y())

    curve3.setData([x1, x2], [y1, y2])
    # Update moving point's position
    bx = bezier_curve(t, point1.x(), point3.x(), point2.x())
    by = bezier_curve(t, point1.y(), point3.y(), point2.y())
    moving_point.setPos(bx, by)


def update_time():
    global t
    t += 0.01  # Increment t value
    if t > 1:
        t = 0  # Reset t value when it exceeds 1
    update_curve()


def bezier_curve(t, P0, P1, P2):
    return (1 - t) ** 2 * P0 + 2 * (1 - t) * t * P1 + t**2 * P2


def bezier_curve_1(t, P0, P1):
    return (1 - t) * P0 + t * P1


app = pg.mkQApp("bezier_curve")
pw = pg.PlotWidget()

point1, point2 = (5, 5), (25, 10)
point3 = (12, 12)

target1 = pg.TargetItem(pos=point1, size=20, symbol="x", pen="#F4511E")
target2 = pg.TargetItem(pos=point2, size=20, symbol="x", pen="#F4511E")
control_point = pg.TargetItem(pos=point3, size=20, symbol="t1")
curve1 = pw.plot(pen={"style": Qt.DashLine})
curve2 = pw.plot(pen={"style": Qt.DashLine})
bezier_curve_plot = pw.plot(pen={"width": 3})


# 可视化绿色的线
curve3 = pw.plot(pen={"color": "green", "width": 3})

# Create a moving point
moving_point = pg.TargetItem(
    point1,
    symbol="o",
    movable=False,
    size=10,
)
pw.addItem(moving_point)
pw.addItem(target1)
pw.addItem(target2)
pw.addItem(control_point)

target1.sigPositionChanged.connect(update_curve)
target2.sigPositionChanged.connect(update_curve)
control_point.sigPositionChanged.connect(update_curve)

t = 0  # Initialize t value

# Create a QTimer to update the moving point's position
timer = QTimer()
timer.timeout.connect(update_time)
timer.start(20)  # Update every 20ms, which gives 2 seconds for a full cycle

update_curve()
pw.setXRange(0, 30)
pw.setYRange(0, 20)
pw.show()

if __name__ == "__main__":
    pg.exec()
