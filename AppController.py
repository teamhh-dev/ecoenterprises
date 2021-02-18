from ExcelModel import *

from gui import *
import sys


class AppController:
    def __init__(self):
        self.Application = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.initButtonHandlers()

        self.MainWindow.show()

        sys.exit(self.Application.exec_())

    def initButtonHandlers(self):
        self.ui.pushButton.clicked.connect(self.showTab1)
        self.ui.pushButton_2.clicked.connect(self.showTab2)
        self.ui.pushButton_3.clicked.connect(self.showTab3)
        self.ui.pushButton_4.clicked.connect(self.showTab4)

    def showTab1(self):
        self.ui.tabWidget.setCurrentIndex(0)

    def showTab2(self):
        self.ui.tabWidget.setCurrentIndex(1)

    def showTab3(self):
        self.ui.tabWidget.setCurrentIndex(2)

    def showTab4(self):
        self.ui.tabWidget.setCurrentIndex(3)


if __name__ == "__main__":

    App = AppController()
