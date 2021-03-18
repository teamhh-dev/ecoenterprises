from Letters import Letters
from datetime import date
import os
from Bill import *
from mailmerge import MailMerge
import datetime


class LetterModel:
    def __init__(self):
        self.templateFile = "AppData/Templates/Letter.docx"
        self.document = MailMerge(self.templateFile)
        self.toFileName = "User Data/"

    def saveLetterInfo(self, letter: Letters):
        date = datetime.datetime.today().strftime("%d/%b/%Y")
        self.document.merge(
            date=date, bank_name=letter.getBankName(), branch_address=letter.getAddress(),
            inv_id=str(letter.getComplainNo()), subject_line=letter.getSubjectLine(),
            body=letter.getLetterContent())

        self.saveToFile(str(letter.getComplaintNo()))

    def saveToFile(self, fileName: str):
        print(fileName)

        self.document.write(fileName+".docx")
        self.templateFile = "User Data/Letter.docx"
        self.document = MailMerge(self.templateFile)
        self.toFileName = "User Data/"
        pass


if __name__ == "__main__":
    test = LetterModel()
    print(test.saveLetterInfo())
