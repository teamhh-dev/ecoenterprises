from AppView import *
from ExcelModel import *
import sys


class AppController:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.initHandlers()
        self.MainWindow.show()
        sys.exit(self.app.exec_())

    def initHandlers(self):
        self.ui.pushButton_4.clicked.connect(self.showAddQuotaionTab)
        self.ui.pushButton_6.clicked.connect(self.showAddBillTab)
        self.ui.pushButton_8.clicked.connect(self.showQuotaionTab)
        self.ui.pushButton_9.clicked.connect(self.showBillTab)

    def showAddQuotaionTab(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def showAddBillTab(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def showQuotaionTab(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def showBillTab(self):
        self.ui.stackedWidget.setCurrentIndex(2)


if __name__ == "__main__":
    app = AppController()
