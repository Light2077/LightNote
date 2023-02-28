import sys
from PyQt5.QtWidgets import QWidget, QApplication, QDateTimeEdit, QVBoxLayout
from PyQt5.QtCore import QDateTime

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.datetime_edit = QDateTimeEdit(QDateTime.currentDateTimeUtc())
        self.datetime_edit.setCalendarPopup(True)
        self.datetime_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        vbox = QVBoxLayout()
        vbox.addWidget(self.datetime_edit)
        self.setLayout(vbox)
        # self.setGeometry(300, 300, 350, 250)
        # self.setWindowTitle('Main window')

        self.datetime_edit.dateTimeChanged.connect(self.show_dt)
        self.show()
    def show_dt(self, event):
        print(type(event))  # PyQt5.QtCore.QDateTime
        print(event)  # PyQt5.QtCore.QDateTime'
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
 