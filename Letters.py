

class Letters:
    def __init__(self, subjectLine: str, letterContent: str, complaintNo: int, address: str, zone: str, bankName: str):
        self.subjectLine = subjectLine
        self.letterContent = letterContent
        self.complaintNo = complaintNo
        self.address = address
        self.zone = zone
        self.bankName = bankName

    def setSubjectLine(self, subjectLine: str):
        self.subjectLine = subjectLine

    def setLetterContent(self, letterContent: str):
        self.letterContent = letterContent

    def setComplaintNo(self, complaintNo: int):
        self.complaintNo = complaintNo

    def setAddress(self, address: str):
        self.address = address

    def setZone(self, zone: str):
        self.zone = zone

    def setBankName(self, bankName: str):
        self.bankName = bankName

    def getSubjectLine(self):
        return self.subjectLine

    def getLetterContent(self):
        return self.letterContent

    def getComplaintNo(self):
        return self.complaintNo

    def getAddress(self):
        return self.address

    def getZone(self):
        return self.zone

    def getBankName(self):
        return self.bankName
