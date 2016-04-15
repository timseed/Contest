import logging
from enum import Enum
import datetime
from dxcc import dxcc_all
from rbn import HamBand

from ContestUI import *
from k3 import K3

from qsoWidget import qsoWidget
from cwWidget import cwWidget
from spidWidget import spidWidget
from spid3 import spid
from qtbeacon import qtbeacon
from datetime import datetime
from rbn import HamBand, rbn
from qtrbn import qtrbn


class QSOMod(Enum):
    RUN = 0
    SP = 1

class Contest(Ui_MainWindow):

    def __init__(self):
        super(Contest, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Init")
        self._dxcclist = dxcc_all()
        self._dxcclist.read()
        self._spidgui = spidWidget()
        self._spid = spid()
        self._number = 0
        self._lastcall = ''
        self._mode = 0
        self._call = ''
        self._calllen = 0
        self._sent = ''
        self._sentlen = 0

        self._received = ''
        self._receivedlen = 0
        self.qso = qsoWidget()
        self.cww = cwWidget()
        self.band = HamBand()  #Convert from hz to M

        self.beacon_network = qtbeacon()
        self.beacon_network.BEACON.connect(self.onBEACON)
        self.beacon_network.start()

        self._rbn = qtrbn()
        try:
            self.logger.debug('setting up RBN Signal')
            self.rbnWantedBand='All'
            self._rbn.RBN.connect(self.onRBN)
            self.logger.debug('RBN Starting')
            self._rbn.start()
            #Note the Button is setup in SetupUI
            self.logger.info('RBN Started')
        except Exception as e:
            self.logger.error("Error with rbn {}".format(str(e)))

        self._spidgui.MOVETO.connect(self._spid.moveto)
        self._spidgui.STOP.connect(self._spid.stop)
        self._spidgui.STATUS.connect(self._spid.status)
        self.qso.TEXT.connect(self.retPressed)

        try:
            self.Rig = K3()  # My Rig Controll Class
            self.Band = HamBand()  # Work out the Ham Bands
        except:
            self.Rig = None
            self.logger.error("No k3 Present")

    def escape(self):
        junk = 1

    def setupUi(self, *argv, **argvw):

        """
        Setup the "wiring" in the GUI
        This should not add new widgets to the UI.
        We connect widgets to functions
        and signals to slots.

        It is important to call the base method also

        :param argv:
        :param argvw:
        :return:
        """
        super(Contest, self).setupUi(*argv, **argvw)

        self._mode = 0
        self._call = None
        self._calllen = 0
        self._number = None

        self.escape()
        logging.debug("setupUI called")
        self.verticalLayout.addWidget(self.qso)
        self.verticalLayout.addWidget(self.cww)
        self.rbSendNumber = self.rbSEARCH = QtWidgets.QRadioButton()
        self.rbSendNumber.setChecked(True)
        #
        # Add the Rotator Controller
        self.tab2layout.addWidget(self._spidgui)
        #
        #
        self.beaconTable.setHorizontalHeaderItem(0,QtWidgets.QTableWidgetItem("Call"))
        self.beaconTable.setHorizontalHeaderItem(1,QtWidgets.QTableWidgetItem("Country"))
        self.beaconTable.setHorizontalHeaderItem(2,QtWidgets.QTableWidgetItem("Freq"))
        try:
            self.rbnClear.clicked.connect(self.onRBNclear)
        except Exception as e:
            self.logger.error("Error setting up rbnClear "+str(e))


        try:
            self.cbrbnBand.currentIndexChanged['int'].connect(self.rbnBandChange)
        except Exception as e:
            self.logger.error("Error setting up rbnBandChange "+str(e))




    def nextNumber(self):
        try:
            self._number = self._number + 1
            return self._number
        except:
            self._number = 1
            return self._number

    def GetText(self, widget):
        """
        Gets Text Value from a Widget
        :param widget:
        :return:
        """
        try:
            tmp = widget.text()
            logging.debug(str.format("Widget Name <{}> Value <{}>",str(widget.objectName()),tmp))
            return tmp
        except ValueError:
            logging.error("Value Error Error")
            return ''
        except:
            logging.error("Some other error")
            return ''

    def rbnBandChange(self,band_id):
        self.logger.debug("rbnBandChange called")
        junk=1
        self.rbnWantedBand = str(self.cbrbnBand.currentText())
        if self.rbnWantedBand != 'All':
            self.onRBNclear()



    def retPressed(self,txttosend):
        self.logger.debug("In retPressed data passed is "+txttosend)
        fast=self.cww.lbQRQ.text()
        self.logger.debug("fast is %s"%fast)
        fastcw = str.format('KS{:03d};', int(self.GetText(self.cww.lbQRQ)))
        slowcw = str.format('KS{:03d};', int(self.GetText(self.cww.lbQRS)))

        for word in txttosend.split(' '):
            if word == 'QRS':
                if self.Rig is not None:
                    self.Rig.sendcw(slowcw)
                    self.logger.debug(str.format("Rig Sent {}", slowcw))
            elif word == 'QRQ':
                if self.Rig is not None:
                    self.Rig.sendcw(fastcw)
                    self.logger.debug(str.format("Rig Sent {}", fastcw))
            else:
                if self.Rig is not None:
                    cmd = str.format('KYW {};', word)
                    self.Rig.sendcw(cmd)
                    self.logger.debug(str.format("Rig Sent {}", cmd))
        if self.Rig is not None:
            self.Rig.sendcw(slowcw)

    def onRBN(self,data):
        """
        Handle the RBN Signal
        :param data: a list of rbn_tup types
        :return:
        """
        self.logger.debug('RBN data has arrived')
        print("RBN data has arrived")

        items=len(data)
        logging.debug(str.format("We got {} beacon objects",items))
        rowPosition=self.rbnTable.rowCount()
        for n in data:
            if self.rbnWantedBand == 'All' or self.rbnWantedBand == n[4]:

                self.rbnTable.insertRow(rowPosition)
                tn=datetime.now()
                tn=tn.time().strftime('%H:%M:%S')
                self.rbnTable.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(str(tn)))

                for i in range(len(n)):
                    self.logger.debug("Adding Data at {} {} data {} ".format(rowPosition,i+1,n[i]))
                    print("Adding Data at {} {} data {} ".format(rowPosition,i+1,n[i]))
                    self.rbnTable.setItem(rowPosition ,
                                          i+1,
                                          QtWidgets.QTableWidgetItem(str(n[i])))
                rowPosition += 1
            else:
                self.logger.debug("rbn Record rejected due to Band settings")

    def onRBNclear(self):
        row = self.rbnTable.rowCount()
        while row>=0:
            self.rbnTable.removeRow(row)
            row=row-1

    def onBEACON(self,data):
        logging.debug("Beacon Data Arrived")
        items=len(data)
        if self.Rig is not None:
            freq=self.Rig.qsyq()
            if len(freq)>4:
                self.logger.debug("freq is %s"%freq)
                Band_In_M=self.band.M(float(freq))
                if Band_In_M != None:
                    self.logger.debug(str.format("Band in M is {}",Band_In_M))
                    hf_band_index=self.Band.Index(Band_In_M)
                    if hf_band_index != -1:
                        self.qso.BAND.setCurrentIndex(hf_band_index)
        while self.beaconTable.rowCount()<5:
                self.beaconTable.insertRow(0)

        logging.debug(str.format("We got {} beacon objects",items))
        rowPosition=0
        for n in data:
            for i in range(len(n)):
                #self.logger.debug(str.format("i {} data {} ",i,n[i]))
                self.beaconTable.setItem(rowPosition , i, QtWidgets.QTableWidgetItem(str(n[i])))
            rowPosition += 1



