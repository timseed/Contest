
import sys
import logging.config
import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from ContestUI import *
from Contest import Contest
import parser
from optparse import OptionParser
import yaml

if __name__ == "__main__":



    def useage():
        print("Error Reading Parameters")
        print("Try main.py --help")
        print("Usage: main.py -r <FILENAME> -d <FILENAME> -v INFO|DEBUG|CRITICAL")
        exit()
    test = 0

    qso_file = ""
    rules_file = ""

    parser = OptionParser()
    parser.add_option("-r", "--rules", dest="rules_filename",
                      help="Rules-contest file to read", metavar="FILE")
    parser.add_option("-q", "--qso", dest="qso_filename",
                      help="qso file to save as ", metavar="FILE")
    parser.add_option("-l", "--location", dest="location",
                      help="Maidenhead Location used for bearings and distance", metavar="FILE")


    (options, args) = parser.parse_args()
    try:
        rules_file = options.rules_filename
        qso_file   = options.qso_filename
        location   = options.location

        if len(rules_file) == 0 or len(qso_file) == 0 or len(location) == 0:
            useage()
    except:
            useage()

    logging.config.fileConfig('logging.conf')
    with open('logging.yaml','rt') as f:
        config=yaml.safe_load(f.read())
        f.close()
    logger=logging.getLogger(__name__)
    logger.info("Contest is starting")
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    logger.info("Creating Contest object")
    ui = Contest()

    try:
        logger.info("Process css")
        with open('contest.css') as f:
            css=''
            for line in f:
                css = css+line
            MainWindow.setStyleSheet(css)
            f.close()
    except:
        logger.error("Error reading contest.css")


    #MainWindow.setStyleSheet("QLineEdit { background-color: yellow }");
    #ui.qso.setStyleSheet("QLineEdit#CALL { background-color: yellow }")
    #MainWindow.setStyleSheet("QLineEdit#CALL { background-color: yellow }")

    ui.qso.setfiles(qso_file,rules_file)
    ui.qso.setlocation(location)

    #ui.setContestFile(rules_file)
    #ui.setQsoFile(qso_file)

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
