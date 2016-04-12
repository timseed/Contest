import logging
from datetime import datetime

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from dxcc import dxcc_all

from MyEventFilter import MyQSOEventFilter
from qso_text_builder import qso_text_builder


class qsoWidget(QtWidgets.QWidget):
    logger = logging.getLogger(__name__)
    # Some Signals we want to send from this class
    RUN = QtCore.pyqtSignal(str)
    SEARCH = QtCore.pyqtSignal(str)
    TEXT = QtCore.pyqtSignal(str)
    SAVE = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)
        self._dxcclist = dxcc_all()
        self._dxcclist.read()
        self.BAND = QtWidgets.QComboBox()
        self.BAND.setObjectName("BAND")
        self.BAND.addItem("160")
        self.BAND.addItem("80")
        self.BAND.addItem("60")
        self.BAND.addItem("40")
        self.BAND.addItem("30")
        self.BAND.addItem("20")
        self.BAND.addItem("18")
        self.BAND.addItem("15")
        self.BAND.addItem("12")
        self.BAND.addItem("10")
        self._lastcall=""
        self.qsl=False
        self.qsofile="QSO.csv"

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
        self.btSAVE = QtWidgets.QPushButton()
        self.btSAVE.setObjectName("btSAVE")
        self.btSAVE.setText("Save")
        self.btCLEAR = QtWidgets.QPushButton()
        self.btCLEAR.setObjectName("btCLEAR")
        self.btCLEAR.setText("Clear")


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
        layout.addWidget(self.btSAVE,  9, 1, 1, 1)
        layout.addWidget(self.btCLEAR, 9, 2, 1, 1)

        # Need to Connect the Radio Buttons to a method which will send a Signal
        self.rbSEARCH.clicked.connect(self.sigMode)
        self.rbRUN.clicked.connect(self.sigMode)
        #self.btSEARCH.clicked.connect(self.saveQSO())
        self.btSAVE.clicked.connect(self.saveQSO)
        self.btCLEAR.clicked.connect(self.clear)

        self.myQSOFilter = MyQSOEventFilter()
        self.installEventFilter(self.myQSOFilter)
        #
        #Wire up the signals
        #
        self.myQSOFilter.QSORETURN.connect(self.retPressed)
        self.textbuilder = qso_text_builder('Contest/ru_test.yaml')
        self.textbuilder.SENT.connect(self.setSent)
        self.textbuilder.QSL.connect(self.setQSL)

        #Get the Max QSO Number
        self.textbuilder.setnumber(self.getMaxSentNumber())

    def retPressed(self,DATA):
        '''
        Return Pressed - Calculate the COUNTRY_NAME if possible
        :param DATA:
        :return:
        '''
        logging.info("retPressed - lookup Callsign")
        print("Ret Pressed")
        try:
            call = self.CALL.text().upper()
            if len(call)>0:
                logging.info("Call Longer then 0 ")
                ctry = self._dxcclist.find(call)
                logging.info("dx lookup Completed ")
                #ctry is a DXCC Object
                if ctry is not None:
                    logging.debug(str.format("COUNTRY_NAME needs to be set as <{}>",ctry.Country_Name()))
                    self.COUNTRY_NAME.setText(ctry.Country_Name())
                else:
                    logging.warning(str.format("Can not match Call of <{}>",call))
        except Exception as e:
            logging.error(str.format("Call sign lookup Exception Thrown {}",e.__class__.__name__))

        print("In RetPressed")
        self.textbuilder.setMode(0)
        self.textbuilder.setCall(self.CALL.text())
        self.textbuilder.setReceive(self.RECEIVE.text())
        self.textbuilder.setSent(self.SENT.text())

        txttosend=self.textbuilder.qso_text()
        logging.debug("txttosend is "+txttosend)
        #
        #Replace QRS and QRQ In the MAIN Window - as we do not own the CW Widget
        #
        self.TEXT.emit(txttosend)
        if self.qsl==True:
            self.saveQSO()
            self.CALL.setFocus()

    def setQSL(self):
        self.qsl=True

    def getMaxSentNumber(self):
        """
        Read QSO File and get the Number of Lines - i.e. the max number we have sent
        :return: Line count from file
        """
        try:
            with open(self.qsofile,"r") as file:
                n=len(file.readlines())
                file.close()
        except:
            n=0
        return n

    def setfiles(self,qso_file,rules_file):
        """
        Pass on Parameters to respective Sub Classes
        :param qso_file:
        :param rules_file:
        :return:
        """
        self.setContestFile(rules_file)
        self.setQsoFile(qso_file)

    def setContestFile(self,rules_file):
        self.logger.info(str.format("Setting Contest file to {}",rules_file))
        self.textbuilder.setrulesfile(rules_file)

    def setQsoFile(self,qso_file):
        self.logger.info(str.format("Setting Qso file to {}",qso_file))
        self.qsofile=qso_file
        self.textbuilder.setnumber(self.getMaxSentNumber())


    def saveQSO(self):
        """
        This Saves the current QSO
        :return:
        """
        if len(self.CALL.text())>2:
            ofp=open(self.qsofile,"a")
            line=str.format("{},{},{},{},{},{},{},{}\n",
                                    datetime.now().isoformat(),
                                    self.BAND.currentText(),
                                    self.MODE.currentText(),
                                    self.CALL.text(),
                                    self.RST.text(),
                                    self.SENT.text(),
                                    self.RECEIVE.text(),
                                    self.COUNTRY_NAME.text())
            ofp.write(line)
            ofp.close()
            self.clear()

    def clear(self):
        """
        Clear the QSO Data
        :return:
        """
        self._lastcall == self.CALL
        self.CALL.setText('')
        self.SENT.setText('')
        self.RECEIVE.setText('')
        self.COUNTRY_NAME.setText('')
        self.qsl=False
        self.CALL.setFocus()
        #      freqhz=self.Rig.qsyq()
        #      meters=self.Band.M(freqhz)
        #      self.BAND.setText(meters)

    def setSent(self,num):
        self.SENT.setText(num)
        self.RECEIVE.setFocus()

    def sigMode(self):
        if self.rbRUN.isChecked():
            self.RUN.emit("RUN")
            print("Emit RUN")
        else:
            print("Emit SEARCH")
            self.SEARCH.emit("SEARCH")