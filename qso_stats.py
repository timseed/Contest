from dxcc import dxcc_all
from PyQt5 import QtCore, QtGui, QtWidgets
import logging


class qso_stats(QtCore.QObject):
    """
    A rather general class to store the QSO's that have been made.
    This will need to be updated when say a log file is opened.

    As I will add a Signal to be received by this Object - we have made this based on a QtObject

    """


    def __init__(self):
        super(qso_stats,self).__init__()
        self.logger = logging.getLogger(__name__)
        dx=dxcc_all()
        dx.read()
        self.ctry=dx.CountryList()

        #Using a List
        #BAND=[1,160,80,40,20,15,10]
        #table= [ [ 0 for i in range(len(BAND)) ] for j in ctry ]
        #for c in range(len(ctry)):
        #    table[c][0]=ctry[c]

        self.BAND=[160,80,40,30,20,18,15,12,10]
        self.qso = {}
        for c in self.ctry:
            b={}
            for B in self.BAND:
                b[B]=0
            self.qso[c]=b

    def contact(self,band,country):
        """
        Store the Band and Country - Not Mode... as I usually only do 1 Mode Contests
        :param band:
        :param country:
        :return:
        """
        if self.qso[country]:
            if self.qso[country][band]:
                self.qso[country][band] = self.qso[country][band] +1
            else:
                self.logger(str.format("Error Band {} does not exists for Country {}",band,country))
        else:
            self.logger(str.format("Error Country {} does not exists ", country))

    def summary_per_band(self):
        """
        Calculate the totals per Band
        Return as a List
        :return:
        """
        BandTot = [0 for b in range(len(self.BAND))]
        bandpos=0
        for b in self.BAND:
            for c in self.ctry:
                if self.qso[c][b]>0:
                    BandTot[bandpos] += 1
            bandpos += 1
        return BandTot
