from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from MyEventFilter import MyQSOEventFilter
from dxcc import dxcc_all
import logging

class qsoWidget(QtWidgets.QWidget):
    logger = logging.getLogger(__name__)
    # Some Signals we want to send from this class
    RUN = QtCore.pyqtSignal(str)
    SEARCH = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)
        self._dxcclist = dxcc_all()
        self._dxcclist.read()
        self.BAND = QtWidgets.QComboBox()
        self.BAND.setObjectName("BAND")
        self.BAND.addItem("160")
        self.BAND.addItem("80")
        self.BAND.addItem("40")
        self.BAND.addItem("20")
        self.BAND.addItem("15")
        self.BAND.addItem("10")
        
        self.MODE= QtWidgets.QComboBox()
        self.MODE.setObjectName("MODE")
        self.MODE.addItem("CW")
        self.MODE.addItem("SSB")

        l1 = QLabel(self.tr("Band:"))
        l1a = QLabel(self.tr("Mode:"))
        l2 = QLabel(self.tr("Call:"))
        l3 = QLabel(self.tr("RST:"))
        l4 = QLabel(self.tr("Sent:"))
        l5 = QLabel(self.tr("Receive:"))
        l6 = QLabel(self.tr("Country:"))
        l7 = QLabel(self.tr("Run:"))
        l8 = QLabel(self.tr("Search:"))

        self.CALL = QtWidgets.QLineEdit()
        self.CALL.setObjectName("CALL")
        self.RST = QtWidgets.QLineEdit()
        self.RST.setText("599/599")
        self.RST.setObjectName("RST")
        self.SENT = QtWidgets.QLineEdit()
        self.SENT.setObjectName("SENT")
        self.RECEIVE = QtWidgets.QLineEdit()
        self.RECEIVE.setObjectName("RECEIVE")
        self.COUNTRY_NAME = QtWidgets.QLineEdit()
        self.COUNTRY_NAME.setObjectName("COUNTRY_NAME")
        self.rbRUN = QtWidgets.QRadioButton()
        self.rbRUN.setChecked(True)
        self.rbRUN.setObjectName("rbRUN")
        self.rbSEARCH = QtWidgets.QRadioButton()
        self.rbSEARCH.setChecked(False)
        self.rbSEARCH.setObjectName("rbSEARCH")

        layout = QGridLayout(self)
        layout.addWidget(l1, 0, 0)
        layout.addWidget(self.BAND, 0, 1)
        layout.addWidget(l1a, 1, 0)
        layout.addWidget(self.MODE, 1, 1)

        layout.addWidget(l2, 2, 0)
        layout.addWidget(self.CALL, 2, 1)
        layout.addWidget(l3, 3, 0)
        layout.addWidget(self.RST, 3, 1)
        layout.addWidget(l4, 4, 0)
        layout.addWidget(self.SENT, 4, 1)
        layout.addWidget(l5, 5, 0)
        layout.addWidget(self.RECEIVE, 5, 1)
        layout.addWidget(l6, 6, 0)
        layout.addWidget(self.COUNTRY_NAME, 6, 1)
        layout.addWidget(l7, 7, 1)
        layout.addWidget(self.rbRUN, 7, 2, 1, 1)
        layout.addWidget(l8, 8, 1)
        layout.addWidget(self.rbSEARCH, 8, 2, 1, 1)

        # Need to Connect the Radio Buttons to a method which will send a Signal
        self.rbSEARCH.clicked.connect(self.sigMode)
        self.rbRUN.clicked.connect(self.sigMode)

        self.myQSOFilter = MyQSOEventFilter()
        self.installEventFilter(self.myQSOFilter)
        self.myQSOFilter.QSORETURN.connect(self.retPressed)


    def retPressed(self,DATA):
        '''
        Return Pressed - Calculate the COUNTRY_NAME if possible
        :param DATA:
        :return:
        '''
        logging.info("retPressed - lookup Callsign")
        try:
            call = self.CALL.text()
            if len(call)>0:
                logging.info("retPressed - lookup Callsign")
                ctry = self._dxcclist.find(call)
                #ctry is a DXCC Object
                if len(call) >0:
                    logging.debug(str.format("COUNTRY_NAME needs to be set as <{}>",ctry.Country_Name()))
                    self.COUNTRY_NAME.setText(ctry.Country_Name())
                else:
                    logging.warning(str.format("Can not match Call of <{}>",call))
        except Exception as e:
            logging.error(str.format("Exception Thrown {}",e.__class__.__name__))



    def sigMode(self):
        if self.rbRUN.isChecked():
            self.RUN.emit("RUN")
            print("Emit RUN")
        else:
            print("Emit SEARCH")
            self.SEARCH.emit("SEARCH")
