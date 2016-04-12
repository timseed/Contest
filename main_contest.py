
import logging
from enum import Enum

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
from rbn import HamBand
from Contest import Contest

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
