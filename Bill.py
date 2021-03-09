from AdditionalCharges import AdditionalCharges
from ComplaintInfo import *
from Services import *


class Bill():

    def __init__(self, complaintInfo: ComplaintInfo, services: Services, additionalCharges: AdditionalCharges):
        self.complaintInfo = complaintInfo
        self.services = services
        self.additionalCharges = additionalCharges

    def getComplainInfo(self):
        return self.complaintInfo

    def getServices(self):
        return self.services

    def getAdditionalCharges(self):
        return self.additionalCharges

    def setComplainInfo(self, complaintInfo: ComplaintInfo):
        self.complaintInfo = complaintInfo

    def setServices(self, services: Services):
        self.services = services

    def setAdditionalCharges(self, additionalCharges: AdditionalCharges):
        self.additionalCharges = additionalCharges
