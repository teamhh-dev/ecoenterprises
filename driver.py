# from HomePageView import *
from ComplaintInfo import *
from Services import *
from Bill import *
from ExcelModel import *
import datetime

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = HomePageView()
#     window.show()
#     sys.exit(app.exec_())


myList = [
    {
        'description': "PCB kit Repair with aeroflex installation outdoor",
        'qty': '45rft',
        'rate': 2000,
        'amount': 20000
    },
    {
        'description': "Gas charging",
        'qty': '45rft',
        'rate': 2000,
        'amount': 23445.78
    },
    {
        'description': "Coil brazing on new Heir AC outdoor installation",
        'qty': '45rft',
        'rate': 2000,
        'amount': 234.89
    },
    {
        'description': "Gas charging",
        'qty': '45rft',
        'rate': 2000,
        'amount': 1233
    }
]


bill = Bill(ComplaintInfo("temp", str(datetime.datetime.now().strftime("%d/%b/%Y")),
                          "sample  Branch,sample Zone", "sample", 1), Services(myList))

eM = ExcelModel()

eM.addBill(bill)
