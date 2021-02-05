# from __future__ import print_function
from mailmerge import MailMerge
from datetime import date
import os

template = "Invoice.docx"

document = MailMerge(template)
# print(document.get_merge_fields())
converting_list = list(document.get_merge_fields())
print(converting_list)


document.merge(inv_id='LB001-01-2021', date='01-01-2021')

# document.write('test-output.docx')

services_list = []

#    {
#     'sr_num': '2', 'qty': '10', 'amount': '1000', 'description': 'lol', 'rate': '200'

# },
#     {
#     'sr_num': '3', 'qty': '123', 'amount': '1000', 'description': 'lol', 'rate': '200'


services = {
    'qty': '10', 'amount': '1000', 'description': 'pcb kit repair aeroflex isulation', 'rate': '200'}

for count in range(5):
    services_list.append(services)
document.merge_rows('qty', services_list)
document.write('test-output.docx')
print(os.name)
# filename = 'test-output1.docx'

# open (filename , "r")
# os.startfile(filename, "print")
