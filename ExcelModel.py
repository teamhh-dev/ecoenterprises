from openpyxl import *
import datetime
# from XlsxWriter import *
# from HomePageView import *
from copy import copy

from openpyxl.styles.alignment import Alignment

workbook = load_workbook(filename='sample.xlsx')
ws = workbook["testing"]
# Data can be assigned directly to cells

# ws['B16'] = "hello"
# ws['A7'] = datetime.datetime.now()

# ws['A9'] = 'obj.address'
# cells = ws['A1': 'H28']
# contentList = []
# for i in range(26):
#     for j in range(7):
#             contentList.append(cells[i][j].value)
# i=0
# while i<len(contentList):
#     if contentList[i] is not None:
#         print(contentList[i])

#     i=i+1
# ws2 = workbook.copy_worksheet(ws)
# wsTitle = ws.title
# ws2.title = wsTitle+"2"
# # print(workbook.active)

data = {"D2": "lB01-01-2021", "A7": datetime.datetime.now(), "H7": 112022, "A9": "PECO ROAD BRANCH, LHR ZONE",
        "B16": "System flushing", "B17": "Gas charging",
        "B18": "PCB kit repair aeroflex outdoor AC",
        "B19": "PCB kit repair aeroflex outdoor AC",
        "B20": "PCB kit repair aeroflex outdoor AC",
        "B21": "PCB kit repair aeroflex outdoor AC 25 ton with copper wiring"}


cell_data = list(data.items())
print(cell_data)


# to enter multiple inputs
# for value in cell_data:
#     ws[value[0]] = value[1]


# ws.insert_rows(17, 5)
# # ws.delete_rows(17,5)
# ws.merge_cells('B16:D16')
# ws.cell(row=16, column=2).alignment = Alignment(
#     horizontal='left', vertical='top', wrap_text=True)
row = list(ws.rows)[15]
# row2 = list(ws.rows)[16]

# i = 0
# j = 17
# while j <= 20:
#     for cell in row:
#         list(ws.rows)[j][i].border = copy(cell.border)
#         # list(ws.rows)[j][i].alignment = copy(cell.alignment)
#         i = i+1

#     i = 0
#     j = j+1
j = 19
ws["H"+str(j+2)] = "=SUM(H16:H"+str(j+1)+")"
ws["H" + str(j+3)] = "=H" + str(j+2)+"*0.16"
ws["H" + str(j+6)] = "=SUM(H" + str(j+2)+":H"+str(j+5)+")"
# cell2.value = cell1.value
# cell2.border = cell1.border
# cell2.alignment = cell1.alignment

print(len(ws.cell(row=16, column=2).value))
print(type(ws.cell(row=16, column=2).value))


def formattingCells(x: int):
    while x <= 20:
        ws.merge_cells('B'+str(x)+':'+'D'+str(x))
        ws.cell(row=x, column=2).alignment = Alignment(
            horizontal='left', vertical='top', wrap_text=True)

        if (len(ws.cell(row=x, column=2).value)) > 36:
            ws.row_dimensions[x].height = 31.50

        x = x+1


# formattingCells(16)
workbook.save(filename="sample.xlsx")


# class ExcelModel():
#     def __init__(self):
#         self.workbook = load_workbook(filename='sample.xlsx')
#         self.worksheet = self.workbook.active

#     def SaveDataInExcel(self, address: str):
#         self.worksheet['A9'] = address
#         self.worksheet['A7'] = datetime.datetime.now()
#         self.workbook.save(filename="sample.xlsx")
