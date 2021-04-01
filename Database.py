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
        self.appCursor.execute("CREATE TABLE IF NOT EXISTS `ecodb1`.`complaints` ( `complaint_number` INT(10) NOT NULL , `bank_name` VARCHAR(100) NOT NULL , `branch_address` VARCHAR(100) NOT NULL , `bank_zone` VARCHAR(15) NOT NULL , `complaint_date` DATE NOT NULL , PRIMARY KEY (`complaint_number`));")
        self.appCursor.execute("CREATE TABLE IF NOT EXISTS `ecodb1`.`quotations` ( `complaint_number` INT(10) NOT NULL , `quotation_id` INT(10) NOT NULL , `services_amount` FLOAT(10,2) NOT NULL,`tax` FLOAT(10,2) NOT NULL ,`reimbursement_charges` FLOAT(10,2) NOT NULL , `total_amount` FLOAT(10,2) NOT NULL ,  `quotation_date` DATE NOT NULL,`is_done` BOOLEAN NOT NULL DEFAULT FALSE,PRIMARY KEY (`quotation_id`) ) ;")
        self.appCursor.execute("CREATE TABLE IF NOT EXISTS `ecodb1`.`services` ( `service_id` VARCHAR(32) NOT NULL , `quotation_id` INT(10) NOT NULL , `service_description` VARCHAR(150) NOT NULL , `service_rate` FLOAT(10,2) NOT NULL , `service_qty` FLOAT(10,2) NOT NULL , `service_amount` FLOAT(10,2) NOT NULL , PRIMARY KEY (`service_id`));")
        self.appCursor.execute(
            "CREATE TABLE IF NOT EXISTS `ecodb1`.`bills` ( `invoice_id` VARCHAR(20) NOT NULL , `quotation_id` INT(10) NOT NULL , `job_completion_date` DATE NULL,PRIMARY KEY (`invoice_id`) ) ;")

    def getAllServices(self) -> list:
        self.appCursor.execute(
            "SELECT service_description from ecodb.services_details")
        services_list = []
        for row in self.appCursor:
            services_list.append(row[0])
        return services_list

    def getServiceRate(self, serice_description) -> float:
        self.appCursor.execute(
            "SELECT service_rate FROM ecodb.services_details WHERE service_description=%s", (serice_description,))

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
        #     "INSERT INTO  `ecodb1`.`complaints` (`complaint_number`, `bank_name`, `branch_address`, `bank_zone`, `complaint_date`) VALUES (%s,%s,%s,%s,%s)", l
        # )
        self.appCursor.execute(
            "INSERT INTO  `ecodb1`.`complaints` (`complaint_number`, `bank_name`, `branch_address`, `bank_zone`, `complaint_date`) VALUES (%s,%s,%s,%s,STR_TO_DATE(%s,'%d/%b/%Y'))",
            (complaint.getComplainNo(), complaint.getBankName(),
             complaint.getAddress(), complaint.getZone(), complaint.getDate(),))
        self.appDatabase.commit()

    def addQuotation(self, bill: Bill):
        totalServiceAmount = 0
        for service in bill.getServices().getServicesList():
            totalServiceAmount = totalServiceAmount+service["amount"]

        extra_charges = bill.getAdditionalCharges().getPersonQty() * \
            bill.getAdditionalCharges().getPerPersonRate()
        totalAmount = totalServiceAmount + \
            (totalServiceAmount*0.16)+extra_charges
        self.appCursor.execute(
            "INSERT INTO `ecodb1`.`quotations` (`complaint_number`, `quotation_id`, `services_amount`, `tax`,`reimbursement_charges`, `total_amount`, `quotation_date`) VALUES (%s,%s,%s,%s,%s,%s,STR_TO_DATE(%s,'%d/%b/%Y'))",
            (bill.getComplainInfo().getComplainNo(), bill.getComplainInfo().getComplainNo(), totalServiceAmount, totalServiceAmount*0.16, extra_charges, totalAmount,  bill.getComplainInfo().getDate(),))
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
            "SELECT count(complaint_number) from ecodb1.quotations where is_done=0")
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

    def fetchNotDoneQuotations(self) -> list:
        self.appCursor.execute(
            "SELECT c.complaint_number, c.bank_zone , c.branch_address ,q.quotation_date ,q.total_amount,c.bank_name from ecodb1.complaints c join ecodb1.quotations q on c.complaint_number = q.complaint_number where q.is_done=0")
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

    def updateInvoiceId(self, oldinvoiceid, newinvoiceId: str):
        try:
            self.appCursor.execute(
                ("UPDATE ecodb1.bills set invoice_id=%s where invoice_id=%s"), (newinvoiceId, oldinvoiceid,))
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

    def getBranchAddressFromComplaintNo(self, complaintno: int) -> str:

        self.appCursor.execute(
            "SELECT branch_address FROM ecodb1.complaints WHERE complaint_number=%s", (complaintno,))
        for row in self.appCursor:
            return row[0]

    def updateJobCompletionDate(self, comaplaitno: int, date: str):
        self.appCursor.execute(
            "update ecodb1.bills set job_completion_date=STR_TO_DATE(%s,'%d/%b/%Y') where quotation_id=%s", (date, comaplaitno,))
        self.appCursor.execute(
            "update ecodb1.quotations set is_done=1 where quotation_id=%s", (comaplaitno,))
        self.appDatabase.commit()

    def fetchDoneQuotations(self, month: str, year: str) -> list:
        self.appCursor.execute(
            "SELECT b.invoice_id ,q.complaint_number, b.job_completion_date , c.bank_zone, c.branch_address ,q.total_amount from ecodb1.complaints c join ecodb1.quotations q on c.complaint_number = q.complaint_number join ecodb1.bills b on b.quotation_id = q.quotation_id where q.is_done=1 and b.invoice_id like concat('______',%s,'-',%s)", (month, year,))
        quotationsList = []
        for row in self.appCursor:
            quotationsList.append(row)

        return quotationsList

    def fetchDoneQuotationsByZone(self, zone: str, month: str, year: str) -> list:
        self.appCursor.execute(
            "SELECT b.invoice_id ,q.complaint_number, b.job_completion_date , c.bank_zone, c.branch_address ,q.total_amount from ecodb1.complaints c join ecodb1.quotations q on c.complaint_number = q.complaint_number join ecodb1.bills b on b.quotation_id = q.quotation_id where q.is_done=1 and c.bank_zone =upper(%s) and b.invoice_id like concat('______',%s,'-',%s)", (zone, month, year,))
        quotationsList = []
        for row in self.appCursor:
            quotationsList.append(row)

        return quotationsList

    def fetchDoneQuotationsByBank(self, bank: str, month: str, year: str) -> list:
        self.appCursor.execute(
            "SELECT b.invoice_id ,q.complaint_number, b.job_completion_date , c.bank_zone, c.branch_address ,q.total_amount from ecodb1.complaints c join ecodb1.quotations q on c.complaint_number = q.complaint_number join ecodb1.bills b on b.quotation_id = q.quotation_id where q.is_done=1 and c.bank_name =upper(%s) and b.invoice_id like concat('______',%s,'-',%s)", (bank, month, year,))
        quotationsList = []
        for row in self.appCursor:
            quotationsList.append(row)

        return quotationsList

    def fetchDoneQuotationByComplaintNo(self, complaintno: int, month: str, year: str) -> list:
        self.appCursor.execute(
            "SELECT b.invoice_id ,q.complaint_number, b.job_completion_date , c.bank_zone, c.branch_address ,q.total_amount from ecodb1.complaints c join ecodb1.quotations q on c.complaint_number = q.complaint_number join ecodb1.bills b on b.quotation_id = q.quotation_id where q.is_done=1 and q.complaint_number =%s and b.invoice_id like concat('______',%s,'-',%s)", (complaintno, month, year,))
        quotationsList = []
        for row in self.appCursor:
            quotationsList.append(row)

        return quotationsList

    def getZoneMaximumInvoiceId(self, zone: str):
        print(zone[0])
        query = "SELECT invoice_id FROM `ecodb1`.`bills` WHERE invoice_id like %s ORDER by invoice_id DESC LIMIT 1"
        args = (zone[0],)
        self.appCursor.execute(
            query, (zone[0] + "%",))

        for row in self.appCursor:
            print(row)
            return row[0]

    def fetchDataForSummary(self, zone: str, month: str, year: str) -> list:
        self.appCursor.execute(
            "SELECT c.branch_address, q.complaint_number,b.invoice_id , q.services_amount,q.tax,q.reimbursement_charges,q.total_amount from ecodb1.complaints c join ecodb1.quotations q on c.complaint_number = q.complaint_number join ecodb1.bills b on b.quotation_id = q.quotation_id where q.is_done=1 and c.bank_zone =upper(%s) and b.invoice_id like concat('______',%s,'-',%s)", (zone, month, year,))
        data = []
        for row in self.appCursor:
            data.append(row)
        return data


if __name__ == "__main__":
    db = Database()
    # print(len(db.fetchQuotationsByBank('Bank al-habib')))
    # print((db.fetchDoneQuotations()))
    # print(db.getZoneMaximumInvoiceId(zone="LHR"))
    # print(db.fetchTotalRows())
    # print(db.deleteQuotation(1))
    # print(db.getInvoiceIdFromComplaintNo(1))
    # db.getdata()
    print(db.fetchDataForSummary("LHR", "04", "2021"))
