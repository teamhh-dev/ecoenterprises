import mysql.connector


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
        self.appCursor.execute("create database if not exists ecodb")
        # self.appCursor.execute(
        #     "CREATE TABLE if not exists `ecodb`.`comaplaints` ( `Compalint_No` INT(5) NOT NULL , `Bank_ID` VARCHAR(10) NOT NULL , `Complaint_IssueDate` DATE NOT NULL , PRIMARY KEY (`Compalint_No`));")
        self.appCursor.execute("CREATE TABLE if not exists `ecodb`.`complaints` ( `invoice_id` VARCHAR(15) NOT NULL ,  `date` DATE NOT NULL ,  `branch_address` VARCHAR(50) NOT NULL ,  `zone` VARCHAR(10) NOT NULL ,  `complaint_no` INT(10) NOT NULL ,    PRIMARY KEY  (`invoice_id`));")
        self.appCursor.execute(
            "CREATE TABLE if not exists `ecodb`.`banks` ( `Bank_ID` VARCHAR(10) NOT NULL , `Branch_code` INT(10) NOT NULL , `Zone` VARCHAR(10) NOT NULL , `Bank_Name` VARCHAR(50) NOT NULL , `Bank_Location` VARCHAR(50) NOT NULL , PRIMARY KEY (`Bank_ID`));")
        self.appCursor.execute(
            "CREATE TABLE if not exists `ecodb`.`services_details` ( `Service_ID` INT NOT NULL , `Service_Description` VARCHAR(100) NOT NULL , `Service_Rate` INT(10) NOT NULL , PRIMARY KEY (`Service_ID`));")
        self.appCursor.execute(
            "CREATE TABLE if not exists `ecodb`.`quotations` ( `date_of_visit` DATE NOT NULL , `visit_charges` INT(100) NOT NULL DEFAULT '780' , `complaint_no` VARCHAR(30) NOT NULL , `total_price` INT(100) NOT NULL , PRIMARY KEY (`complaint_no`));")

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
    # def getdata(self):
    #     self.dbCursor.execute("select * from ins.students")
    #     for row in self.dbCursor:
    #         print(row[0])


if __name__ == "__main__":
    db = Database()
    print(db.getServiceRate('Monthly general Servicing (upto to 2 Ton)'))
    # db.getdata()
