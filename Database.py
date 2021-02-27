import mysql.connector


class Database:
    def __init__(self):
<<<<<<< HEAD
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="twitter_"
        )
        self.appCursor = self.mydb.cursor()
=======
        self.appDatabase = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        self.appCursor = self.appDatabase.cursor()
>>>>>>> a505de5579bccfd7715ad9f855441a8de58b635f
        self.initDatabase()

    def initDatabase(self):
        self.appCursor.execute("create database if not exists ecodb")
<<<<<<< HEAD
        self.appCursor.execute("CREATE TABLE `ecodb`.`complaints` ( `invoice_id` VARCHAR(15) NOT NULL ,  `date` DATE NOT NULL ,  `branch_address` VARCHAR(50) NOT NULL ,  `zone` VARCHAR(10) NOT NULL ,  `complaint_no` INT(10) NOT NULL ,    PRIMARY KEY  (`invoice_id`));")

    def getdata(self):
        self.appCursor.execute("SELECT * FROM hamzaalidatabase.customer")
        for row in self.appCursor:
            print(row)
=======
        # self.appCursor.execute(
        #     "CREATE TABLE if not exists `ecodb`.`comaplaints` ( `Compalint_No` INT(5) NOT NULL , `Bank_ID` VARCHAR(10) NOT NULL , `Complaint_IssueDate` DATE NOT NULL , PRIMARY KEY (`Compalint_No`));")
        self.appCursor.execute("CREATE TABLE if not exists `ecodb`.`complaints` ( `invoice_id` VARCHAR(15) NOT NULL ,  `date` DATE NOT NULL ,  `branch_address` VARCHAR(50) NOT NULL ,  `zone` VARCHAR(10) NOT NULL ,  `complaint_no` INT(10) NOT NULL ,    PRIMARY KEY  (`invoice_id`));")
        self.appCursor.execute(
            "CREATE TABLE if not exists `ecodb`.`banks` ( `Bank_ID` VARCHAR(10) NOT NULL , `Branch_code` INT(10) NOT NULL , `Zone` VARCHAR(10) NOT NULL , `Bank_Name` VARCHAR(50) NOT NULL , `Bank_Location` VARCHAR(50) NOT NULL , PRIMARY KEY (`Bank_ID`));")
        self.appCursor.execute(
            "CREATE TABLE if not exists `ecodb`.`services_details` ( `Service_ID` INT NOT NULL , `Service_Description` VARCHAR(100) NOT NULL , `Service_Rate` INT(10) NOT NULL , PRIMARY KEY (`Service_ID`));")

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
>>>>>>> a505de5579bccfd7715ad9f855441a8de58b635f


if __name__ == "__main__":
    db = Database()
<<<<<<< HEAD
    db.getdata()
=======
    print(db.getServiceRate('Monthly general Servicing (upto to 2 Ton)'))
    # db.getdata()
>>>>>>> a505de5579bccfd7715ad9f855441a8de58b635f
