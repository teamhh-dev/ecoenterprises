# from __future__ import print_function

from datetime import date
import os
from Bill import *
from mailmerge import MailMerge


class WordModel:
    def __init__(self):
        self.templateFile = "User Data/quatation.docx"
        self.document = MailMerge(self.templateFile)
        self.toFileName = "User Data/Feburary/"

    def addBill(self, bill: Bill):
        self.saveBillComlaintInfo(bill.getComplainInfo())
        self.saveBillServices(bill.getServices())

        self.saveToFile(
            self.toFileName+bill.getComplainInfo().getZone()+"/"+bill.getComplainInfo().getInvoiceId())

    def saveBillComlaintInfo(self, complainInfo: ComplaintInfo):
        self.document.merge(
            date=complainInfo.getDate(), branch_address=complainInfo.getAddress(), inv_id=str(complainInfo.getComplainNo()))

    def saveBillServices(self, services: Services):
        services_list = []
        dictionary = {'sr_num': 1, 'qty': '10', 'amount': '1000',
                      'description': 'pcb kit repair aeroflex isulation', 'rate': '200'}
        for service in services.getServicesList():

            service['rate'] = str(service['rate'])
            service['amount'] = str(service['amount'])
        # for service in services.getServicesList():

        #     service['rate'] = str(service['rate'])
        #     service['amount'] = str(service['amount'])

        #     dictionary['qty'] = service['qty']
        #     dictionary['rate'] = service['rate']
        #     dictionary['description'] = service['descriptio']
        #     dictionary['qty'] = service['qty']
        print(services.getServicesList())
        self.document.merge_rows(
            'description', list(services.getServicesList()))

    def saveToFile(self, fileName: str):
        print(fileName)
        self.document.write(fileName+".docx")

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
