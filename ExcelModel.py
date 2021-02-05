from openpyxl import *
import datetime
from Xlsxwriter import *

# from HomePageView import *
# workbook = load_workbook(filename='sample.xlsx')
# ws = workbook["Sheet1"]
# Data can be assigned directly to cells

ws['B16'] = "helllllllllllll"
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
        "B16": "System flushing", "B17": "Gas charging",  "B20": "visit charges", "H16": 1101.92, "H17": 4996.84}


# cell_data = list(data.items())
# print(cell_data)

# # to enter multiple inputs
# for value in cell_data:
#         ws[value[0]] = value[1]

ws.insert_rows(17, 3)


workbook.save(filename="sample.xlsx")


# class ExcelModel():
#     def __init__(self):
#         self.workbook = load_workbook(filename='sample.xlsx')
#         self.worksheet = self.workbook.active

#     def SaveDataInExcel(self, address: str):
#         self.worksheet['A9'] = address
#         self.worksheet['A7'] = datetime.datetime.now()
#         self.workbook.save(filename="sample.xlsx")
