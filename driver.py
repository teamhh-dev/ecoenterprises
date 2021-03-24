# from HomePageView import *
from ComplaintInfo import *
from Services import *
from Bill import *
from ExcelModel import *
import datetime
from WordModel import *
from Database import *
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = HomePageView()
#     window.show()
#     sys.exit(app.exec_())


myList = [
    {
        'description': "PCB kit Repair with aeroflex installation outdoor",
        'qty': 45,
        'rate': 2000,
        'amount': 20000
    },
    {
        'description': "Gas charging",
        'qty': 45,
        'rate': 2000,
        'amount': 23445.78
    }
    # {
    #     'description': "Coil brazing on new Heir AC outdoor installation",
    #     'qty': '45rft',
    #     'rate': 2000,
    #     'amount': 234.89
    # },
    # {
    #     'description': "Gas charging",
    #     'qty': '45rft',
    #     'rate': 2000,
    #     'amount': 1233
    # }
]


bill = Bill(ComplaintInfo("test", str(datetime.datetime.now().strftime("%d/%b/%Y")), "BKL",
                          "sample  Branch,sample Zone", "LHR", 8), Services(myList), AdditionalCharges("Visit", 12, 780))

eM = ExcelModel()

# eM.addBill(bill)

# wM = WordModel()
# wM.addBill(bill)
eM.addToSummary()
# db = Database()
# db.insertData(bill)
# print(db.getInvoiceId("FSD"))
