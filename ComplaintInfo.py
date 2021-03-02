

class ComplaintInfo:
    def __init__(self, invoiceId: str, date: str, bankName: str, address: str, zone: str, complaintNo: int) -> None:
        self.invoiceId = invoiceId
        self.bankName = bankName
        self.address = address
        self.zone = zone
        self.date = date
        self.complaintNo = complaintNo

    def getInvoiceId(self):

        return self.invoiceId

    def getDate(self):
        return self.date

    def getAddress(self):
        return self.address

    def getZone(self):
        return self.zone

    def getComplainNo(self):
        return self.complaintNo

    def getBankName(self):
        return self.bankName

    def setInvoiceId(self, invoiceId: str):

        self.invoiceId = invoiceId

    def setDate(self, date: str):

        self.date = date

    def setAddress(self, address: str):
        self.address = address

    def setZone(self, zone: str):
        self.zone = zone

    def setComplainNo(self, complaintNo: int):
        self.complaintNo = complaintNo

    def setBankName(self, bankName: str):
        self.bankName = bankName
