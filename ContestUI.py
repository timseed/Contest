# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ContestUi.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 657)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rbnTab = QtWidgets.QTabWidget(self.frame)
        self.rbnTab.setObjectName("rbnTab")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.CMD = QtWidgets.QPlainTextEdit(self.tab)
        self.CMD.setGeometry(QtCore.QRect(20, 20, 601, 161))
        self.CMD.setObjectName("CMD")
        self.rbnTab.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(30, 30, 541, 461))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.tab2layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.tab2layout.setObjectName("tab2layout")
        self.beaconTable = QtWidgets.QTableWidget(self.verticalLayoutWidget_2)
        self.beaconTable.setColumnCount(3)
        self.beaconTable.setObjectName("beaconTable")
        self.beaconTable.setRowCount(0)
        self.tab2layout.addWidget(self.beaconTable)
        self.rbnTab.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.frame_3 = QtWidgets.QFrame(self.tab_3)
        self.frame_3.setGeometry(QtCore.QRect(10, 10, 131, 470))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.cbclusterBand = QtWidgets.QComboBox(self.frame_3)
        self.cbclusterBand.setObjectName("cbclusterBand")
        self.cbclusterBand.addItem("")
        self.cbclusterBand.addItem("")
        self.cbclusterBand.addItem("")
        self.cbclusterBand.addItem("")
        self.cbclusterBand.addItem("")
        self.cbclusterBand.addItem("")
        self.cbclusterBand.addItem("")
        self.cbclusterBand.addItem("")
        self.cbclusterBand.addItem("")
        self.cbclusterBand.addItem("")
        self.cbclusterBand.addItem("")
        self.verticalLayout_4.addWidget(self.cbclusterBand)
        self.clusterMycall = QtWidgets.QRadioButton(self.frame_3)
        self.clusterMycall.setObjectName("clusterMycall")
        self.verticalLayout_4.addWidget(self.clusterMycall)
        self.clusterClear = QtWidgets.QPushButton(self.frame_3)
        self.clusterClear.setObjectName("clusterClear")
        self.verticalLayout_4.addWidget(self.clusterClear)
        self.rbnTable_2 = QtWidgets.QTableWidget(self.tab_3)
        self.rbnTable_2.setGeometry(QtCore.QRect(150, 10, 494, 470))
        self.rbnTable_2.setColumnCount(10)
        self.rbnTable_2.setObjectName("rbnTable_2")
        self.rbnTable_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.rbnTable_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.rbnTable_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.rbnTable_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.rbnTable_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.rbnTable_2.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.rbnTable_2.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.rbnTable_2.setHorizontalHeaderItem(6, item)
        self.rbnTab.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab_4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_2 = QtWidgets.QFrame(self.tab_4)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cbrbnBand = QtWidgets.QComboBox(self.frame_2)
        self.cbrbnBand.setObjectName("cbrbnBand")
        self.cbrbnBand.addItem("")
        self.cbrbnBand.addItem("")
        self.cbrbnBand.addItem("")
        self.cbrbnBand.addItem("")
        self.cbrbnBand.addItem("")
        self.cbrbnBand.addItem("")
        self.cbrbnBand.addItem("")
        self.cbrbnBand.addItem("")
        self.cbrbnBand.addItem("")
        self.cbrbnBand.addItem("")
        self.cbrbnBand.addItem("")
        self.verticalLayout_2.addWidget(self.cbrbnBand)
        self.rbnMycall = QtWidgets.QRadioButton(self.frame_2)
        self.rbnMycall.setObjectName("rbnMycall")
        self.verticalLayout_2.addWidget(self.rbnMycall)
        self.rbnClear = QtWidgets.QPushButton(self.frame_2)
        self.rbnClear.setObjectName("rbnClear")
        self.verticalLayout_2.addWidget(self.rbnClear)
        self.horizontalLayout_4.addWidget(self.frame_2)
        self.rbnTable = QtWidgets.QTableWidget(self.tab_4)
        self.rbnTable.setColumnCount(10)
        self.rbnTable.setObjectName("rbnTable")
        self.rbnTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.rbnTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.rbnTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.rbnTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.rbnTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.rbnTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.rbnTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.rbnTable.setHorizontalHeaderItem(6, item)
        self.horizontalLayout_4.addWidget(self.rbnTable)
        self.rbnTab.addTab(self.tab_4, "")
        self.horizontalLayout_2.addWidget(self.rbnTab)
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget = QtWidgets.QWidget(self.dockWidgetContents)
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout_3.addWidget(self.widget)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.dockWidget_2 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_2)

        self.retranslateUi(MainWindow)
        self.rbnTab.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.rbnTab.setTabText(self.rbnTab.indexOf(self.tab), _translate("MainWindow", "CW Gen"))
        self.rbnTab.setTabText(self.rbnTab.indexOf(self.tab_2), _translate("MainWindow", "Beacons"))
        self.cbclusterBand.setItemText(0, _translate("MainWindow", "All"))
        self.cbclusterBand.setItemText(1, _translate("MainWindow", "160"))
        self.cbclusterBand.setItemText(2, _translate("MainWindow", "80"))
        self.cbclusterBand.setItemText(3, _translate("MainWindow", "60"))
        self.cbclusterBand.setItemText(4, _translate("MainWindow", "40"))
        self.cbclusterBand.setItemText(5, _translate("MainWindow", "30"))
        self.cbclusterBand.setItemText(6, _translate("MainWindow", "20"))
        self.cbclusterBand.setItemText(7, _translate("MainWindow", "18"))
        self.cbclusterBand.setItemText(8, _translate("MainWindow", "15"))
        self.cbclusterBand.setItemText(9, _translate("MainWindow", "12"))
        self.cbclusterBand.setItemText(10, _translate("MainWindow", "10"))
        self.clusterMycall.setText(_translate("MainWindow", "My Call"))
        self.clusterClear.setText(_translate("MainWindow", "Clear"))
        self.rbnTable_2.setSortingEnabled(True)
        item = self.rbnTable_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Time"))
        item = self.rbnTable_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Skimmer"))
        item = self.rbnTable_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Call"))
        item = self.rbnTable_2.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Country"))
        item = self.rbnTable_2.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Freq"))
        item = self.rbnTable_2.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Band"))
        item = self.rbnTable_2.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "S/N"))
        self.rbnTab.setTabText(self.rbnTab.indexOf(self.tab_3), _translate("MainWindow", "Dx-Cluster"))
        self.cbrbnBand.setItemText(0, _translate("MainWindow", "All"))
        self.cbrbnBand.setItemText(1, _translate("MainWindow", "160"))
        self.cbrbnBand.setItemText(2, _translate("MainWindow", "80"))
        self.cbrbnBand.setItemText(3, _translate("MainWindow", "60"))
        self.cbrbnBand.setItemText(4, _translate("MainWindow", "40"))
        self.cbrbnBand.setItemText(5, _translate("MainWindow", "30"))
        self.cbrbnBand.setItemText(6, _translate("MainWindow", "20"))
        self.cbrbnBand.setItemText(7, _translate("MainWindow", "18"))
        self.cbrbnBand.setItemText(8, _translate("MainWindow", "15"))
        self.cbrbnBand.setItemText(9, _translate("MainWindow", "12"))
        self.cbrbnBand.setItemText(10, _translate("MainWindow", "10"))
        self.rbnMycall.setText(_translate("MainWindow", "My Call"))
        self.rbnClear.setText(_translate("MainWindow", "Clear"))
        self.rbnTable.setSortingEnabled(True)
        item = self.rbnTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Time"))
        item = self.rbnTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Skimmer"))
        item = self.rbnTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Call"))
        item = self.rbnTable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Country"))
        item = self.rbnTable.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Freq"))
        item = self.rbnTable.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Band"))
        item = self.rbnTable.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "S/N"))
        self.rbnTab.setTabText(self.rbnTab.indexOf(self.tab_4), _translate("MainWindow", "RBN"))

