# from __future__ import print_function
from mailmerge import MailMerge
from datetime import date
import os

template = "quatation.docx"

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
    'sr_num': '1', 'qty': '10', 'amount': '1000', 'description': 'a black little boy have ajump on to the road to avoid car. He knows the value of life', 'rate': '200'}

for _ in range(10):
    services_list.append(services)
document.merge_rows('sr_num', services_list)
document.write('test-output.docx')
print(os.name)
# filename = 'test-output1.docx'

# open (filename , "r")
# os.startfile(filename, "print")
