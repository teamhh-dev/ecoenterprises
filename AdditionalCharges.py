class AdditionalCharges:
    def __init__(self, type: str, personQty: int, perPersonRate: int):
        self.type = type
        self.personQty = personQty
        self.perPersonRate = perPersonRate

    def getType(self):
        return self.type

    def getPersonQty(self):
        return self.personQty

    def getPerPersonRate(self):
        return self.perPersonRate

    def setType(self, type: str):
        self.type = type

    def setPersonQty(self, personQty: int):
        self.personQty = personQty

    def setPerPersonRate(self, perPersonRate: int):
        self.perPersonRate = perPersonRate
