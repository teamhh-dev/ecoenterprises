from Letters import *
from datetime import date
import os
from Bill import *
from mailmerge import MailMerge
import datetime
from docx2pdf import convert


class LetterModel:
    def __init__(self):
        self.templateFile = "AppData/Templates/Letter.docx"
        self.document = MailMerge(self.templateFile)
        self.toFileName = "User Data/"

    def saveLetterInfo(self, letter: Letters):
        date = datetime.datetime.today().strftime("%d/%b/%Y")
        self.document.merge(
            date=date, bank_name=letter.getBankName(), branch_address=letter.getAddress(),
            inv_id=str(letter.getComplaintNo()), subject_line=letter.getSubjectLine(),
            body=letter.getLetterContent())
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%B")
        # saveFilePath = self.toFileName+month+"_"+year+"/"+"LETTERS AND REPORTS/"+
        saveFilePath = self.toFileName+month+"_"+year+"/"+"LETTERS AND REPORTS/" + \
            str(letter.getComplaintNo())+" " + \
            letter.getAddress()+" Branch, "+letter.getZone()+" Zone."
        self.saveToFile(saveFilePath)

    def saveToFile(self, fileName: str):
        print(fileName)

        self.document.write(fileName+".docx")
        self.templateFile = "AppData/Templates/Letter.docx"
        self.document = MailMerge(self.templateFile)
        self.toFileName = "User Data/"
        convert(fileName+".docx")
        os.remove(fileName+".docx")


if __name__ == "__main__":
    test = LetterModel()
