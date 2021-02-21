import sys

from PyQt5.QtCore import QDateTime, Qt, QtFatalMsg
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QTableWidgetSelectionRange

from AppView import *
from ExcelModel import *
from WordModel import *


class AppController:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.initHandlers()
        self.MainWindow.show()
        self.excelModel = ExcelModel()
        self.wordModel = WordModel()
        self.bill = Bill(None, Services([]))
        # self.bill = Bill(None, Services([]))
        sys.exit(self.app.exec_())

    def initHandlers(self):
        self.ui.addQuotationBtn.clicked.connect(self.showAddQuotaionTab)
        self.ui.addToBillBtn.clicked.connect(self.showAddBillTab)
        self.ui.approvalsBtn.clicked.connect(self.showApprovalsTab)
        self.ui.billsBtn.clicked.connect(self.showBillTab)
        self.ui.addLetterBtn.clicked.connect(self.showAddLetterTab)
        self.ui.addServiceBtn.clicked.connect(self.addService)
        self.ui.saveBtn.setDisabled(True)
        self.ui.finalizeBtn.clicked.connect(self.finalize)
        self.ui.deleteServiceBtn.clicked.connect(self.deleteService)
        self.ui.saveBtn.clicked.connect(self.saveBill)

    def showAddQuotaionTab(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def showAddBillTab(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def showAddLetterTab(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def showBillTab(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def showApprovalsTab(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def addService(self):
        qty = self.ui.qtySpinBox.value()
        description = self.ui.descriptionBox.text()+" "+self.ui.detailsBox.text()
        rate = float(self.ui.rateBox.text())
        amount = rate*qty
        self.ui.servicesTbl.insertRow(0)
        self.ui.servicesTbl.setItem(0, 0, QTableWidgetItem(description))
        self.ui.servicesTbl.setItem(0, 1, QTableWidgetItem(str(qty)))
        self.ui.servicesTbl.setItem(0, 2, QTableWidgetItem(str(rate)))
        self.ui.servicesTbl.setItem(0, 3, QTableWidgetItem(str(amount)))
        # print(description, ":", qty, ":", rate, ":", amount)
        service = {
            'description': description,
            'qty': str(qty),
            'rate': rate,
            'amount': amount
        }
        # self.bill.getServices().append(service)
        self.bill.getServices().getServicesList().append(service)

    def validate(self) -> bool:
        flag = True
        if(self.ui.complaintNoBox.text() == ""):
            flag = False

        return flag

    def finalize(self):
        zone = self.ui.zoneComBox.currentText()
        date = self.ui.complaintDateBox.date()
        bankAddress = self.ui.bankComBox.currentText()
        temp = "{:0>3d}".format(1)
        invoiceId = zone[0]+"B"+temp+"-" + \
            "{:0>2d}".format(
                (date.getDate()[1]))+"-"+str(date.getDate()[0])
        comaplaintNo = self.ui.complaintNoBox.text()
        branchAddress = self.ui.branchAddressBox.text()
        formattedDate = datetime.datetime(date.getDate()[0], date.getDate()[
                                          1], date.getDate()[2]).strftime("%d/%b/%Y")

        print(formattedDate, ":", invoiceId)

        complaintInfo = ComplaintInfo(
            invoiceId, formattedDate, branchAddress.upper()+","+zone+" ZONE", zone, int(comaplaintNo))
        self.bill.setComplainInfo(complaintInfo)

        if(self.validate()):
            self.ui.saveBtn.setDisabled(False)

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Invalid Data Entered")
            msg.setWindowTitle("Invalid Information")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def deleteService(self):
        self.ui.servicesTbl.removeRow(self.ui.servicesTbl.currentRow())


#  yar yeh dekho update ni ho rah text table me

    # def updateItems(self):
    #     self.ui.servicesTbl.setItem(self.ui.servicesTbl.currentRow(), self.ui.servicesTbl.currentColumn(), self.putText())

    # def putItem(self, text, flags):
    #     tableWidgetItem = QTableWidgetItem(self.ui.servicesTbl.currentItem().text())
    #     tableWidgetItem.text = self.ui.servicesTbl.cellPressed.connect(self.updateText)
    #     return tableWidgetItem

    # def updateText(self):
    #     self.ui.servicesTbl.

    def saveBill(self):
        if(self.validate()):
            self.ui.saveBtn.setDisabled(True)
            print(self.bill.getComplainInfo())
            # print(self.bill.getServices().getServicesList())
            self.excelModel.addBill(
                Bill(self.bill.getComplainInfo(), self.bill.getServices()))

            self.wordModel.addBill(
                Bill(self.bill.getComplainInfo(), self.bill.getServices()))

            # self.excelModel.addBill(
            #     Bill(self.bill.getComplainInfo(), self.bill.getServices().getServicesList()))
            # self.excelModel.addBill(self.bill)

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Invalid Data Entered")
            msg.setWindowTitle("Invalid Information")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()


if __name__ == "__main__":
    app = AppController()
