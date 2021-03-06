# from __future__ import print_function

from datetime import date
import os
from Bill import *
from mailmerge import MailMerge
import datetime


class WordModel:
    def __init__(self):
        self.templateFile = "AppData/Templates/Word.docx"
        self.document = MailMerge(self.templateFile)
        self.toFileName = "User Data/"

    def addBill(self, bill: Bill):
        self.saveBillComlaintInfo(bill.getComplainInfo())
        self.saveBillServices(bill.getServices())
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%B")
        self.saveToFile(
            self.toFileName+month+"_"+year+"/"+"PDF "+month.upper()[0:3]+" "+bill.getComplainInfo().getZone()+"/"+bill.getComplainInfo().getInvoiceId())

    def saveBillComlaintInfo(self, complainInfo: ComplaintInfo):
        self.document.merge(
            date=complainInfo.getDate(), bank_name=complainInfo.getBankName(), branch_address=complainInfo.getAddress(), inv_id=str(complainInfo.getComplainNo()))

    def saveBillServices(self, services: Services):

        for service in services.getServicesList():

            service['qty'] = str(service['qty'])
            service['rate'] = str(service['rate'])
            service['amount'] = str(service['amount'])

        self.document.merge_rows(
            'description', list(services.getServicesList()))

    def saveToFile(self, fileName: str):
        print(fileName)

        self.document.write(fileName+".docx")
        self.templateFile = "User Data/quotation.docx"
        self.document = MailMerge(self.templateFile)
        self.toFileName = "User Data/"

# template = "Invoice.docx"

# document = MailMerge(template)
# # print(document.get_merge_fields())
# converting_list = list(document.get_merge_fields())
# print(converting_list)


# document.merge(inv_id='LB001-01-2021', date='01-01-2021')

# # document.write('test-output.docx')

# services_list = []

# #    {
# #     'sr_num': '2', 'qty': '10', 'amount': '1000', 'description': 'lol', 'rate': '200'

# # },
# #     {
# #     'sr_num': '3', 'qty': '123', 'amount': '1000', 'description': 'lol', 'rate': '200'


# services = {
#     'qty': '10', 'amount': '1000', 'description': 'pcb kit repair aeroflex isulation', 'rate': '200'}

# for count in range(5):
#     services_list.append(services)
# document.merge_rows('qty', services_list)
# document.write('test-output.docx')
# print(os.name)
# # filename = 'test-output1.docx'

# # open (filename , "r")
# # os.startfile(filename, "print")
