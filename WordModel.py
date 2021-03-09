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

        self.saveBillServices(bill.getServices(), bill.getAdditionalCharges())
        self.saveAdditionalCharges(bill.getAdditionalCharges())
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%B")
        self.saveToFile(
            self.toFileName+month+"_"+year+"/"+"PDF "+month.upper()[0:3]+" "+bill.getComplainInfo().getZone()+"/"+bill.getComplainInfo().getInvoiceId())

    def saveBillComlaintInfo(self, complainInfo: ComplaintInfo):
        self.document.merge(
            date=complainInfo.getDate(), bank_name=complainInfo.getBankName(), branch_address=complainInfo.getAddress(), inv_id=str(complainInfo.getComplainNo()))

    def saveBillServices(self, services: Services, additionalCharges: AdditionalCharges):
        serviceTotal = 0
        Tax = 0
        totalAmount = 0
        for service in services.getServicesList():
            serviceTotal = serviceTotal + service['amount']
            service['qty'] = str(service['qty'])
            service['rate'] = str(service['rate'])
            service['amount'] = str(service['amount'])

        Tax = serviceTotal*0.16
        chargesAmount = additionalCharges.getPersonQty(
        ) * additionalCharges.getPerPersonRate()
        totalAmount = serviceTotal + Tax + chargesAmount

        self.document.merge_rows(
            'description', list(services.getServicesList()))
        self.document.merge(servicestotal=str(serviceTotal),
                            tax=str(Tax), totalamount=str(totalAmount))

    def saveAdditionalCharges(self, additionalCharges: AdditionalCharges):
        chargesAmount = additionalCharges.getPersonQty(
        ) * additionalCharges.getPerPersonRate()
        self.document.merge(type=additionalCharges.getType() + " Charges", chargesqty=str(additionalCharges.getPersonQty()),
                            chargesrate=str(additionalCharges.getPerPersonRate()), chargesamount=str(chargesAmount))

    def saveToFile(self, fileName: str):
        print(fileName)

        self.document.write(fileName+".docx")
        self.templateFile = "AppData/Templates/Word.docx"
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
