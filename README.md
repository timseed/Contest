#Contest Builder

#QT Designer

QT Designer makes it easy to create a visualisation of the Gui - but adding code is a pain - especially soon as you modify the ui file all the code is lost. So the only good mechanisms are

  - Manually !! Do the lot by hand
  - Designer, and subclass

For a simple Widget I do not mind doing this manually - but my QT skills for a complex Gui are not good enough to do this manually (maybe I should just to learn them...) - so designer - then output py code, and then another class inherits from the designer code. A little more long-winded - but allows you to keep the code and the Gui seperate.



##Changing a designer Widgets into a QT5 Widget
In designer create your Gui - and then a pyuic5 convert... 



##Class Definition
change class from qso(object) to qso(QtWidgets.QWidget)

##OnSetup to init
change the OnSetup to def __init__(self,name, Parent=None ):

add

    super(QtWidgets.QWidget).__init__(parent)

## Bottom Cleanup
Remove the def _translate - and join it to the rest of the __init__ code

At bottom on Init - 

    self.layout = self.gridLayout()

##Diff Output

This will change a little depnding on your Gui - but assuming it is a simple Widget - this should be close.

In Diff format this is
11,15c3,8
< class Ui_qso(object):
<     def setupUi(self, qso):
<         qso.setObjectName("qso")
<         qso.resize(400, 300)
<         self.gridLayout_2 = QtWidgets.QGridLayout(qso)
---
> class Ui_qso(QtWidgets.QWidget):
>     def __init__(self):
>         super(QtWidgets.QWidget,self).__init__()
>         self.setObjectName("qso")
>         self.resize(400, 300)
>         self.gridLayout_2 = QtWidgets.QGridLayout(self)
17c10
<         self.widget = QtWidgets.QWidget(qso)
---
>         self.widget = QtWidgets.QWidget()
65,69c58
< 
<         self.retranslateUi(qso)
<         QtCore.QMetaObject.connectSlotsByName(qso)
< 
<     def retranslateUi(self, qso):
---
>         QtCore.QMetaObject.connectSlotsByName(self)
71d59
<         qso.setWindowTitle(_translate("qso", "Form"))


#Colors

In the past in "other" GUI's - You spend ages messing around with colors and fonts etc - it is nice to be able to place the formatting in a file and generate it as the Interface is rendered. It also allows anyone else to customize this as they desire.


#Locations
The Locations from the dxcc are in "US" Lat/long i.e. West is positive - East is Negative. I have kept the data files in their original format plus the dxcc code is the same.
i
#Mod 9

##Auto Mode

Rather a late change - this turns on and off Auto Saving - and auto sending. So if you are unplugged from the K3 - you can use this option. The buttons Save and clear are easy to press (although they should have a shortcut added to them).

##rbn
The rnm page is working nicely - it can be cleared - and also set to only show a specific band that you are interested in working. At the moment the **Call Sign** radio button does nothing - but that may change in the future.


