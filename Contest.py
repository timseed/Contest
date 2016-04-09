import logging
from enum import Enum

from dxcc import dxcc_all
from rbn import HamBand

from ContestUI import *
from k3 import K3
#from MyEventFilter import MyQSOEventFilter
from qsoWidget import qsoWidget
from cwWidget import cwWidget
from spidWidget import spidWidget
from spid3 import spid
from qtbeacon import qtbeacon
from datetime import datetime


class QSOMod(Enum):
    RUN = 0
    SP = 1


class Contest(Ui_MainWindow):

    logger = logging.getLogger(__name__)

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
        # Connect the 2 Signals to a local Method
        self.qso.RUN.connect(self.runMode)
        self.qso.SEARCH.connect(self.runMode)

        self.beacon_network = qtbeacon()
        self.beacon_network.BEACON.connect(self.onBEACON)
        self.beacon_network.start()

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

    def saveQSO(self):

        ofp=open("QSO.csv","a")
        line=str.format("{},{},{},{},{},{}\n",datetime.now().isoformat(),
                                self.qso.BAND.currentText(),
                                self.qso.MODE.currentText(),
                                self.qso.CALL.text(),
                                self.qso.RST.text(),
                                self.qso.SENT.text(),
                                self.qso.RECEIVE.text())
        ofp.write(line)
        ofp.close()
        self._lastcall == self.GetText(self.qso.CALL)
        self.qso.CALL.setText('')
        self.qso.SENT.setText('')
        self.qso.RECEIVE.setText('')
        self.qso.COUNTRY_NAME.setText('')
        #      freqhz=self.Rig.qsyq()
        #      meters=self.Band.M(freqhz)
        #      self.BAND.setText(meters)

    def retPressed(self,txttosend):
        print("In retPressed data passed is "+txttosend)
        fast=self.cww.lbQRQ.text()
        print("fast is %s"%fast)
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


    def onBEACON(self,data):
        logging.debug("Beacon Data Arrived")
        items=len(data)
        while self.beaconTable.rowCount()<5:
                self.beaconTable.insertRow(0)

        logging.debug(str.format("We got {} beacon objects",items))
        rowPosition=0
        for n in data:
            for i in range(len(n)):
                #print(str.format("i {} data {} ",i,n[i]))
                self.beaconTable.setItem(rowPosition , i, QtWidgets.QTableWidgetItem(str(n[i])))
            rowPosition += 1

    def runMode(self, data):
        if data == "RUN":
            logging.info("Run Mode")
            print("run Mode")
            self._mode = 0
        else:
            logging.info("Search Mode")
            print("search Mode")
            self._mode = 1

    def key_speed(self, type=0, text=''):
        """
        :param type: 0 Means Number - the default. 1 means Text/Message
        :param text: Initial String
        :return:
        """

        if type == 0:
            rv = "KS%03d;KYW %s ;" % (int(self.GetText(self.cww.lbQRQ)), text)
        else:
            rv = "KS%03d;KYW %s ;KS%03d;" % (
                int(self.GetText(self.cww.lbQRS)),
                text,
                int(self.GetText(self.cww.lbQRQ)))
        return rv

    def what_to_send_unused(self, mode, CALL='', SENT='', RECEIVED=''):
        """
        This Method is called when the Return Key is pressed

        :param mode:
        :param CALL:
        :param SENT:
        :param RECEIVED:
        :return:
        """

        logging.debug("In What to Send")
        cl = len(CALL)
        sl = len(SENT)
        rl = len(RECEIVED)
        logging.debug("Got Lengths of variables")
        name=""

        try:
            curwidget = QtWidgets.QApplication.focusWidget()
            if curwidget != 0:
                logging.debug("curwidget is not 0")
                logging.debug(str.format("curwidget is <{}>",curwidget))
                try:
                    name = curwidget.objectName()
                    logging.debug(str.format("Widget name is <{}>",name))
                except:
                    name = "UNknown"
                    logging.debug("Error in curwidget")
                    return "Err"
            else:
                print("Not sure what the active widget is")
        except:
            name = "UNknown"
            logging.debug("Error in curwidget")
            return "Err"

        logging.debug("Getting Mode")
        logging.debug(str.format("Active field is <{}>",name))
        if mode == 0:
            logging.info("Run Mode")
            if name == "CALL":
                logging.debug("CALL")
                if cl == 0:
                    return self.key_speed(0, 'test a45wg a45wg')
                if cl < 3:
                    return self.key_speed(0, CALL + ' ?')
                if cl >= 3 and sl == 0:
                    # Send my NUMBER
                    self.qso.RECEIVE.setFocus()
                    if CALL != self._lastcall and CALL != '':
                        self._number = self.nextNumber()
                        self.qso.RECEIVE.setFocus()
                        self.qso.SENT.setText(str(self._number))
                    #if self.rbSendNumber.isChecked():
                    #    return self.key_speed(0, CALL) + self.key_speed(1, ' 599 ') + self.key_speed(0,
                    #                                                                                 str(self._number))
                    #else:
                        return self.key_speed(0, CALL) + self.key_speed(1, ' 599 ')
            elif name == "SENT":
                logging.debug("SENT")
                if sl > 0 and rl == 0:
                    if name == "tim":
                        #self.rbSendNumber.isChecked():
                        self.qso.RECEIVE.focusWidget()
                        return self.key_speed(1, ' 599 ') + self.key_speed(0, self.GetText(self.qso.SENT))
                else:
                    return self.key_speed(0, CALL) + self.key_speed(1, ' 599 ')
            elif name == "RECEIVE":
                logging.debug("RECEIVE")
                if cl > 3 and sl > 0 and rl > 0:
                    self.saveQSO()
                    self.qso.CALL.setFocus()
                    return self.key_speed(0, "tu de a45wg")
                else:
                    return self.key_speed(0, CALL) + \
                           self.key_speed(1, ' 599 ') + \
                           self.key_speed(0, self.GetText(self.qso.SENT)) + \
                           self.key_speed(0, ' NR ?')
            else:
                logging.error("Unknown field we are pressing return from")
                return "UNKNOWN"
        else:
            logging.info("S&P Mode")
            logging.debug("Mode 1 no data yet")
            return ""



    def what_to_send_orig(self, mode, CALL='', SENT='', RECEIVED=''):
        """
        This Method is called when the Return Key is pressed

        :param mode:
        :param CALL:
        :param SENT:
        :param RECEIVED:
        :return:
        """
        cl = len(CALL)
        sl = len(SENT)
        rl = len(RECEIVED)

        # QWidget * QApplication::focusWidget ()

        if mode == 0:
            logging.info("Run Mode")
            if cl == 0 and sl == 0 and rl == 0:
                return self.key_speed(0, 'test a45wg a45wg')
            if cl > 0 and cl < 3 and sl == 0 and rl == 0:
                return self.key_speed(0, CALL + ' ?')
            if cl >= 3 and sl == 0:
                # Send my NUMBER
                self.qso.RECEIVE.setFocus()
                if CALL != self._lastcall and CALL != '':
                    self._number = self.nextNumber()
                    self.qso.RECEIVE.setFocus()
                    self.qso.SENT.setText(str(self._number))
                if self.rbSendNumber.isChecked():
                    return self.key_speed(0, CALL) + self.key_speed(1, ' 599 ') + self.key_speed(0, str(self._number))
                else:
                    return self.key_speed(0, CALL) + self.key_speed(1, ' 599 ')
            if cl > 3 and sl > 0 and rl == 0:
                if self.rbSendNumber.isChecked():
                    self.qso.RECEIVE.focusWidget()
                    return self.key_speed(1, ' 599 ') + self.key_speed(0, self.GetText(self.qso.SENT) + ' NR ?')
                else:
                    return self.key_speed(0, CALL) + self.key_speed(1, ' 599 ')
            if cl > 3 and sl > 0 and rl > 0:
                self.saveQSO()
                self.qso.CALL.setFocus()
                return self.key_speed(0, "tu de a45wg")
        else:
            logging.info("S&P Mode")


if __name__ == "__main__":


    import parser
    def useage():
        print("Error Reading Parameters")
        print("Try main.py --help")
        print("Usage: main.py -r <FILENAME> -d <FILENAME> -v INFO|DEBUG|CRITICAL")
        exit()
    test = 0
    from optparse import OptionParser

    qso_file = ""
    rules_file = ""

    parser = OptionParser()
    parser.add_option("-r", "--rules", dest="rules_filename",
                      help="Rules-contest file to read", metavar="FILE")
    parser.add_option("-q", "--qso", dest="qso_filename",
                      help="qso file to save as ", metavar="FILE")

    (options, args) = parser.parse_args()
    try:
        rules_file = options.rules_filename
        qso_file   = options.qso_filename
        if len(rules_file) == 0 or len(qso_file) == 0:
            useage()
    except:
            useage()

    import sys
    import logging.config
    logging.config.fileConfig('logging.conf')
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Contest()
    ui.qso.setfiles(qso_file,rules_file)

    #ui.setContestFile(rules_file)
    #ui.setQsoFile(qso_file)

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
