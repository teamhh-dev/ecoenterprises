from AppController import *

if __name__ == "__main__":
    try:
        db = Database()
        app = AppController(db)
    except Exception as e:
        print(e.__str__())
