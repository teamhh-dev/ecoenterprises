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
        'foo': 12,
        'bar': 14
    },
    {
        'moo': 52,
        'car': 641
    },
    {
        'doo': 6,
        'tar': 84
    }
]


bill = Bill(ComplaintInfo("LB005-02-2021", str(datetime.datetime.now().strftime("%d/%b/%Y")),
                          "Malakwal Branch,Africa Zone", "Africa", 1), Services(myList))

eM = ExcelModel()

eM.addBill(bill)
