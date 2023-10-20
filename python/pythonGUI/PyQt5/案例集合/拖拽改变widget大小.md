首先要定义各个区域的框

```python
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRectF, QPointF, QRect, QPoint
from PyQt5.QtWidgets import (
    QApplication, QPushButton, QMainWindow, QLabel
)
from PyQt5 import QtCore

handleTopLeft = 0
handleTopMiddle = 1
handleTopRight = 2
handleMiddleLeft = 3
handleMiddleRight = 4
handleBottomLeft = 5
handleBottomMiddle = 6
handleBottomRight = 7
handleMiddle = 8

handleSize = +8.0
handleSpace = -4.0

handleCursors = {
    handleTopLeft: Qt.SizeFDiagCursor,
    handleTopMiddle: Qt.SizeVerCursor,
    handleTopRight: Qt.SizeBDiagCursor,
    handleMiddleLeft: Qt.SizeHorCursor,
    handleMiddleRight: Qt.SizeHorCursor,
    handleBottomLeft: Qt.SizeBDiagCursor,
    handleBottomMiddle: Qt.SizeVerCursor,
    handleBottomRight: Qt.SizeFDiagCursor,
    handleMiddle: Qt.ArrowCursor,
}

class HandleLabel(QLabel):
    # def __init__(self, parent, handle_id, left, top, width, height):
    def __init__(self, parent, label, handle_id):
        super().__init__(parent)
        self.parent: QMainWindow = parent
        self.label: QLabel = label
        self.handle_id = handle_id
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setStyleSheet(
            'border-width: 1px;' \
            'border-style: solid;' \
            'border-color: rgb(255, 0, 0);' \
            'background-color: rgba(255, 0, 0, 0.2);'
        )
        # self.setGeometry(left, top, width, height)

    def enterEvent(self, moveEvent):
        cursor = handleCursors[self.handle_id]
        self.setCursor(cursor)
        super().enterEvent(moveEvent)

    def leaveEvent(self, moveEvent):
        self.setCursor(Qt.ArrowCursor)
        super().enterEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        self.selected = True
        self.bounding_rect = self.label.geometry()
        rect = self.geometry()
        self.bx = mouseEvent.pos().x() + rect.left()
        self.by = mouseEvent.pos().y() + rect.top()

        # print(self.bounding_rect, self.bounding_rect.right())
        # self.handleSelected = self.handleAt(mouseEvent.pos())
        # if self.handleSelected:
        #     self.mousePressPos = mouseEvent.pos()
        #     self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    def mouseReleaseEvent(self, ev) -> None:
        self.selected = False
        return super().mouseReleaseEvent(ev)

    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.selected:
            self.interactiveResize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        parent_rect = self.parent.geometry()
        label_rect = self.label.geometry()
        rect = self.geometry()
        x, y = mousePos.x() + rect.left(), mousePos.y() + rect.top()
        x, y = min(parent_rect.width()-2, max(2, x)), min(parent_rect.height(), max(2, y))

        if self.handle_id in [handleMiddleRight, handleBottomRight, handleTopRight]:
            label_rect.setRight(x)
        if self.handle_id in [handleMiddleLeft, handleBottomLeft, handleTopLeft]:
            label_rect.setLeft(x)
        if self.handle_id in [handleTopMiddle, handleTopLeft, handleTopRight]:
            label_rect.setTop(y)
        if self.handle_id in [handleBottomMiddle, handleBottomLeft, handleBottomRight]:
            label_rect.setBottom(y)

        if self.handle_id == handleMiddle:
            left, top = self.bounding_rect.left(), self.bounding_rect.top()
            dx, dy = x - self.bx, y - self.by
            print(dx, dy, self.bx, self.by)
            print(left+dx, top+dy)
            self.label.move(left+dx, top+dy)
            self.label.updateHandlesPos()
            return
            # label_rect.setTopLeft(QPoint())

        self.label.setGeometry(label_rect)
        self.label.updateHandlesPos()


class MyLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.handles = {i:HandleLabel(self.parent, self, i) for i in range(9)}
        self.setFrameShape(QtWidgets.QFrame.Box)
        # label.setStyleSheet("background-color:rgba(255,255,255,0.1)")
        self.setStyleSheet(
            'border-width: 2px;' \
            'border-style: solid;' \
            'border-color: rgb(0, 0, 0);' \
            'background-color: rgba(255, 255, 255, 1);'
        )
        # self.setAcceptHoverEvents(True)

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = min(10, int(min(self.width()+5, self.height()+5) * 0.3))
        mwidth = self.width() - s * 2 + 4
        mheight = self.height() - s * 2 + 4
        rect = self.geometry()
        left, top = rect.left() - 2, rect.top() - 2

        self.handles[handleTopLeft].setGeometry(
            left, top, s, s
        )
        self.handles[handleTopMiddle].setGeometry(
            left + s, top, mwidth, s
        )
        self.handles[handleTopRight].setGeometry(
            left + s + mwidth, top, s, s
        )
        self.handles[handleMiddleLeft].setGeometry(
            left, top + s, s, mheight
        )
        self.handles[handleMiddleRight].setGeometry(
            left + s + mwidth, top + s, s, mheight
        )
        self.handles[handleBottomLeft].setGeometry(
            left, top + mheight + s, s, s
        )
        self.handles[handleBottomMiddle].setGeometry(
            left + s, top + mheight + s, mwidth, s
        )
        self.handles[handleBottomRight].setGeometry(
            left + s + mwidth, top + mheight + s, s, s
        )
        self.handles[handleMiddle].setGeometry(
            left + s, top + s, mwidth, mheight
        )


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.init_ui()

    def init_ui(self):
        label = MyLabel(self)
        label.move(50, 50)
        label.resize(200, 200)
        label.updateHandlesPos()

        self.setGeometry(600, 300, 1000, 800)
        self.setWindowTitle('demo')
        self.show()

def main():
    app = QApplication(sys.argv)
    w = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```



对于一个Label，给这个label加上了几个隐藏的小方块。

鼠标放到这些区域的时候，就可以拖拽改变Label的大小。

核心就是记录鼠标的 x y坐标，判断该坐标与原坐标的差值即可。

要注意的是，鼠标事件中，获得的坐标是相对该widget而言的。还需要把这个坐标还原回大布局的坐标。