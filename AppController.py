from copy import deepcopy
import sys
from warnings import catch_warnings
import PyQt5
import datetime
import shutil

from PyQt5.QtCore import QDateTime, Qt, QtFatalMsg
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QTableWidgetSelectionRange, QCompleter, QDialog, QPushButton, QComboBox
from PyQt5.QtGui import QIcon

# from AppView import *
from GuiView import *
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
        self.MainWindow.setWindowIcon(QIcon("AppData/Images/eco_icon.ico"))
        self.initHandlers()
        self.MainWindow.show()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.excelModel = ExcelModel()
        self.wordModel = WordModel()
        self.bill = Bill(None, Services([]), None)
        #  yaha mjhy rakhni chyeh k ni btana zaror
        # self.serviceTotalValue = 0
        # self.taxValue = 0
        # self.totalAmountValue = 0

        sys.exit(self.app.exec_())

    def initHandlers(self):
        services = self.dao.getAllServices()
        completer = QCompleter(services)
        self.ui.complaintDateBox.setDate(
            self.ui.complaintDateBox.date().currentDate())
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
        self.ui.addToBillBtn.clicked.connect(self.showAllQuotations)
        # self.ui.
        self.ui.complaintNoAddToBillBox.returnPressed.connect(lambda: self.showQuotationByComplaintNo(
            self.ui.complaintNoAddToBillBox.text()))
        self.ui.zoneAddToBillComBox.currentTextChanged.connect(
            lambda: self.showQuotationsByZone(self.ui.zoneAddToBillComBox.currentText()))
        self.ui.bankAddToBillComBox.currentTextChanged.connect(
            lambda: self.showQuotationsByBank(self.ui.bankAddToBillComBox.currentText()))
        self.ui.deleteQuotationBtn.clicked.connect(self.deleteQuotation)
        self.ui.descriptionBox.setCompleter(completer)
        self.ui.descriptionBox.editingFinished.connect(self.textChanged)
        self.ui.conveyenceChargesBox.setText(self.dao.getConveyenceCharges())
        self.ui.visitTypeComBox.currentIndexChanged.connect(
            self.visitTypeChangeAction)
        self.ui.actionCreate_Files_and_Folders.triggered.connect(
            self.openFilesAndFoldersDialog)
        self.showAllQuotations()
        # # self.showQuotationsByZone(self.ui.zoneAddToBillComBox.currentText())
        # self.showQuotationByComplaintNo(144)

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

    def visitTypeChangeAction(self):
        if self.ui.visitTypeComBox.currentText() == "Visit":
            self.ui.conveyenceChargesBox.setText("780")
        else:
            self.ui.conveyenceChargesBox.setText("")

    def openFilesAndFoldersDialog(self):
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December']
        folderNameDialog = QDialog()
        folderNameDialog.setGeometry(500, 500, 300, 120)
        monthComBox = QComboBox(folderNameDialog)
        monthComBox.addItems(
            months)

        monthComBox.move(60, 50)
        okButton = QPushButton("create", folderNameDialog)
        okButton.clicked.connect(
            lambda: self.generateFilesAndFolders(folderNameDialog, monthComBox.currentText(), months.index(monthComBox.currentText())+1))

        okButton.move(150, 50)

        folderNameDialog.setWindowTitle("Select Month...")
        folderNameDialog.setWindowModality(Qt.ApplicationModal)
        folderNameDialog.exec_()

    def generateFilesAndFolders(self, dialogBox: QDialog, month: str, monthNo: str):
        # print(month)
        zones = ["LHR", "GUJ", "KPK", "FSD"]

        dialogBox.close()
        year = datetime.datetime.now().strftime("%Y")
        # print(year)
        current_directory = os.getcwd()
        parentDirectory = "User Data"
        mainFolderName = month.upper()+"_"+year

        print(mainFolderName)
        mainFolderPath = os.path.join(
            current_directory, parentDirectory, mainFolderName)
        os.mkdir(mainFolderPath)
        for zone in zones:
            subFolderName = "PDF "+month.upper()[0:3] + " "+zone
            print(subFolderName)
            subFolderPath = os.path.join(mainFolderPath, subFolderName)
            os.mkdir(subFolderPath)
            excelFileName = "Monthly Report "+zone+" " + \
                "01-"+"{:0>2d}".format(monthNo)+"-"+year
            source = "./AppData/Templates/Excel.xlsx"
            destination = "./User Data/"+mainFolderName+"/"+excelFileName+".xlsx"
            print(source, ":", destination)
            shutil.copy(source, destination)

        # mainFolderName = month.upper()[0:3]+year

    def addService(self) -> float:
        # if(self.ui.rftCheckBox.isEnabled()):
        #     qty = str(self.ui.qtySpinBox.value())+"rft"
        # else:
        qty = self.ui.qtySpinBox.value()
        if self.ui.descriptionBox.text() == "" or self.ui.rateBox.text() == "":
            return
        description = self.ui.descriptionBox.text()+" "+self.ui.detailsBox.text()

        rate = float(self.ui.rateBox.text())
        amount = rate*qty
        if(self.ui.rftCheckBox.isChecked()):

            qty = str(self.ui.qtySpinBox.value())+"rft"
        else:
            qty = self.ui.qtySpinBox.value()

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
        # Calculatin service total, tax and total amount
        # self.serviceTotalValue = self.serviceTotalValue + \
        #     float(service['amount'])

    def validate(self) -> dict:
        flag = True
        messages = []
        if(self.ui.complaintNoBox.text() == "" or not self.ui.complaintNoBox.text().isnumeric()):
            flag = False
            messages.append("Invalid complaint number")
        if(self.ui.branchAddressBox.text() == ""):
            flag = False
            messages.append("Invalid bank address")
        if(self.ui.conveyenceChargesBox.text() == "") and not self.ui.conveyenceChargesBox.text().isnumeric():
            flag = False
            messages.append("Please enter the Convenyence Charges")
        if(self.ui.chargesQtyBox.text() == "") or not self.ui.chargesQtyBox.text().isnumeric():
            flag = False
            messages.append("Please enter some charges quantity")
        # if(self.ui.descriptionBox.text() == ""):
        #     flag = False
        #     messages.append("Enter some valid service name")
        # if not (self.ui.rateBox.text().isdecimal()) and not (self.ui.rateBox.text() == ""):
        #     flag = False
        #     messages.append("Rate can not be zero ,enter value")
        # if(len(self.bill.getServices().getServicesList()) == 0):
        #     flag = False

        return {'status': flag, 'messages': messages}

    def finalize(self):
        zone = self.ui.zoneComBox.currentText()
        date = self.ui.complaintDateBox.date()
        bankAddress = self.ui.bankComBox.currentText()
        comaplaintNo = self.ui.complaintNoBox.text()
        temp = "{:0>3d}".format(int(self.dao.getInvoiceId(zone)))

        # yahan temp nahi ana yahan number change hona jo invoice id ka hoga
        invoiceId = zone[0]+"B"+temp+"-" + \
            "{:0>2d}".format(
                (date.getDate()[1]))+"-"+str(date.getDate()[0])

        branchAddress = self.ui.branchAddressBox.text()
        formattedDate = datetime.datetime(date.getDate()[0], date.getDate()[
            1], date.getDate()[2]).strftime("%d/%b/%Y")

        validation = self.validate()
        if(validation['status']):
            self.ui.saveBtn.setDisabled(False)
            self.showServiceTotalAndTaxAndTotalAmount()
            complaintInfo = ComplaintInfo(
                invoiceId, formattedDate, bankAddress, branchAddress.upper()+" Branch,"+zone+" ZONE", zone, int(comaplaintNo))
            self.bill.setComplainInfo(complaintInfo)
            self.bill.setAdditionalCharges(AdditionalCharges(
                self.ui.visitTypeComBox.currentText(), int(self.ui.chargesQtyBox.text()), int(self.ui.conveyenceChargesBox.text())))

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

    def showServiceTotalAndTaxAndTotalAmount(self):
        allTotals = self.calculatesServiceTotalAndTaxAndTotalAmount()
        # if not len(self.bill.getServices().getServicesList()) == 0:
        self.ui.ServiceTotalValueLbl.setText(
            str(round(allTotals['servicetotal'], 2)))
        self.ui.taxValueLbl.setText(str(round(allTotals['taxvalue'], 2)))
        self.ui.totalAmountValueLbl.setText(
            str(round(allTotals['totalamount'], 2)))
        # else:
        #     self.ui.ServiceTotalValueLbl.setText(
        #         str(round(allTotals['servicetotal'], 2)))
        #     self.ui.taxValueLbl.setText(str(round(allTotals['taxvalue'], 2)))
        #     self.ui.totalAmountValueLbl.setText(
        #         str(round(allTotals['totalamount'], 2)))

    def calculatesServiceTotalAndTaxAndTotalAmount(self):
        serviceTotalValue = 0
        for service in self.bill.getServices().getServicesList():
            serviceTotalValue = serviceTotalValue + service['amount']
        taxValue = serviceTotalValue * 0.16
        extraCharges = float(self.ui.chargesQtyBox.text()) * \
            float(self.ui.conveyenceChargesBox.text())
        totalAmountValue = round(
            serviceTotalValue, 2) + round(taxValue, 2) + round(extraCharges, 2)
        return {'servicetotal': serviceTotalValue, 'taxvalue': taxValue, 'totalamount': totalAmountValue}
        # print(self.taxValue, self.totalAmountValue)

    def deleteService(self):
        removeIndex = len(self.bill.getServices().getServicesList()
                          ) - self.ui.servicesTbl.currentRow()-1

        self.bill.getServices().getServicesList().pop(removeIndex)
        self.ui.servicesTbl.removeRow(self.ui.servicesTbl.currentRow())

    def saveBill(self):
        validation = self.validate()
        if(validation['status']):
            self.ui.saveBtn.setDisabled(True)
            billComplaintInfo = self.bill.getComplainInfo()
            billServices = self.bill.getServices()
            try:

                self.excelModel.addBill(
                    Bill(deepcopy(self.bill.getComplainInfo()), deepcopy(self.bill.getServices()), deepcopy(self.bill.getAdditionalCharges())))

                self.wordModel.addBill(
                    Bill(deepcopy(self.bill.getComplainInfo()), deepcopy(self.bill.getServices()), deepcopy(self.bill.getAdditionalCharges())))
                self.dao.insertData(
                    Bill(deepcopy(self.bill.getComplainInfo()), deepcopy(self.bill.getServices()), deepcopy(self.bill.getAdditionalCharges())))
                self.ui.servicesTbl.clearContents()
                self.bill.getServices().getServicesList().clear()
                self.ui.servicesTbl.setRowCount(0)
                self.clearViewContents()
            except Exception as ex:
                print(ex)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(
                    "Check Current Month Folder Exists OR Correct Comaplaint No")
                msg.setWindowTitle("Invalid Data")
                msg.setWindowIcon(QIcon("./AppData/Images/error.ico"))

                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
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

    def showAllQuotations(self):
        self.ui.quotationsTbl.clearContents()
        self.ui.quotationsTbl.model().removeRows(0, self.ui.quotationsTbl.rowCount())
        row, column = 0, 0
        for row in range(self.dao.fetchTotalRows()):
            self.ui.quotationsTbl.insertRow(row)
            for column in range(self.ui.quotationsTbl.columnCount()):
                item = self.dao.fetchAllQuotations()[row][column]
                # print(item)
                self.ui.quotationsTbl.setItem(
                    row, column, QTableWidgetItem(str(item)))

    def showQuotationsByZone(self, zone: str):
        self.ui.quotationsTbl.clearContents()
        self.ui.quotationsTbl.model().removeRows(0, self.ui.quotationsTbl.rowCount())
        row, column = 0, 0
        for row in range(self.dao.fetchRowsByZone(zone)):
            self.ui.quotationsTbl.insertRow(row)
            for column in range(self.ui.quotationsTbl.columnCount()):
                item = self.dao.fetchQuotationsByZone(zone)[row][column]
                # print(item)
                self.ui.quotationsTbl.setItem(
                    row, column, QTableWidgetItem(str(item)))

    def showQuotationsByBank(self, bank: str):
        self.ui.quotationsTbl.clearContents()
        self.ui.quotationsTbl.model().removeRows(0, self.ui.quotationsTbl.rowCount())
        row, column = 0, 0
        for row in range(self.dao.fetchRowsByBank(bank)):
            self.ui.quotationsTbl.insertRow(row)
            for column in range(self.ui.quotationsTbl.columnCount()):
                item = self.dao.fetchQuotationsByBank(bank)[row][column]
                # print(item)
                self.ui.quotationsTbl.setItem(
                    row, column, QTableWidgetItem(str(item)))
        # self.ui.bankAddToBillComBox.setCurrentText(bank)

    def showQuotationByComplaintNo(self, complaintno: int):
        self.ui.quotationsTbl.clearContents()
        self.ui.quotationsTbl.model().removeRows(0, self.ui.quotationsTbl.rowCount())
        row, column = 0, 0
        for row in range(self.dao.fetchRowByComplaintNo(complaintno)):
            self.ui.quotationsTbl.insertRow(row)
            for column in range(self.ui.quotationsTbl.columnCount()):
                item = self.dao.fetchQuotationByComplaintNo(complaintno)[
                    row][column]
                # print(item)
                self.ui.quotationsTbl.setItem(
                    row, column, QTableWidgetItem(str(item)))

    def deleteQuotation(self):
        cNo = self.ui.quotationsTbl.selectionModel().selectedRows()[0].data()
        row = self.ui.quotationsTbl.selectionModel().selectedRows()[0].row()
        print(cNo, row)
        self.dao.deleteQuotation(int(cNo))
        self.ui.quotationsTbl.removeRow(row)
        # print(
        #     type(self.ui.quotationsTbl.selectionModel().selectedRows()[0].data()))
        # print(
        #     self.ui.quotationsTbl.selectionModel().selectedRows()[0].data())
        # print(self.ui.quotationsTbl.selectionModel().selectedRows()[0].row())

    def clearViewContents(self):
        self.ui.complaintNoBox.setText("")
        self.ui.chargesQtyBox.setText("")
        self.ui.descriptionBox.setText("")
        self.ui.rateBox.setText("")
        self.ui.qtySpinBox.setValue(1)
        self.ui.branchAddressBox.setText("")
        self.ui.rftCheckBox.setChecked(False)
        self.ui.taxValueLbl.setText("")
        self.ui.totalAmountValueLbl.setText("")
        self.ui.ServiceTotalValueLbl.setText("")


if __name__ == "__main__":
    db = Database()
    app = AppController(db)
