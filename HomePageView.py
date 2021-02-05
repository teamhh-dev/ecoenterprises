import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from AddButtonHandler import *


class HomePageView(QWidget):

    def __init__(self):
        self.addressBox = None
        self.addButton = None
        super().__init__()
        self.initGui()

    def initGui(self):
        self.setWindowTitle("QHBoxLayout Example")

        layout = QGridLayout()

        addressBox = QLineEdit()
        addButton = QPushButton("Add")
        addButton.clicked.connect(
            lambda: (addData(addressBox.text())))

        layout.addWidget(addressBox, 0, 1)
        layout.addWidget(addButton, 1, 1)
        # layout.addWidget(QPushButton("Right-Most"), 2, 1)

        # Set the layout on the application's window
        self.setLayout(layout)
        layout.setSpacing(20)
