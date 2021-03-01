from copy import deepcopy
import sys
from warnings import catch_warnings

from PyQt5.QtCore import QDateTime, Qt, QtFatalMsg
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QTableWidgetSelectionRange, QCompleter
from PyQt5.QtGui import QIcon

from AppView import *
from ExcelModel import *
from WordModel import *
from Database import *


class AppController:
    def __init__(self, database: Database):
        self.dao = database
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.initHandlers()
        self.MainWindow.show()
        self.excelModel = ExcelModel()
        self.wordModel = WordModel()
        self.bill = Bill(None, Services([]))

        sys.exit(self.app.exec_())

    def initHandlers(self):
        services = self.dao.getAllServices()
        completer = QCompleter(services)
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
        self.ui.descriptionBox.setCompleter(completer)
        self.ui.descriptionBox.editingFinished.connect(self.textChanged)

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

    def textChanged(self):
        self.ui.rateBox.setText(str(self.dao.getServiceRate(
            self.ui.descriptionBox.text())))

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
        service = {
            'description': description,
            'qty': qty,
            'rate': rate,
            'amount': amount
        }
        self.bill.getServices().getServicesList().append(service)

    def validate(self) -> dict:
        flag = True
        messages = []
        if(self.ui.complaintNoBox.text() == ""):
            flag = False
            messages.append("Invalid complaint number")
        if(self.ui.branchAddressBox.text() == ""):
            flag = False
            messages.append("Invalid bank address")
        if(self.ui.conveyenceChargesBox.text() == ""):
            flag = False
            messages.append("Invalid conveyence charges")
        if(self.ui.chargesQtyBox.text() == ""):
            flag = False
            messages.append("Invalid charges qunatity")
        # if(len(self.bill.getServices().getServicesList()) == 0):
        #     flag = False

        return {'status': flag, 'messages': messages}

    def finalize(self):
        zone = self.ui.zoneComBox.currentText()
        date = self.ui.complaintDateBox.date()
        bankAddress = self.ui.bankComBox.currentText()
        comaplaintNo = self.ui.complaintNoBox.text()
        temp = "{:0>3d}".format(int(comaplaintNo))
        # yahan temp nahi ana yahan number change hona jo invoice id ka hoga
        invoiceId = zone[0]+"B"+temp+"-" + \
            "{:0>2d}".format(
                (date.getDate()[1]))+"-"+str(date.getDate()[0])

        branchAddress = self.ui.branchAddressBox.text()
        formattedDate = datetime.datetime(date.getDate()[0], date.getDate()[
            1], date.getDate()[2]).strftime("%d/%b/%Y")

        complaintInfo = ComplaintInfo(
            invoiceId, formattedDate, branchAddress.upper()+","+zone+" ZONE", zone, int(comaplaintNo))
        self.bill.setComplainInfo(complaintInfo)
        validation = self.validate()
        if(validation['status']):
            self.ui.saveBtn.setDisabled(False)

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Invalid Data Entered")
            msg.setWindowTitle("Invalid Data")
            msg.setWindowIcon(QIcon("./AppData/Images/error.ico"))
            detailedMessage = ""
            for message in validation['messages']:
                detailedMessage = detailedMessage+"\n"+message
            msg.setDetailedText(detailedMessage)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def deleteService(self):
        removeIndex = len(self.bill.getServices().getServicesList()
                          ) - self.ui.servicesTbl.currentRow()-1

        self.bill.getServices().getServicesList().pop(removeIndex)
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
        validation = self.validate()
        if(validation['status']):
            self.ui.saveBtn.setDisabled(True)
            billComplaintInfo = self.bill.getComplainInfo()
            billServices = self.bill.getServices()

            self.excelModel.addBill(
                Bill(deepcopy(self.bill.getComplainInfo()), deepcopy(self.bill.getServices())))

            self.wordModel.addBill(
                Bill(deepcopy(self.bill.getComplainInfo()), deepcopy(self.bill.getServices())))

            self.ui.servicesTbl.clearContents()
            self.bill.getServices().getServicesList().clear()
            self.ui.servicesTbl.setRowCount(0)

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Invalid Data Entered")
            msg.setWindowTitle("Invalid Data")
            msg.setWindowIcon(QIcon("./AppData/Images/error.ico"))
            detailedMessage = ""
            for message in validation['messages']:
                detailedMessage = detailedMessage+"\n"+message
            msg.setDetailedText(detailedMessage)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()


if __name__ == "__main__":
    db = Database()
    app = AppController(db)
