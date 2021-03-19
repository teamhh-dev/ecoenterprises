import mysql.connector
from Bill import *


class Database:
    def __init__(self):
        self.appDatabase = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        self.appCursor = self.appDatabase.cursor()
        self.initDatabase()

    def initDatabase(self):
        self.appCursor.execute("create database if not exists ecodb1")
        # self.appCursor.execute(
        #     "CREATE TABLE if not exists `ecodb`.`comaplaints` ( `Compalint_No` INT(5) NOT NULL , `Bank_ID` VARCHAR(10) NOT NULL , `Complaint_IssueDate` DATE NOT NULL , PRIMARY KEY (`Compalint_No`));")
        # self.appCursor.execute("CREATE TABLE if not exists `ecodb`.`complaints` ( `invoice_id` VARCHAR(15) NOT NULL ,  `date` DATE NOT NULL ,  `branch_address` VARCHAR(50) NOT NULL ,  `zone` VARCHAR(10) NOT NULL ,  `complaint_no` INT(10) NOT NULL ,    PRIMARY KEY  (`invoice_id`));")
        # self.appCursor.execute(
        #     "CREATE TABLE if not exists `ecodb`.`banks` ( `Bank_ID` VARCHAR(10) NOT NULL , `Branch_code` INT(10) NOT NULL , `Zone` VARCHAR(10) NOT NULL , `Bank_Name` VARCHAR(50) NOT NULL , `Bank_Location` VARCHAR(50) NOT NULL , PRIMARY KEY (`Bank_ID`));")
        # self.appCursor.execute(
        #     "CREATE TABLE if not exists `ecodb`.`services_details` ( `Service_ID` INT NOT NULL , `Service_Description` VARCHAR(100) NOT NULL , `Service_Rate` INT(10) NOT NULL , PRIMARY KEY (`Service_ID`));")
        # self.appCursor.execute(
        #     "CREATE TABLE if not exists `ecodb`.`quotations` ( `date_of_visit` DATE NOT NULL , `visit_charges` INT(100) NOT NULL DEFAULT '780' , `complaint_no` VARCHAR(30) NOT NULL , `total_price` INT(100) NOT NULL , PRIMARY KEY (`complaint_no`));")
        self.appCursor.execute("CREATE TABLE IF NOT EXISTS `ecodb1`.`complaints` ( `complaint_number` INT(10) NOT NULL , `bank_name` VARCHAR(100) NOT NULL , `branch_address` VARCHAR(100) NOT NULL , `bank_zone` VARCHAR(15) NOT NULL , `comaplaint_date` DATE NOT NULL , PRIMARY KEY (`complaint_number`));")
        self.appCursor.execute("CREATE TABLE IF NOT EXISTS `ecodb1`.`quotations` ( `complaint_number` INT(10) NOT NULL , `quotation_id` INT(10) NOT NULL , `reimbursement_charges` FLOAT(10,2) NOT NULL , `total_amount` FLOAT(10,2) NOT NULL , `tax` FLOAT(10,2) NOT NULL , `quotation_date` DATE NOT NULL, PRIMARY KEY (`quotation_id`) ) ;")
        self.appCursor.execute("CREATE TABLE IF NOT EXISTS `ecodb1`.`services` ( `service_id` VARCHAR(32) NOT NULL , `quotation_id` INT(10) NOT NULL , `service_description` VARCHAR(150) NOT NULL , `service_rate` FLOAT(10,2) NOT NULL , `service_qty` FLOAT(10,2) NOT NULL , `service_amount` FLOAT(10,2) NOT NULL , PRIMARY KEY (`service_id`));")
        self.appCursor.execute(
            "CREATE TABLE IF NOT EXISTS `ecodb1`.`bills` ( `invoice_id` VARCHAR(20) NOT NULL , `quotation_id` INT(10) NOT NULL , `job_completion_date` DATE NULL,PRIMARY KEY (`invoice_id`) ) ;")

    def getAllServices(self) -> list:
        self.appCursor.execute(
            "SELECT Service_Description from ecodb.services_details")
        services_list = []
        for row in self.appCursor:
            services_list.append(row[0])
        return services_list

    def getServiceRate(self, serice_description) -> float:
        self.appCursor.execute(
            "SELECT Service_Rate FROM ecodb.services_details WHERE Service_Description=%s", (serice_description,))

        for row in self.appCursor:
            return row[0]
        return 0

    def getConveyenceCharges(self) -> str:
        # yahan database sy data uthaya jae ga
        return "780"

    def insertData(self, bill: Bill):
        self.addComplaint(bill.getComplainInfo())
        self.addQuotation(bill)
        self.addServices(bill)
        self.addBill(bill)

        # def getdata(self):
        #     self.dbCursor.execute("select * from ins.students")
        #     for row in self.dbCursor:
        #         print(row[0])
        self.appDatabase.commit()

    def addComplaint(self, complaint: ComplaintInfo):
        # l = (complaint.getComplainNo(), complaint.getBankName(),
        #      complaint.getAddress(), complaint.getZone(), complaint.getDate())
        # print(
        #     "INSERT INTO  `ecodb1`.`complaints` (`complaint_number`, `bank_name`, `branch_address`, `bank_zone`, `comaplaint_date`) VALUES (%s,%s,%s,%s,%s)", l
        # )
        self.appCursor.execute(
            "INSERT INTO  `ecodb1`.`complaints` (`complaint_number`, `bank_name`, `branch_address`, `bank_zone`, `comaplaint_date`) VALUES (%s,%s,%s,%s,STR_TO_DATE(%s,'%d/%b/%Y'))",
            (complaint.getComplainNo(), complaint.getBankName(),
             complaint.getAddress(), complaint.getZone(), complaint.getDate(),))
        self.appDatabase.commit()

    def addQuotation(self, bill: Bill):
        totalServiceAmount = 0
        for service in bill.getServices().getServicesList():
            totalServiceAmount = totalServiceAmount+service["amount"]

        totalAmount = totalServiceAmount+(totalServiceAmount*0.16)+780
        self.appCursor.execute(
            "INSERT INTO `ecodb1`.`quotations` (`complaint_number`, `quotation_id`, `reimbursement_charges`, `total_amount`, `tax`, `quotation_date`) VALUES (%s,%s,%s,%s,%s,STR_TO_DATE(%s,'%d/%b/%Y'))",
            (bill.getComplainInfo().getComplainNo(), bill.getComplainInfo().getComplainNo(), 780, totalAmount, totalServiceAmount*0.16, bill.getComplainInfo().getDate(),))
        self.appDatabase.commit()

    def addServices(self, bill: Bill):
        i = 1
        for service in bill.getServices().getServicesList():
            service_id = "S"+str(i) + "-" + \
                str(bill.getComplainInfo().getComplainNo())
            i = i+1
            self.appCursor.execute("INSERT INTO `ecodb1`.`services` (`service_id`, `quotation_id`, `service_description`, `service_rate`, `service_qty`, `service_amount`) VALUES (%s,%s,%s,%s,%s,%s)",
                                   (service_id, bill.getComplainInfo().getComplainNo(), service["description"], service["rate"], service["qty"], service["amount"],))
        self.appDatabase.commit()

    def addBill(self, bill: Bill):
        self.appCursor.execute(
            "INSERT INTO `ecodb1`.`bills` (`invoice_id`, `quotation_id`) VALUES (%s,%s)", (bill.getComplainInfo().getInvoiceId(), bill.getComplainInfo().getComplainNo(),))
        self.appDatabase.commit()

    def getInvoiceId(self, zone: str) -> int:
        self.appCursor.execute(
            "SELECT count(complaint_number) from ecodb1.complaints where bank_zone=upper(%s)", (zone,))
        invoiceId = 0
        for row in self.appCursor:
            invoiceId = row[0]

        return invoiceId+1

    def fetchTotalRows(self) -> int:
        self.appCursor.execute(
            "SELECT count(c.complaint_number) from ecodb1.complaints c join ecodb1.bills b on c.complaint_number = b.quotation_id")
        for row in self.appCursor:
            return row[0]

    def fetchRowsByZone(self, zone: str) -> int:
        self.appCursor.execute(
            "SELECT count(complaint_number) from ecodb1.complaints where bank_zone=upper(%s)", (zone,))
        for row in self.appCursor:
            return row[0]

    def fetchRowsByBank(self, bank: str) -> int:
        self.appCursor.execute(
            "SELECT count(complaint_number) from ecodb1.complaints where bank_name=upper(%s)", (bank,))
        for row in self.appCursor:
            return row[0]

    def fetchRowByComplaintNo(self, complaintno: int) -> int:
        self.appCursor.execute(
            "SELECT count(complaint_number) from ecodb1.complaints where complaint_number=%s", (complaintno,))
        for row in self.appCursor:
            return row[0]

    def fetchAllQuotations(self) -> list:
        self.appCursor.execute(
            "SELECT c.complaint_number, c.bank_zone , c.branch_address ,q.quotation_date ,q.total_amount,c.bank_name from ecodb1.complaints c join ecodb1.quotations q on c.complaint_number = q.complaint_number join ecodb1.bills b on c.complaint_number = b.quotation_id")
        quotationsList = []
        for row in self.appCursor:
            quotationsList.append(row)

        return quotationsList

    def fetchQuotationsByZone(self, zone: str) -> list:
        self.appCursor.execute(
            "SELECT c.complaint_number, c.bank_zone , c.branch_address ,q.quotation_date ,q.total_amount,c.bank_name from ecodb1.complaints c join ecodb1.quotations q on c.complaint_number = q.complaint_number where c.bank_zone=upper(%s)", (zone,))
        quotationsList = []
        for row in self.appCursor:
            quotationsList.append(row)

        return quotationsList

    def fetchQuotationsByBank(self, bank: str) -> list:
        self.appCursor.execute(
            "SELECT c.complaint_number, c.bank_zone , c.branch_address ,q.quotation_date ,q.total_amount,c.bank_name from ecodb1.complaints c join ecodb1.quotations q on c.complaint_number = q.complaint_number where c.bank_name=upper(%s)", (bank,))
        quotationsList = []
        for row in self.appCursor:
            quotationsList.append(row)

        return quotationsList

    def fetchQuotationByComplaintNo(self, complaintno: int) -> list:
        self.appCursor.execute(
            "SELECT c.complaint_number, c.bank_zone , c.branch_address ,q.quotation_date ,q.total_amount,c.bank_name from ecodb1.complaints c join ecodb1.quotations q on c.complaint_number = q.complaint_number where c.complaint_number=%s", (complaintno,))
        quotationsList = []
        for row in self.appCursor:
            quotationsList.append(row)

        return quotationsList

    def deleteQuotation(self, complaintno: int):
        try:
            self.appCursor.execute(
                "DELETE FROM ecodb1.complaints WHERE complaint_number=%s", (complaintno,))
            self.appCursor.execute(
                "DELETE FROM ecodb1.bills WHERE quotation_id=%s", (complaintno,))
            self.appCursor.execute(
                "DELETE FROM ecodb1.quotations WHERE quotation_id=%s", (complaintno,))
            self.appCursor.execute(
                "DELETE FROM ecodb1.services WHERE quotation_id=%s", (complaintno,))
            self.appDatabase.commit()
        except Exception as e:
            print(e)

    def getInvoiceIdAndZoneFromComplaintNo(self, complaintno: int) -> dict:

        invoiceIDAndZone = {"invoice_id": None, "zone": None}
        self.appCursor.execute(
            "SELECT b.invoice_id from ecodb1.quotations q join ecodb1.bills b on q.quotation_id = b.quotation_id where q.complaint_number=%s", (complaintno,))
        for row in self.appCursor:
            invoiceIDAndZone["invoice_id"] = row[0]
        self.appCursor.execute(
            "select bank_zone from ecodb1.complaints where complaint_number=%s", (complaintno,))
        for row in self.appCursor:
            invoiceIDAndZone["zone"] = row[0]
        return invoiceIDAndZone

    def updateJobCompletionDate(self, comaplaitno: int, date: str):
        self.appCursor.execute(
            "update ecodb1.bills set job_completion_date=STR_TO_DATE(%s,'%d/%b/%Y') where quotation_id=%s", (date, comaplaitno,))
        self.appDatabase.commit()


if __name__ == "__main__":
    db = Database()
    # print(len(db.fetchQuotationsByBank('Bank al-habib')))
    # print(len(db.fetchAllQuotations()))
    # print(db.fetchTotalRows())
    # print(db.deleteQuotation(1))
    print(db.getInvoiceIdFromComplaintNo(1))
    # db.getdata()
