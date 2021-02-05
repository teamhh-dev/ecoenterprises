from HomePageView import *
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePageView()
    window.show()
    sys.exit(app.exec_())
