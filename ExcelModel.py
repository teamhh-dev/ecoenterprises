from openpyxl import *
import datetime
# from HomePageView import *
from copy import copy
from Bill import *
from openpyxl.styles.alignment import Alignment


class ExcelModel():
    def __init__(self):

        # all global variables
        self.workbook = None
        self.worksheet = None
        self.activeWorkSheet = None
        self.fileName = None
        self.firstRow = 0
        self.service_len = 0
        self.sr_number = 0

    #  Selecting Excel file in which data has to stored
    def selectExcelFile(self, zone: str):

        self.fileName = 'User Data/Feburary/'+zone+'.xlsx'
        self.workbook = load_workbook(filename=self.fileName)
        self.worksheet = self.workbook['template']

    # Creating worksheet
    def createWorksheet(self, name: str):

        self.activeWorkSheet = self.workbook.copy_worksheet(self.worksheet)
        self.activeWorkSheet.title = name

    # Adding Bill to Excel sheet
    def addBill(self, bill: Bill):

        self.selectExcelFile(bill.getComplainInfo().getZone())
        self.createWorksheet(bill.getComplainInfo().getInvoiceId())
        self.saveBillComlaintInfo(bill.getComplainInfo())
        self.saveBillServices(bill.getServices())
        self.workbook.save(filename=self.fileName)

    # Adding essential information about complaint in the worksheet
    def saveBillComlaintInfo(self, complainInfo: ComplaintInfo):

        self.activeWorkSheet['D2'] = complainInfo.getInvoiceId()
        self.activeWorkSheet['A7'] = complainInfo.getDate()
        self.activeWorkSheet['H7'] = complainInfo.getComplainNo()
        self.activeWorkSheet['A9'] = complainInfo.getAddress()

    # adding services rows to active worksheet , format them and then adding data in them
    def saveBillServices(self, services: Services):
        # print(services.getServicesList())
        # return
        self.firstRow = 16
        self.service_len = len(services.getServicesList())-2
        if not self.service_len == 0:
            self.activeWorkSheet.insert_rows(17, self.service_len)
        row = list(self.activeWorkSheet.rows)[15]
        i = 0
        j = self.firstRow

    # Adding service rows to active worksheet
        if not self.service_len == 0:
            while j <= self.firstRow + self.service_len:

                for cell in row:

                    list(self.activeWorkSheet.rows)[
                        j][i].border = copy(cell.border)
                    list(self.activeWorkSheet.rows)[
                        j][i].font = copy(cell.font)
                    list(self.activeWorkSheet.rows)[
                        j][i].number_format = copy(cell.number_format)
                    i = i+1
                i = 0
                j = j+1

    # Adding services to worksheet

        services.getServicesList().reverse()
        self.sr_number = 1
        for service in services.getServicesList():

            self.activeWorkSheet['A'+str(self.firstRow)] = self.sr_number
            self.activeWorkSheet['B' +
                                 str(self.firstRow)] = service['description']
            self.activeWorkSheet['E'+str(self.firstRow)] = service['qty']
            self.activeWorkSheet['G'+str(self.firstRow)] = service['rate']
            self.activeWorkSheet['H'+str(self.firstRow)] = service['amount']
            self.firstRow = self.firstRow + 1
            self.sr_number = self.sr_number + 1
    # yahan maslah hai hai jab rows do hoti hain tab formula sahih calculate nahi hota
    # Updating the formulas
        self.activeWorkSheet["H"+str(j+1)] = "=SUM(H16:H"+str(j)+")"
        self.activeWorkSheet["H" + str(j+2)] = "=H" + str(j+1)+"*0.16"
        self.activeWorkSheet["H" +
                             str(j+5)] = "=SUM(H" + str(j+1)+":H"+str(j+4)+")"

    # Calling the formatting cells function
        self.formattingCells(16)

    # Perform formatting cells
    def formattingCells(self, rowNo: int):

        while rowNo <= (self.firstRow+self.service_len)-2 or rowNo == 16 or rowNo == 17:

            self.activeWorkSheet.merge_cells('B'+str(rowNo)+':'+'D'+str(rowNo))
            self.activeWorkSheet.cell(row=rowNo, column=1).alignment = Alignment(
                horizontal='center', vertical='center', wrap_text=True)
            self.activeWorkSheet.cell(row=rowNo, column=2).alignment = Alignment(
                horizontal='left', vertical='top', wrap_text=True)
            self.activeWorkSheet.cell(row=rowNo, column=5).alignment = Alignment(
                horizontal='center', vertical='center', wrap_text=True)
            self.activeWorkSheet.cell(row=rowNo, column=7).alignment = Alignment(
                horizontal='center', vertical='center', wrap_text=True)
            self.activeWorkSheet.cell(row=rowNo, column=8).alignment = Alignment(
                horizontal='center', vertical='center', wrap_text=True)

            #  Increasing the size of height of row
            if (len(str(self.activeWorkSheet.cell(row=rowNo, column=2).value))) > 36:

                self.activeWorkSheet.row_dimensions[rowNo].height = 31.50
            # fixed
            rowNo = rowNo + 1
