import yaml
import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *


class qso_settings(object):
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.data = yaml.load(f)

    def get(self, key):
        """
        cq end resendsend
        :param key:
        :return:
        """
        return str(self.data['settings'][key])

class qso_text_builder(QtCore.QObject):
    """
    A QSO Builder for any form of automatic QSO's
    """

    SENT = QtCore.pyqtSignal(str)
    RECEIVED = QtCore.pyqtSignal(str)
    QSL  = QtCore.pyqtSignal(str)

    def __init__(self, config_filename):
        super(qso_text_builder,self).__init__()
        self._call = ''
        self._sent = ''
        self._receive = ''
        self._number = 0
        self.logger = logging.getLogger(__name__)
        self.setting = qso_settings(config_filename)
        self._mode =  0
        #RUN = 0
        #SP = 1

    def setrulesfile(self,filename):
        self.logger.info(str.format("Config filename {} being used",filename))
        self.setting = qso_settings(filename)

    def clear(self):
        self._call = ''
        self._sent = ''
        self._receive = ''

    def newnumber(self):
        self._number = self._number + 1

    def getnumber(self):
        return str(self._number)

    def setnumber(self,c):
        """
        This should only be called 1 time - when the Setup is being run.
        So we can stop and start the logger
        :param c:
        :return:
        """

        self._number=c

    def setCall(self, c):
        self._call = c

    def getCall(self):
        return self._call

    def setSent(self, c):
        self._sent = c

    def getSent(self):
        return str(self._sent)

    def setReceive(self, c):
        self._receive = c

    def getReceive(self):
        return str(self._receive)

    def getMode(self):
        return str(self._mode)

    def setMode(self,c):
        self._mode=c

    def qso_text(self):
        cl = len(self._call)
        sl = len(self._sent)
        rl = len(self._receive)
        if self._mode == 0:
            #Run MODE
            if cl == 0 and sl == 0 and rl == 0:
                # MSG1
                self.logger.info("MSG1")
                return self.make_text(1)
            elif cl < 3 and sl == 0 and rl == 0:
                # Partial call
                # MSG2
                self.logger.info("MSG2")
                return self.make_text(2)
            elif cl > 2 and sl == 0 and rl == 0:
                # MSG3
                # Got call  - send sumber
                self.newnumber()
                self.setSent(self.getnumber())
                self.SENT.emit(self.getnumber())
                self.logger.info("MSG3")
                return self.make_text(3)
            elif cl > 2 and sl > 0 and rl == 0:
                # MSG4
                # We have sent - but we have not heard out return value
                self.logger.info("MSG4")
                return self.make_text(4)
            elif cl > 2 and sl > 0 and rl > 0:
                # MSG5
                # We have everythng we need
                self.logger.info("MSG5")
                self.clear()
                self.QSL.emit('QSL')
                return self.make_text(5)
            return "Opps"
        else:
            #S&P Mode
            if cl >3 and sl == 0 and rl == 0:
                # Make Contact
                self.logger.info("MSG6")
                return self.make_text(6)
            elif cl >3 and sl == 0 and rl > 0:
                #
                self.newnumber()
                self.setSent(self.getnumber())
                self.SENT.emit(self.getSent())
                self.logger.info("MSG7")
                return self.make_text(7)
            elif cl >3 and sl >0  and rl > 0:
                self.logger.info("MSG8")
                self.QSL.emit('QSL')
                return self.make_text(8)
            else:
                return "Eek S&P Error"

    def show(self, sz):
        print("%s" % sz)

    def make_text(self, MSG_NUM):
        """

       :param MSG_NUM: 1-5 int
       :return:
       """
        if MSG_NUM > 8 or MSG_NUM < 1:
            return "Bad Msg Number"
        #Get Initial MSG from YAML File
        text = self.setting.get("MSG" + str(MSG_NUM))
        text = text.replace('MYCALL', self.setting.get('MYCALL'))
        text = text.replace('SENT',self.setting.get('SENT'))
        #Now update from current QSO going on
        text = text.replace('CALL', self.getCall())
        text = text.replace('SENT',self.setting.get('SENT'))
        text = text.replace('NUMBER',self.getnumber())
        return text

if __name__ == "__main__":
    q = qso_text_builder("Contest/ru_test.yaml")
    m=0
    print("======= Run Mode Test ============")
    print("=== All Empty ===")
    q.show(q.qso_text())
    print("=== Partial Call ===")
    q.setCall('m')
    q.show(q.qso_text())
    print("=== Full Call ===")
    q.setCall('m0fgc')
    q.show(q.qso_text())
    print("===  No Number  ===")
    q.setReceive("")
    q.show(q.qso_text())
    print("=== Got Number ===")
    q.setReceive("12")
    q.show(q.qso_text())

    print("=== All Empty ===")
    q.setMode(1)
    q.clear()
    print("=== Full Call ===")
    q.setCall('m0fgc')
    q.show(q.qso_text())
    print("===  No Number  ===")
    q.setReceive("")
    q.show(q.qso_text())
    print("=== Got Number ===")
    q.setReceive("12")
    q.show(q.qso_text())
    print("=== Got ALL ===")
    q.show(q.qso_text())
    print("======New Contact=========")
    q.clear()
    print("=== Full Call ===")
    q.setCall('m1fgc')
    q.show(q.qso_text())
    print("===  No Number  ===")
    q.setReceive("")
    q.show(q.qso_text())
    print("=== Got Number ===")
    q.setReceive("12")
    q.show(q.qso_text())
    print("=== Got ALL ===")
    q.show(q.qso_text())