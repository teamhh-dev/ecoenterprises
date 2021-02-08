from ComplaintInfo import *
from Services import *


class Bill():

    def __init__(self, complaintInfo: ComplaintInfo, services: Services):
        self.complaintInfo = complaintInfo
        self.services = services

    def getComplainInfo(self):
        return self.complaintInfo

    def getServices(self):
        return self.services

    def setComplainInfo(self, complaintInfo: ComplaintInfo):
        self.complaintInfo = complaintInfo

    def setServices(self, services: Services):
        self.services = services
