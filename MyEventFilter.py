from PyQt5 import QtCore, QtGui, QtWidgets

class MyQSOEventFilter(QtCore.QObject):

    QSOESCAPE = QtCore.pyqtSignal(str)
    QSORETURN = QtCore.pyqtSignal(str)
    def eventFilter(self, receiver, event):
        if (event.type() == QtCore.QEvent.KeyPress):
            try:
                if event.text() == chr(27):
                    self.QSOESCAPE.emit("ESCAPE")
                    print("ESCAPE emit")
                    QtWidgets.QMessageBox.information(None, "Filtered Key Press Event!!",
                                              "Escape: " + event.text())
                if event.text() == chr(13):
                    print("RETURN emit")
                    self.QSORETURN.emit("RETURN")
            except:
                QtWidgets.QMessageBox.information(None, "Filtered Key Press Event!!",
                                              "You Pressed: " + event.text())
            return True
        else:
            # Call Base Class Method to Continue Normal Event Processing
            return super(MyQSOEventFilter, self).eventFilter(receiver, event)