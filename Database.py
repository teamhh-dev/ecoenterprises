import mysql.connector


class Database:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="twitter_"
        )
        self.appCursor = self.mydb.cursor()
        self.initDatabase()

    def initDatabase(self):
        self.appCursor.execute("create database if not exists ecodb")
        self.appCursor.execute("CREATE TABLE `ecodb`.`complaints` ( `invoice_id` VARCHAR(15) NOT NULL ,  `date` DATE NOT NULL ,  `branch_address` VARCHAR(50) NOT NULL ,  `zone` VARCHAR(10) NOT NULL ,  `complaint_no` INT(10) NOT NULL ,    PRIMARY KEY  (`invoice_id`));")

    def getdata(self):
        self.appCursor.execute("SELECT * FROM hamzaalidatabase.customer")
        for row in self.appCursor:
            print(row)


if __name__ == "__main__":
    db = Database()
    db.getdata()
