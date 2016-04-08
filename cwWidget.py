from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *


class cwWidget(QtWidgets.QWidget):
    # Some Signals we want to send from this class
    #QRQ = QtCore.pyqtSignal(str)
    #QRS = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)

        l1 = QLabel(self.tr("RST Speed:"))
        l2 = QLabel(self.tr("CW  Speed:"))
        l3 = QLabel(self.tr("Numbers:"))

        self.lbQRQ= QtWidgets.QLineEdit()
        self.lbQRQ.setObjectName("QRQ")
        self.lbQRQ.setText("35")

        self.lbQRS = QtWidgets.QLineEdit()
        self.lbQRS.setObjectName("QRS")
        self.lbQRS.setText("25")
        layout = QGridLayout(self)
        layout.addWidget(l1, 1, 0)
        layout.addWidget(self.lbQRQ, 1, 1)
        layout.addWidget(l2, 0, 0)
        layout.addWidget(self.lbQRS, 0, 1)

