from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import logging

class spidWidget(QtWidgets.QWidget):

  MOVETO = QtCore.pyqtSignal(str)
  STOP   = QtCore.pyqtSignal(str)
  STATUS = QtCore.pyqtSignal(str)

  def __init__(self, parent = None):

     QtWidgets.QWidget.__init__(self, parent)
     self.logger = logging.getLogger(__name__)
     bearingLabel = QLabel(self.tr("Bearing:"))
     cancelButton = QtWidgets.QPushButton("Cancel",self)     
     cancelButton.setStyleSheet('QPushButton {background-color: #FF0000; foreground-color: #00FFFF;}')
     statusButton = QtWidgets.QPushButton("Status",self)     
     statusButton.setStyleSheet('QPushButton {background-color: #00FF00; foreground-color: #00FFFF;}')
     rotateButton = QtWidgets.QPushButton("Rotate",self)
     self.bearingSpinBox = QDoubleSpinBox()
     self.bearingSpinBox.setRange(0, 360)
     self.bearingSpinBox.setDecimals(0)

     #self.bearingSpinBox.valueChanged['double'].connect(self.bearingChanged)
     cancelButton.clicked.connect(self.stop)
     statusButton.clicked.connect(self.status)
     rotateButton.clicked.connect(self.bearingChanged)
     QtCore.QMetaObject.connectSlotsByName(self)
     layout = QGridLayout(self)
     layout.addWidget(bearingLabel, 0, 0)
     layout.addWidget(self.bearingSpinBox, 0, 1)
     layout.addWidget(rotateButton,1, 1,1,1)
     layout.addWidget(cancelButton,2, 0)
     layout.addWidget(statusButton,2, 1)

  def bearingChanged(self):
     #Emit a Signal so some other class can connect to this
     self.logger.debug("Emitting !!")
     self.MOVETO.emit(self.bearingSpinBox.text())


  def stop(self,val):
     self.logger.debug("Stop")
     self.STOP.emit("Stop")

  def status(self,val):
     self.logger.debug("Status")
     self.STATUS.emit("Status")
