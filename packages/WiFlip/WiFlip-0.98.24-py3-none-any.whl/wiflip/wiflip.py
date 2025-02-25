# -*- coding: utf-8 -*-
'''
Created on 23 mars 2022


@author: garzol 
search keywords: switches reset open transparent I have a alarm1
WebEngine WebView OpenGL numpy QtTextToSpeech pickle Crazy Race index ======
signaling Fletcher console open timeout signaling error resetthe dockWidget_5 reset 
switch signal emit QTimer foo
checkBox_flag3
QPixmap
dockWidget_2
dockWidget
Bios
memTyp
sc_formatString:
close conn. thread
Dip
audio sound
signaling error settings :game
action generic
initial sound state 
waiting for host
Hi, connection to
reprog
bad format console
socket timeout
yoyo
style hostname
http://garzol.free.fr/wiflip/wiflip0_97setup.exe
rssi
super disconnect
papa myCmds settings _with_ack
actionClear socket connected
closeEvent
Reset Ack Frame print(f"val
message request is b'
print Dump Game PROM pushButton_7
Ack received DIP inputRejected
:/x/images/1x/pinballbell480.png
gridLayout_4

'''

import os, sys, time, struct
import select

from .resource_rc import *

from time import sleep
from functools import partial
from builtins import staticmethod

import requests
from bs4 import BeautifulSoup

sys.path += ['.']

#print("wiflip.py name, package", __name__,__package__)
#print("path", sys.path)
    
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#from PyQt5.QtWidgets import *   #removed 2024-10-08, (not sure)

from PyQt5.QtWidgets import QMessageBox, QAction, QLineEdit, QPushButton
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtNetwork 
#from PyQt5 import QtMultimedia 
from PyQt5.QtMultimedia import QSound
from PyQt5.QtMultimedia import QAudio
from PyQt5.QtMultimedia import QAudioDeviceInfo, QAudioFormat, QAudioOutput

from PyQt5.QtCore import QByteArray, QDataStream 
#from PyQt5.QtCore import QIODevice
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtNetwork import QHostAddress, QTcpServer

#from PyQt5.QtWebEngineWidgets import QWebEngineView
#from PyQt5 import QtNetwork, QtOpenGL 
import math

import socket

#import OpenGL.platform
#import OpenGL.platform.win32
#from OpenGL import *
#from OpenGL import GL 
from .fletcher import Fletcher
from .lwin     import Ui_MainWindow

from .about    import Ui_AboutDialog
from .help     import Ui_HelpDialog
from .settings import Ui_DialogSettings
from .reprog   import Ui_ReprogDialog
from .gameset  import Ui_GameSettings
from .wificnf  import Ui_DialogWifiC 

from .mysupervisor import MySuperv

from    .clklabel import ClkLabel


from .rscmodel import RscPin

# except:
#     from fletcher import Fletcher
#
#     from lwin     import Ui_MainWindow
#
#     from about    import Ui_AboutDialog
#     from help     import Ui_HelpDialog
#     from settings import Ui_DialogSettings
#     from reprog   import Ui_ReprogDialog
#     from gameset  import Ui_GameSettings
#     from wificnf  import Ui_DialogWifiC 
#
#     from mysupervisor import MySuperv
#
#     from    clklabel import ClkLabel
#
#
#     from rscmodel import RscPin
from  .options import MyOptions
# import sys
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

#Here is the main window   
MSGLEN = 5

aboutContent = '''
<table cellpadding="10"><tr>
<td><img src=":/x/images/aa55_logo_2.ico"/></td>
<td valign="middle"></td>
<p><span style=" font-size:18pt; font-weight:600;">%(productName)s</span></p>
<p><span style=" font-size:12pt;">%(copyright)s</span></p>
<p><span style=" font-size:12pt;">Software product from AA55</span></p>
<p><span style=" font-size:12pt;">Version %(version)s - %(date)s</span></p>
<p><span style=" font-size:10pt;">WiFlip allows user to connect to a pinball MPU and collect data from the pinball</span></p>
<p><span style=" font-size:10pt;">One can emulate Gottlieb and Recel pinball machines</span></p>
<p><span style=" font-size:10pt;">On Recel, this interface is required to replace the original miniprinter, which now became nowhere to be found</span></p>
<p><span style=" font-size:10pt;"><a href="https://www.pps4.fr">https://www.pps4.fr</a></span></p>
</td></tr></table>
'''

from .version import prodvers
print(prodvers)
VERSION = ".".join(map(str, prodvers)) #"0.95"
DATE    = "2025-02-23"
print("release date", DATE)

__version__ = VERSION
__author__ = 'garzol'
__credits__ = 'AA55 Consulting'

#Here is the about dialog box
class MyAbout(QtWidgets.QDialog):
    """
    This dialog box was created with QT
    in about.ui
    """
    def __init__(self, parent=None):
        super(MyAbout, self).__init__(parent)
        #QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        self.ui.aboutContent.setText( aboutContent % {
            'productName': 'WiFlip',
            'version'    : "V "+ VERSION,
            'date'       : DATE,
            'copyright'  : 'by AA55 Consulting'} )

#Here is the about dialog box
class MyHelp(QtWidgets.QDialog):
    """
    This dialog box was created with QT
    in help.ui
    """
    def __init__(self, parent=None):
        super(MyHelp, self).__init__(parent)
        #QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_HelpDialog()
        self.ui.setupUi(self)
        #self.ui.webEngineView.load(QtCore.QUrl.fromLocalFile('/Users/garzol/git/wiflip_tracer/index.htm'))
        self.ui.toolButton.setText(u"\u2302") #petite maison
        
        self.ui.textBrowser.append('''
<b>V0.98.2x</b> - 2025-02-23<br>Hidden changes in the machinery to make SW compatible with package structure<br>
Improvement in the communication thread at disconnection/connection (we don't kill the thread abruptly any more<br>
wiflip can now be downloaded through pip with pip install wiflip. Then you can run the application by calling <i>wiflip-zero</i><br><br>
<b>V0.98.7.0</b> - 2025-02-22<br>Internal cleanings of the package to prepare it for pypi<br><br>
<b>V0.98.0.0</b> - 2025-02-02<br>Supervisor mode added for compatible devices<br>
Font for RSSI corrected<br>
Retry on connection losses improved<br>
<b>V0.97.0.1</b> - 2025-01-24<br>Bug fixes in game settings. <br>Factory settings will dim option checkboxes.<br><br>
<b>V0.96</b> - 2024-12-11<br>moved game binary files. Added RSSI display on compatible devices<br><br>
<b>V0.95</b> - 2024-11-28<br>Version Signed.<br><br>
<b>V0.94</b> - 2024-11-17<br>Bug fix on game settings for params such as handicaps 1 where user enters 10 instead of 00010 for example. <br>
Added settings for coil protection circuitry.<br>
Added triple click on switches in order to close a switch permanently.
 <br><br>
<b>V0.93</b> - 2024-11-11<br>Reprog full operational. (Except PokerPlus, which hangs up) <br><br>
<b>V0.92</b> - 2024-10-08<br>Reprog works only with compatible boards.VB_MG.<br><br>
<b>V0.91</b> - 2024-10-08<br>Added the small leds per player score + The 1M digit. The only missing display indication is the set of decimal points at the moment. Lighter EXE. calques for Switch matrix are now memorized in app settings<br><br>
<b>V0.89</b> - 2024-10-06<br>scorie corrections<br><br>
<b>V0.88</b> - 2024-10-02<br>Removed several unused lib. for the exe file<br><br>
<b>V0.87</b> - 2024-09-19<br>Added game settings. Improved initial layout<br><br>
<b>V0.86</b> - 2024-09-19<br>Added sound (experimental). Improved initial layout<br><br>
<b>V0.80</b><br>correction of bug when loading nvr data file was not actually sending data<br><br>
<b>V0.78</b><br>original version<br>
'''
)

        cursor = self.ui.textBrowser.textCursor()
        cursor.setPosition(0);
        self.ui.textBrowser.setTextCursor(cursor);   
             
        self.ui.textBrowser_2.setSource(QtCore.QUrl('qrc:/help/docs/index.htm'))
        #self.ui.textBrowser_2.setSource(QtCore.QUrl('index.htm'))
   
        self.ui.textBrowser_2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.textBrowser_2.customContextMenuRequested.connect(self.emptySpaceMenu)
        self.ui.toolButton.clicked.connect(self.home)
        self.ui.toolButton_3.clicked.connect(self.backward)
        self.ui.toolButton_2.clicked.connect(self.forward)
        
    def emptySpaceMenu(self):
        menu = QtWidgets.QMenu()
        FA = QAction('Forward')
        FB = QAction('Backward')
        FH = QAction('Home')
        
        menu.addAction(FA)
        menu.addAction(FB)
        menu.addAction(FH)
        FA.triggered.connect(self.forward)
        FB.triggered.connect(self.backward)
        FH.triggered.connect(self.home)
        menu.exec_(QtGui.QCursor.pos())
    
    def forward(self):
        self.ui.textBrowser_2.forward()
        
    def backward(self):
        self.ui.textBrowser_2.backward()
        
    def home(self):
        self.ui.textBrowser_2.home()
        
    def closeEvent(self, event):
        #print("closing help")
        # Finally we pass the event to the class we inherit from. It can choose to accept or reject the event, but we don't need to deal with it ourselves
        self.parent().myhelp = None
        super(MyHelp, self).closeEvent(event)

        
        
class MyGameSet(QtWidgets.QDialog): 
    """
    Obsolete. Look at options 
    This dialog box was created with QT
    in gameset.ui
    """
    def __init__(self, parent=None):
        super(MyGameSet, self).__init__(parent)
        #QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_GameSettings()
        self.ui.setupUi(self)

        _translate = QtCore.QCoreApplication.translate

        self.widget1fp = QSpinBox()
        self.widget1fp.setValue(65)
        self.widget1fp.setMinimum(0)
        self.widget1fp.setMaximum(99)
        
        self.widget2fp = QSpinBox()
        self.widget2fp.setValue(82)
        self.widget2fp.setMinimum(0)
        self.widget2fp.setMaximum(99)
        
        self.widgeteb = QSpinBox()
        self.widgeteb.setValue(44)
        self.widgeteb.setMinimum(0)
        self.widgeteb.setMaximum(99)
        
        #self.treeWidget.topLevelItem(0).setText(0, _translate("GameSettings", "Basics"))
        #self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("GameSettings", "Production N°"))
        self.ui.treeWidget.topLevelItem(0).setExpanded(True)
        self.ui.treeWidget.topLevelItem(1).setExpanded(True)
        self.ui.treeWidget.topLevelItem(2).setExpanded(True)
        #self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("GameSettings", "Model N°"))
        # self.treeWidget.topLevelItem(0).child(2).setText(0, _translate("GameSettings", "Serial N° of Printer"))
        # self.treeWidget.topLevelItem(0).child(3).setText(0, _translate("GameSettings", "Credit limit"))
        # self.treeWidget.topLevelItem(1).setText(0, _translate("GameSettings", "Score threshold"))
        # self.treeWidget.topLevelItem(1).child(0).setText(0, _translate("GameSettings", "1st freeplay"))
        # self.treeWidget.topLevelItem(1).child(1).setText(0, _translate("GameSettings", "2nd freeplay"))
        # self.treeWidget.topLevelItem(1).child(2).setText(0, _translate("GameSettings", "Extra ball"))
        # self.treeWidget.topLevelItem(2).setText(0, _translate("GameSettings", "Initial contents"))
        # self.treeWidget.topLevelItem(2).child(0).setText(0, _translate("GameSettings", "#Credit"))
        # self.treeWidget.topLevelItem(2).child(1).setText(0, _translate("GameSettings", "#Free play"))
        # self.treeWidget.topLevelItem(2).child(2).setText(0, _translate("GameSettings", "#Extra ball"))
        # self.treeWidget.topLevelItem(3).setText(0, _translate("GameSettings", "Game variant"))
        # self.treeWidget.topLevelItem(3).child(0).setText(0, _translate("GameSettings", "Adj. Play"))
        self.ui.treeWidget.setItemWidget(self.ui.treeWidget.topLevelItem(1).child(0), 1, self.widget1fp)
        self.ui.treeWidget.setItemWidget(self.ui.treeWidget.topLevelItem(1).child(1), 1, self.widget2fp)
        self.ui.treeWidget.setItemWidget(self.ui.treeWidget.topLevelItem(1).child(2), 1, self.widgeteb)

        #self.ui.treeWidget.topLevelItem(0).child(0).setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled )
        #self.ui.treeWidget.setItemWidget(self.ui.treeWidget.topLevelItem(0).child(0), 1, self.widgetmdl)
        self.ui.treeWidget.topLevelItem(0).child(0).triggered.connect(self.pipo)    
            #self.ui.treeWidget.setItemWidget(item, 1, widget)
        
    def pipo(self, ev):
        print("pipo", ev)
      
class MyReprog(QtWidgets.QDialog): 
    """
    This dialog box was created with QT
    in reprog.ui
    """
    cA1762Org_Fltch = 0x4685
    cA1762Mod_Fltch = 0xDC38
    
    def __init__(self, parent=None):
        super(MyReprog, self).__init__(parent)
        #QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ReprogDialog()
        self.ui.setupUi(self)

        self.nb_call = 0

        self.ui.radioButton.setChecked(True)
        self.ui.radioButton.clicked.connect(partial(self.selmemtyp, 0))
        self.ui.radioButton_2.clicked.connect(partial(self.selmemtyp, 1))

        #get status
        papa = self.parent()
        papa.read128Sig.connect(self.catch128SigReprog)

        self.ui.comboBox.addItems(list(RscPin.Models.keys()))

        #we should set the call back to reset with ack
        #but we won't because it is full manual, we want to keep full control
        #step by step 
        self.ui.toolButton_reset_2.clicked.connect(self.resetthepin)
        self.ui.toolButton_reprog.clicked.connect(self.gotoreprog)
        self.ui.toolButton_write.clicked.connect(self.actionLoadPROM)
        self.ui.toolButton_read.clicked.connect(self.actionReadPROM)
        #flash
        self.ui.toolButton_flash.clicked.connect(self.send_reqflash)
        #fletcher
        self.ui.toolButton_fletcher.clicked.connect(self.send_reqfletcher)
        
        #Apply button
        self.ui.pushButton.clicked.connect(self.start_reprog)

        #Reset button in the group Auto
        self.ui.pushButton_2.clicked.connect(papa.resetthepin_with_ack)


        self.ui.buttonBox.accepted.connect(self.close_callback)
        self.ui.buttonBox.rejected.connect(self.close_callback)


        self.ui.label_crc_cg.setText("????")
        self.ui.label_crc_rg.setText("????")
        self.ui.label_crc_cr.setText("????")
        self.ui.label_crc_rr.setText("????")

        self.ui.label_txt_cg.setText("")
        self.ui.label_txt_rg.setText("")
        self.ui.label_txt_cr.setText("")
        self.ui.label_txt_rr.setText("")
        self.refreshReprog()
        
    def refreshReprog(self):
        papa = self.parent()
        self.fletcherSrc = -1
        self.reprogPhase = 0
        self.memTyp = 0 #game prom by default


        memtyp = 0 + 0 #sys config
        papa.ui.rb_sysconf.setChecked(True)  #we expect the others to turn unchecked...
        print("message request is", b'YR'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            papa.thread.sock.send(b'YR'+memtyp.to_bytes(1, byteorder='big')+b'XX')
        except:
            pass
            print("read sys conf area failed")

    def catch128SigReprog(self, memTypStr):
        #print("catch128SigReprog memTyp", memTypStr)
        papa = self.parent()
        
        #game
        rg = papa.nvrlist[2*8+1][1]*256+papa.nvrlist[2*8+0][1]
        cg = papa.nvrlist[3*8+1][1]*256+papa.nvrlist[3*8+0][1]

        #rom
        rr = papa.nvrlist[4*8+1][1]*256+papa.nvrlist[4*8+0][1]
        cr = papa.nvrlist[5*8+1][1]*256+papa.nvrlist[5*8+0][1]

        self.ui.label_crc_cg.setText(f"{cg:04X}")
        self.ui.label_crc_rg.setText(f"{rg:04X}")
        self.ui.label_crc_cr.setText(f"{cr:04X}")
        self.ui.label_crc_rr.setText(f"{rr:04X}")
        
        #find all keys with such fletcher's
        try:
            crtxt = RscPin.Bios[cr][1]
        except:
            crtxt = "Unknown" 
        try:
            rrtxt = RscPin.Bios[rr][1]
        except:
            rrtxt = "Unknown" 
            
            
            
        self.ui.label_txt_cr.setText(crtxt)
        self.ui.label_txt_rr.setText(rrtxt)
        
        candidates_cg =  [x for x in RscPin.Models.keys() if RscPin.Models[x]["Game Fletcher"]==cg ]
        candidates_rg =  [x for x in RscPin.Models.keys() if RscPin.Models[x]["Game Fletcher"]==rg ]        
        
        self.ui.label_txt_cg.setText("/".join(candidates_cg) if len(candidates_cg)>0 else "Unknown" )                    
        self.ui.label_txt_rg.setText("/".join(candidates_rg) if len(candidates_rg)>0 else "Unknown" )

        self.ui.label_txt_cr.setText(crtxt)
        self.ui.label_txt_rr.setText(rrtxt)

        if self.nb_call == 0:        
            if rr != cr:
                self.ui.plainTextEdit.appendPlainText("Game ROM: Executing Factory (Mod A1762 from HW with 2716)")
            if rg != cg:
                self.ui.plainTextEdit.appendPlainText("Base ROM: Executing Factory (Crazy Race)")
        self.nb_call += 1
        
    def start_reprog(self):
        papa = self.parent()
        self.ui.plainTextEdit.clear()

        self.gameName = self.ui.comboBox.currentText()
        gameFileName  = RscPin.Models[self.gameName]["Game bin"]
        binGame  = QFile(":/games/rs3bin/"+gameFileName)
        if not binGame.open(QIODevice.ReadOnly):
            self.ui.plainTextEdit.appendPlainText(f"{gameFileName} not found.")
            return
        totalGBytes = binGame.size()
        streamG = QDataStream(binGame)
        
        #filecont = QByteArray()
        bn = streamG.readRawData(totalGBytes)
        self.ui.plainTextEdit.appendPlainText(f"Game name: {self.gameName}")
        self.ui.plainTextEdit.appendPlainText(f"Game binary file: {gameFileName} ({totalGBytes} bytes)")
        print("message request is", b'YBXQR')
        try:
            papa.thread.sock.send(b'YBXQR')
            self.ui.plainTextEdit.appendPlainText(f"Set reprog mode.. OK")
        except:
            self.ui.plainTextEdit.appendPlainText(f"Set reprog mode... KO")
            #return
        
        cbytFill = b'\x81'
        dstBin4Fltch = QByteArray()
        dstBin4Fltch.resize(1024)
        dstBin4Fltch.fill(cbytFill)
        myBuffer = QBuffer(dstBin4Fltch)
        myBuffer.open(QIODevice.ReadWrite)
        st=QDataStream(myBuffer)
        bnb = st.readRawData(myBuffer.size())
        myBuffer.seek(0)
        time.sleep(0.1) #to let time for the previous command to execute
        addr = 0
        memtyp = 4  #game prom
        for byte in bn:
            #the high part of addr (0xhll) is to be put on the high nibble
            #of the first param byte... >>8, then <<4 <==> >>4
            addrh  = (addr >> 4)&0xF0 
            b1     = addrh|memtyp
            bb1    = b1.to_bytes(1, byteorder='big')
            bbyt   = byte.to_bytes(1, byteorder='big')
            baddrl = (addr&0xFF).to_bytes(1, byteorder='big')

            myBuffer.write(bbyt)
            print("message request is", b'YW'+bb1+baddrl+bbyt)

            try:
                papa.thread.sock.send(b'YW'+bb1+baddrl+bbyt)
            except:
                pass
                #return
            addr += 1

        #Let's complete to 1024 bytes, if necessary
        more2feed = 1024-totalGBytes
        if more2feed > 1024 or more2feed < 0:
            self.ui.plainTextEdit.appendPlainText(f"Error.Incorrect game file size ({totalGBytes} bytes). Abort.")
            return
        for i in range(1024-totalGBytes):
            #the high part of addr (0xhll) is to be put on the high nibble
            #of the first param byte... >>8, then <<4 <==> >>4
            addrh  = (addr >> 4)&0xF0 
            b1     = addrh|memtyp
            bb1    = b1.to_bytes(1, byteorder='big')
            bbyt   = cbytFill
            baddrl = (addr&0xFF).to_bytes(1, byteorder='big')
            print("message request is", b'YW'+bb1+baddrl+bbyt)

            try:
                papa.thread.sock.send(b'YW'+bb1+baddrl+bbyt)
            except:
                pass
                #return
            addr += 1
              
        #self.fletcherSrc = fletcher = Fletcher(bn)
        self.fletcherSrc = fletcher = Fletcher(dstBin4Fltch)
        
        self.reprogPhase = 0

        self.ui.plainTextEdit.appendPlainText(f"Sent Binary Game. Fletcher's: {fletcher.crc}")
            
        papa.fletcherSig.connect(self.catchFletcherSigAuto)

        time.sleep(0.1) #to let time for the previous command to execute

        memtyp = 4  #game prom    
        #Must send the number of bits to be checked (power of 2)
        #which is always 1K in game prom (empty loc padded with 0x81...)
        #dataLength = (totalGBytes-1).bit_length() 
        dataLength = (1024-1).bit_length()
        if dataLength > 10 or dataLength <= 0:
            self.ui.plainTextEdit.appendPlainText(f"File size error: {gameFileName} ({totalGBytes} bytes)")
            dataLength = 0
        dl = dataLength.to_bytes(1, byteorder='big')             
        print("message request is", b'YZ'+memtyp.to_bytes(1, byteorder='big')+dl+b'X')

        try:
            papa.thread.sock.send(b'YZ'+memtyp.to_bytes(1, byteorder='big')+dl+b'X')
        except:
            pass

        self.timertout = QTimer(singleShot=True, timeout=self.timeoutt)
        self.timertout.start(5000)
        
    def timeoutt(self):
        #print("Time out")
        dlg = QMessageBox(self.parent())
        dlg.setWindowTitle("NAck")
        dlg.setText("Time out. No ack. Please, check connection")
        dlg.setIcon(QMessageBox.Critical)
        button = dlg.exec()

        if button == QMessageBox.Ok:
            self.ui.plainTextEdit.appendPlainText(f"Fletcher Check process failed: Device not responding.")

        

    def catchFletcherSigAuto(self, crc):
        papa = self.parent()
        papa.fletcherSig.disconnect(self.catchFletcherSigAuto)
        self.timertout.stop()
        print("caught fletchers", f"{crc:04X}")
        crcs = f"{crc:04X}"
        self.ui.plainTextEdit.appendPlainText(f"Check Fletcher: {self.fletcherSrc.crc}/{crcs}")
        if self.fletcherSrc.crc != crcs:
            self.ui.plainTextEdit.appendPlainText(f"Fletcher check failed")                                      
            return 
        
        #OK we just need to flash now
        if self.reprogPhase == 0:
            memtyp = 4      
        else:
            memtyp =5      
        print("message request is", b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            papa.thread.sock.send(b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')
        except:
            pass
            #return
        
        if self.reprogPhase == 0:
            txt = "Game"      
        else:
            txt = "ROM 1K"      
        self.ui.plainTextEdit.appendPlainText(f"{txt} flashed")
        time.sleep(0.2) #to let time for the previous command to execute

        #write the crc
        memtyp = 0
        if self.reprogPhase == 0:
            addr = 16      
        else:
            addr = 32      
        byte = crc&0xFF 
        bbyt = byte.to_bytes(1, byteorder='big')
        baddr = addr.to_bytes(1, byteorder='big')
        print("message request is", b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
        try:
            papa.thread.sock.send(b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
        except:
            pass
            #return
        addr += 1
        byte = (crc&0xFF00)>>8 
        bbyt = byte.to_bytes(1, byteorder='big')
        baddr = addr.to_bytes(1, byteorder='big')
        print("message request is", b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
        try:
            papa.thread.sock.send(b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
        except:
            pass
            #return

        time.sleep(0.1) #to let time for the previous command to execute
        
        #OK we just need to flash now
        memtyp = 0            
        print("message request is", b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            papa.thread.sock.send(b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')
        except:
            pass
            #return
        self.ui.plainTextEdit.appendPlainText(f"Fletcher's updated in sys config")

        time.sleep(0.2) #to let time for the previous command to execute
        
        self.reprogPhase += 1
        
        if self.reprogPhase == 1:
            A1762FileName = RscPin.Models[self.gameName]["A1762 bin"]
            binA1762 = QFile(":/games/rs3bin/"+A1762FileName)
            if not binA1762.open(QIODevice.ReadOnly):
                self.ui.plainTextEdit.appendPlainText(f"{A1762FileName} not found.")
                return
            totalRBytes = binA1762.size()
            streamR = QDataStream(binA1762)
            br = streamR.readRawData(totalRBytes)
            self.ui.plainTextEdit.appendPlainText(f"B2 ROM binary file: {A1762FileName} ({totalRBytes} bytes)")
            addr = 0
            memtyp = 5  #A1762 prom
            for byte in br:
                #the high part of addr (0xhll) is to be put on the high nibble
                #of the first param byte... >>8, then <<4 <==> >>4
                addrh  = (addr >> 4)&0xF0 
                b1     = addrh|memtyp
                bb1    = b1.to_bytes(1, byteorder='big')
                bbyt   = byte.to_bytes(1, byteorder='big')
                baddrl = (addr&0xFF).to_bytes(1, byteorder='big')
                print("message request is", b'YW'+bb1+baddrl+bbyt)
    
                try:
                    papa.thread.sock.send(b'YW'+bb1+baddrl+bbyt)
                except:
                    pass
                    #return
                addr += 1
            
            
            self.fletcherSrc = fletcher = Fletcher(br)
            #self.reprogPhase = 1
    
            self.ui.plainTextEdit.appendPlainText(f"Sent Binary A1762. Fletcher's: {fletcher.crc}")
                
            papa.fletcherSig.connect(self.catchFletcherSigAuto)
    
            time.sleep(0.1) #to let time for the previous command to execute
    
            memtyp = 5  #Rom prom            
            #Must send the number of bits to be checked (power of 2)
            dataLength = (totalRBytes-1).bit_length() 
            if dataLength > 10 or dataLength <= 0:
                self.ui.plainTextEdit.appendPlainText(f"File size error: {A1762FileName} ({totalRBytes} bytes)")
                dataLength = 0
            dl = dataLength.to_bytes(1, byteorder='big')             

            print("message request is", b'YZ'+memtyp.to_bytes(1, byteorder='big')+dl+b'X')
    
            try:
                papa.thread.sock.send(b'YZ'+memtyp.to_bytes(1, byteorder='big')+dl+b'X')
            except:
                pass
    
            self.timertout = QTimer(singleShot=True, timeout=self.timeoutt)
            self.timertout.start(5000)
            
        elif self.reprogPhase == 2:

            time.sleep(0.1) #to let time for the previous command to execute
 
            #write the model number
            
            memtyp = 1 #NVRAM
            addr = 0x12  
            model = RscPin.Models[self.gameName]["#Model"]   
            for i in range(1,-1,-1):
                try: 
                    byte = (int(model[2*i], 16)<<4)+int(model[2*i+1], 16)
                except:
                    byte = 15
                bbyt = byte.to_bytes(1, byteorder='big')
                baddr = addr.to_bytes(1, byteorder='big')
                print("message request is", b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
                try:
                    papa.thread.sock.send(b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
                except:
                    pass
                    #return
                addr += 1
                                        
            time.sleep(0.1) #to let time for the previous command to execute
            
            #OK we just need to flash now
            memtyp = 1            
            print("message request is", b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')
    
            try:
                papa.thread.sock.send(b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')
            except:
                pass
                #return
            self.ui.plainTextEdit.appendPlainText(f"Model number updated in NVRAM : {model}")
    
            time.sleep(0.2) #to let time for the previous command to execute
                       
            
            
            
            
            self.ui.plainTextEdit.appendPlainText(f"Process successfully terminated.")
            self.ui.plainTextEdit.appendPlainText(f"Please, reset the pin and close this window to get the modifications applied.")
            self.refreshReprog()
            
        
    def catchFletcherSig(self, crc):
        #print("caught fletchers", f"{crc:04X}")
        self.ui.label_crc_3.setText(f"{crc:04X}")
        
    def send_reqfletcher(self):
        papa = self.parent()

        papa.fletcherSig.connect(self.catchFletcherSig)
        memtyp = 4+self.memTyp            
        totalBytes = 1024
        #Must send the number of bits to be checked (power of 2)
        dataLength = (totalBytes-1).bit_length() 
        if dataLength > 10 or dataLength <= 0:
            self.ui.plainTextEdit.appendPlainText(f"File size error in fletcher request. Data length {totalBytes}")
            dataLength = 0
        dl = dataLength.to_bytes(1, byteorder='big')             
        
        print("message request is", b'YZ'+memtyp.to_bytes(1, byteorder='big')+dl+b'X')

        try:
            papa.thread.sock.send(b'YZ'+memtyp.to_bytes(1, byteorder='big')+dl+b'X')
        except:
            pass
        
        
    def send_reqflash(self):
        papa = self.parent()

        memtyp = 4+self.memTyp            
        print("message request is", b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            papa.thread.sock.send(b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')
        except:
            pass
        time.sleep(0.2) #to let time for the previous command to execute
                        
    def selmemtyp(self, m):
        self.memTyp = m   
        #print("memtyp selected", m) 
        
    def gotoreprog(self):
        papa = self.parent()
        print("message request is", b'YBXQR')
        try:
            papa.thread.sock.send(b'YBXQR')
        except:
            pass
        
    def resetthepin(self):
        papa = self.parent()
        print("message request is", b'YBXQZ')
        try:
            papa.thread.sock.send(b'YBXQZ')
        except:
            pass

        time.sleep(2.5)

        self.frameCnt = 0
        
        #self.frameCntSig.connect(self.frameCounter)

        self.refreshReprog()

    
    def actionReadPROM(self):
        papa = self.parent()
        memtyp = 4 + self.memTyp
        print("message request is", b'YR'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            papa.thread.sock.send(b'YR'+memtyp.to_bytes(1, byteorder='big')+b'XX')
        except:
            pass
        
                
    def actionLoadPROM(self):
        papa = self.parent()
        nvrfileStr = papa.settings.value('binfileStr', None)
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load File",
                                       nvrfileStr,
                                       "Raw binary prog file (*.bin)")

        if filename:
            papa.settings.setValue("binfileStr", filename)
            with open(filename, "rb") as fb:
                # read contents      
                bn = fb.read()
            
            #print("file length", len(bn))

            if len(bn) == 1024:
                addr = 0
                memtyp = 4 + self.memTyp
                for byte in bn:
                    #the high part of addr (0xhll) is to be put on the high nibble
                    #of the first param byte... >>8, then <<4 <==> >>4
                    addrh  = (addr >> 4)&0xF0 
                    b1     = addrh|memtyp
                    bb1    = b1.to_bytes(1, byteorder='big')
                    bbyt   = byte.to_bytes(1, byteorder='big')
                    baddrl = (addr&0xFF).to_bytes(1, byteorder='big')
                    print("message request is", b'YW'+bb1+baddrl+bbyt)
    
                    try:
                        papa.thread.sock.send(b'YW'+bb1+baddrl+bbyt)
                    except:
                        pass
                    addr += 1
                fletcher = Fletcher(bn)
                #print("fletcher's crc:", fletcher.crc)
                self.ui.label_crc.setText(fletcher.crc)
                self.ui.label_error.setText(f"{filename} loaded.")
            
            elif len(bn) == 256:    
                addr = 0
                memtyp = 4 + self.memTyp
                for byte in bn:
                    bbyt = byte.to_bytes(1, byteorder='big')
                    baddr = addr.to_bytes(1, byteorder='big')
                    print("message request is", b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
    
                    try:
                        papa.thread.sock.send(b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
                    except:
                        pass
                    addr += 1
                fletcher = Fletcher(bn)
                #print("fletcher's crc:", fletcher.crc)
                self.ui.label_crc.setText(fletcher.crc)
                self.ui.label_error.setText(f"{filename} loaded.")

            else:
                #print("length  error")
                self.ui.label_error.setText("file length error")
                self.ui.label_crc.setText("")


    def closeEvent(self, event):
        self.close_callback()
        QtWidgets.QDialog.closeEvent(self, event)

    
    def close_callback(self):
        #print("guguguuu")
        papa = self.parent()
        
        papa.read128Sig.disconnect(self.catch128SigReprog)
                        
        
class MyWIFICnf(QtWidgets.QDialog): 
    """
    This dialog box was created with QT
    in wificnf.ui
    This is wifi initial config dialog box, such as type of start factory/normal/miniprinter
    """
    errorVerTxt = \
"""
Currently connected WiFlip device is incompatible with this app.
Versions incompatible.
Either update the wiflip device, or 
configure the device with your usual web browser, going to:
http://192.168.4.22
"""
    errorConnTxt = \
"""
You are not connected to a WiFlip device, or 
the connection is too weak. Please, check that 
you are connected to the right WiFlip AP you think you are 
and retry to configure it.
"""
    errorConfTxt = \
"""
Can't connect to WiFlip AP. Are you sure 
that's your computer is connected to an AP with a name like
WIFLIP_xyzt?
Try moving your computer closer to the WiFlip device.
Try switching the WiFlip device off and on several times.
Try to stop and restart your computer's wifi.
Press the reload button of the dialog window, when you think you are ready, to retry the connection process.
"""
    #statusCmd = pyqtSignal(int, str)
    def __init__(self, parent=None):
        super(MyWIFICnf, self).__init__(parent)
        #QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_DialogWifiC()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.reload)
        self.ui.pushButton_2.clicked.connect(self.postdata)
        
        self.ui.label_ret1.setText("")
        self.ui.label_ret2.setText("")
        self.ui.label_1.setText("")
        self.ui.label_2.setText("")
        self.ui.label_3.setText("")
        self.ui.groupBox.setTitle("")
        
        self.ui.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.checkBox.stateChanged.connect(self.setpwdmask)

        self.reload()
        
    def reload(self):
        self.ui.pushButton_2.setEnabled(False)
        try:
            cnf_pg = requests.get("http://192.168.4.22")
            print("status", cnf_pg.status_code)
        except:
            dlg = QMessageBox(self.parent())
            dlg.setWindowTitle("WiFlip Network Connection")
            
            #dlg.setText("No connection.")
            dlg.setText(self.errorConfTxt)
            dlg.setIcon(QMessageBox.Warning)
            dlg.exec()
            return
        if cnf_pg.status_code != 200:
            self.ui.label_3.setText(f"http error code: {cnf_pg.status_code}")
        else:
            self.ui.label_3.setText(f"")
            
            
        soup = BeautifulSoup(cnf_pg.text, 'html.parser')
        mytitle   = soup.find_all("h1")
        myssid    = soup.find(id="ssid")
        myport    = soup.find(id="portn")
        myiplo    = soup.find(id="iploc")
        mymacaddr = soup.find(id="macaddr-txt")
        
        
        if not len(mytitle):
            dlg = QMessageBox(self.parent())
            dlg.setWindowTitle("WiFlip Network Communication Error")
            
            #dlg.setText("No connection.")
            dlg.setText(self.errorConnTxt)
            dlg.setIcon(QMessageBox.Warning)
            dlg.exec()
            return
            
        
        try:
            myssid = myssid.get("value")
        except:
            myssid = None 
            
        try:
            myport = myport.get("value")
        except:
            myport = None 
            
        try:
            myiplo = myiplo.text
        except:
            myiplo = None 
            
        try:
            mymacaddr = mymacaddr.text
        except:
            mymacaddr = None 
            
        if myssid is None or myport is None or myiplo is None or mymacaddr is None:
            #incompatible version
            self.ui.groupBox.setTitle("Incompatible device")
            self.ui.label_1.setText(f"ssid: {myssid} mac addr: {mymacaddr}")
            self.ui.label_2.setText(f"iplocal: {myiplo} port: {myport}")

            #device version
            if myssid is not None and myport is not None and myiplo is not None and mymacaddr is None:
                dlg = QMessageBox(self.parent())
                dlg.setWindowTitle("WiFlip Network Communication Error")
                
                #dlg.setText("No connection.")
                dlg.setText(self.errorVerTxt)
                dlg.setIcon(QMessageBox.Warning)
                dlg.exec()

            return
            
        if not len(mytitle):
            mytitle = "Unknown version of configurator"
        else:
            mytitle = mytitle[0]
        #print("mydata", mytitle.text, myssid.get("value"), myport.text, myiplo.text)

        self.ui.label_1.setText(f"Mac: {mymacaddr}")
        self.ui.label_2.setText("")
        self.ui.label_3.setText("")
        
        self.ui.groupBox.setTitle(mytitle.text)
        self.ui.lineEdit.setText(myssid)
        self.ui.lineEdit_3.setText(myport)
        self.ui.label_ret1.setText(f"Current IP: {myiplo}")
        self.ui.label_ret2.setText(f"Current port: {myport}")
        self.ui.label_ret1.setTextInteractionFlags(Qt.TextSelectableByMouse) 

        self.ui.pushButton_2.setEnabled(True)
        
    def setpwdmask(self):
        if self.ui.checkBox.isChecked():
            self.ui.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.ui.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)
        
            
    def postdata(self):
        url = "http://192.168.4.22/config_page"
        myobj = {
            "ssid"    : self.ui.lineEdit.text(),
            "pwd"     : self.ui.lineEdit_2.text(),
            "portn"   : self.ui.lineEdit_3.text(),
            "showpwd" : "xxx",
            }

        #print(myobj)
        
        QtWidgets.QApplication.setOverrideCursor(Qt.BusyCursor)

        ret = requests.post(url, data = myobj)

        # do lengthy process 
        QtWidgets.QApplication.restoreOverrideCursor()

        #print(ret.status_code, ret.text)
        if ret.status_code != 200:
            self.ui.label_3.setText(f"http error code: {ret.status_code}")
        else:
            self.ui.label_3.setText(f"")
            soup         = BeautifulSoup(ret.text, 'html.parser')
            myresponse   = soup.find_all("h1")[0]
            myresponse2  = soup.find_all("p")[0]
            #self.ui.label_ret1.setText(f"{myresponse} {myresponse2}")
            self.ui.label_ret1.setText(ret.text)
            self.ui.label_ret2.setText(f"Current port: {myobj['portn']}")
                
        
        
class MySettings(QtWidgets.QDialog): 
    """
    This dialog box was created with QT
    in settings.ui
    This is system settings dialog box, such as type of start factory/normal/miniprinter
    Warning: This is not game settings
    """
    #statusCmd = pyqtSignal(int, str)
    def __init__(self, parent=None):
        super(MySettings, self).__init__(parent)
        #QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_DialogSettings()
        self.ui.setupUi(self)

        self.ui.label.setText("")
        
        self.flags=[self.ui.checkBox_flag0, self.ui.checkBox_flag1, self.ui.checkBox_flag2, self.ui.checkBox_flag3,
                    self.ui.checkBox_flag4, self.ui.checkBox_flag5, self.ui.checkBox_flag6, self.ui.checkBox_flag7]

       
        
        self.ui.toolButton_reset.clicked.connect(self.resetthepin)
        self.ui.toolButton.setVisible(False)
        self.ui.toolButton_2.setVisible(False)
        

        self.refreshdlg()
        
        
        
    def refreshdlg(self):
        #select sys config
        memtyp = 0
        papa = self.parent()
        papa.ui.rb_sysconf.setChecked(True)  #we expect the others to turn unchecked...
        self.ui.label.setText("Loading...")
        
        print("message request is", b'YR'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            papa.thread.sock.send(b'YR'+memtyp.to_bytes(1, byteorder='big')+b'XX')
        except:
            dlg = QMessageBox(self.parent())
            dlg.setWindowTitle("Network")
            dlg.setText("No connection.")
            dlg.setIcon(QMessageBox.Warning)
            dlg.exec()
            self.ui.label.setText("Not connected")
            
            self.ui.groupBox.setDisabled(True)
            self.ui.groupBox_2.setDisabled(True)


        self.timertout = QTimer(singleShot=True, timeout=self.timeoutt)
        self.timertout.start(5000)
        try:
            papa.read128Sig.disconnect(self.cmdDone)
            #self.statusCmd.disconnect(self.cmdDone)
        except:
            pass   
        #self.statusCmd.connect(self.cmdDone)   
        papa.read128Sig.connect(self.cmdDone)
        #next lines to emulate the thing
        self.timerpipo = QTimer(singleShot=True, timeout=self.fpipo)
        self.timerpipo.start(4000)
              
        
        
    def gotoreprog(self):
        papa = self.parent()
        print("message request is", b'YBXQR')
        try:
            papa.thread.sock.send(b'YBXQR')
        except:
            pass
        
    def resetthepin(self):
        '''
        reset with ack
        '''
        papa = self.parent()
        papa.resetAckSig.connect(self.catchResetSig)
        print("message request is", b'YCXQZ')
        try:
            papa.thread.sock.send(b'YCXQZ')
        except:
            pass
        self.timertout2 = QTimer(singleShot=True, timeout=self.timeoutt)
        self.timertout2.start(5000)
        
        #self.refreshdlg()
    
    def catchResetSig(self):   
        '''
        reset ack was received, we can continue
        '''
        #print("catchResetSig")
        papa = self.parent()
        papa.resetAckSig.disconnect(self.catchResetSig)
        self.timertout2.stop()    
        time.sleep(1.5)    
        self.refreshdlg()
        
    def modscr(self):
        sc_mode = 0
        

        if self.ui.radioButton_startmnprn.isChecked():
            sc_mode = 1
            self.ui.groupBox_2.setEnabled(True)
        elif self.ui.radioButton_startnormal.isChecked():
            sc_mode = 2
            self.ui.groupBox_2.setEnabled(True)
        else:
            #disable the option settings box
            self.ui.groupBox_2.setEnabled(False)
            
        #print("yoyo0", sc_mode)

        papa = self.parent()
        
        memtyp = 0
        addr   = 3
        bbyt   = sc_mode
        baddr = addr.to_bytes(1, byteorder='big')
        bbyt = bbyt.to_bytes(1, byteorder='big')
        print("message request is", b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
        try:
            papa.thread.sock.send(b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
        except:
            pass
        
        time.sleep(0.1) #to let time for the previous command to execute
    
        print("message request is", b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            papa.thread.sock.send(b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')
        except:
            pass
        
        time.sleep(0.2) #to let time for the previous command to execute
             
    def modsc(self):
        sc_flags1 = 0
        for i in range(8):
            sc_flags1 |= ((1 if (self.flags[i].isChecked()==True) else 0)<<i)

        #print("modsc called", sc_flags1, self)
        

        papa = self.parent()

        memtyp = 0
        addr   = 4
        bbyt   = sc_flags1
        baddr = addr.to_bytes(1, byteorder='big')
        bbyt = bbyt.to_bytes(1, byteorder='big')
        print("message request is", b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
        try:
            papa.thread.sock.send(b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
        except:
            pass
            
        print("message request is", b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            papa.thread.sock.send(b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')
        except:
            pass
                
        time.sleep(0.4) #to let time for the previous command to execute
                        #to be changed when ack will be implemented
               
    def cmdDone(self, memTypStr):
        #print("Sys settings cmdDone memTyp", memTypStr)
        if memTypStr != "sys conf":
            return  
        #print("nvr read done")
        self.timertout.stop()
        papa = self.parent()

        
        if memTypStr == "sys conf" and papa.ui.rb_sysconf.isChecked():
            #self.ui.groupBox.stateChanged.connect(self.test)
            for cb in self.flags:
                try:
                    cb.stateChanged.disconnect(self.modsc)
                except:
                    pass
                cb.stateChanged.connect(self.modsc)

            try:
                self.ui.radioButton_startnormal.clicked.disconnect(self.modscr)
                self.ui.radioButton_startmnprn.clicked.disconnect(self.modscr)
                self.ui.radioButton_startfactory.clicked.disconnect(self.modscr)
            except:
                pass
            self.ui.radioButton_startnormal.clicked.connect(self.modscr)
            self.ui.radioButton_startmnprn.clicked.connect(self.modscr)
            self.ui.radioButton_startfactory.clicked.connect(self.modscr)
 

            self.ui.label.setText("Current settings:")
            sc_formatString =  f"{papa.nvrlist[0][1]:02X}"+f"{papa.nvrlist[1][1]:02X}"+f"{papa.nvrlist[2][1]:02X}"
            sc_mode         =  papa.nvrlist[3][1]
            sc_flags1       =  papa.nvrlist[4][1]
            #print(f"sc_formatString: {sc_formatString} sc_mode: {sc_mode} sc_flags1: {sc_flags1:08b}")
            self.ui.groupBox_2.setEnabled(True)
            if sc_mode == 1:
                self.ui.radioButton_startmnprn.setChecked(True)
            elif sc_mode == 2:
                self.ui.radioButton_startnormal.setChecked(True)
            else:
                self.ui.radioButton_startfactory.setChecked(True)
                self.ui.groupBox_2.setEnabled(False)
                
            for i in range(8):
                self.flags[i].setChecked(sc_flags1&(1<<i)!=0)
                
            if sc_formatString == "AA55C3":
                #format string for old versions < 2025-01-15
                msg = f"FRAM formatted correctly (before 2025-01-15)"
                print(msg)
                papa.write2Console(msg, insertMode=True)
            elif sc_formatString == "AA553C":
                #format string for old versions < 2025-01-15
                msg = f"FRAM formatted correctly"
                #print(msg)
                #papa.write2Console(msg, insertMode=True)
            else:
                #format string for old versions < 2025-01-15
                msg = f"Bad format string : {sc_formatString}"
                print(msg)
                papa.write2Console(msg, insertMode=True)
                self.ui.label.setText(msg)
                
    # def test(self):
    #     self.statusCmd.emit("zobi")

    def processOneThing(self):
        print("elapsed")
        
    def timeoutt(self):
        #print("Time out")
        dlg = QMessageBox(self.parent())
        dlg.setWindowTitle("Network")
        dlg.setText("Time out. Please, check your connection")
        dlg.setIcon(QMessageBox.Warning)
        button = dlg.exec()

        if button == QMessageBox.Ok:
            self.ui.label.setText("Can't find device")
        
    def fpipo(self):
        pass
        #self.statusCmd.emit(82, "done")
        
    def closeEvent(self, event):
        QtWidgets.QDialog.closeEvent(self, event)



######################################################
#
#
#
#
#        
#Mainclass
#
#
#
# ####################################################   
class MainForm(QtWidgets.QMainWindow):
    """
    This is the main window of the application
    Built by mygui.ui
    """
    fletcherSig   = pyqtSignal(int)
    resetAckSig   = pyqtSignal(int)
    resetButSig   = pyqtSignal(int)
    read128Sig    = pyqtSignal(str)
    frameCntSig   = pyqtSignal(str)
    
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        #print sys.getdefaultencoding()

        self.version   = VERSION
        self.date      = DATE
        self.game_type = "Recel"
        #self.game_type = "Gottlieb"

    

        self.ui = Ui_MainWindow()
        
        
        
        

        self.ui.setupUi(self)
        self.move(100,50)
        #self.setWindowTitle("WiFlip "+ self.game_type + " - V" + self.version + " (" +self.date +")")
        self.setWindowTitle("WiFlip "+ self.game_type)

        self.settings = QtCore.QSettings('AA55', 'wiflip')

        self.settings.setValue("MainWindow/default/geometry", 
                             self.saveGeometry())
        self.settings.setValue("MainWindow/default/windowState", 
                             self.saveState())        
        #self.ui.menuBar.setNativeMenuBar(False)
        #self.ui.menuBar.clear()
        
        # Then we look at our settings to see if there is a setting called geometry saved. Otherwise we default to an empty string
        geometry = self.settings.value('geometry', None)
        state    = self.settings.value('state', None)
        self.HOST     = self.settings.value('host', '192.168.1.26')
        self.PORT     = int(self.settings.value('port', '23'))
        self.face     = self.settings.value('face', 'fair_fight')
        self.fontsz   = self.settings.value('font-sz', '12')
        self.sound    = self.settings.value('sound', 'off')
        # Then we call a Qt built in function called restoreGeometry that will restore whatever values we give it.
        # In this case we give it the values from the settings file.
        if geometry is not None:
            self.restoreGeometry(geometry)
    
        if state is not None:
            self.restoreState(state)

        for act in  self.ui.menuFont_size.actions():                 
            if act.text() == self.fontsz:
                act.setChecked(True)
            else:
                act.setChecked(False)                 
        
        self.fontsz = int(self.fontsz)

        self.myhelp = None
        
        #frame counter is connected to frameCounter sig frameCntSig
        self.frameCnt = 0
        self.ui.rb_sysconf.setChecked(True)   
        self.frameCntSig.connect(self.frameCounter)
        self.read128Sig.connect(self.catch128SigMain)
             
        print("initial sound state", self.sound)
        if self.sound == "off":
            self.ui.actionSound.setChecked(False)
        else:
            self.ui.actionSound.setChecked(True)
        
        if self.game_type == "Recel":
            
            DP = 92
            BY = 69
            BX = 10

            self.setupmatchleds()
            
            self.actionGeneric(self.face)
            # if self.face == 'crazy_race':
            #     self.ui.label.setPixmap(QtGui.QPixmap(":/x/images/1x/crazy_race_480.png"))
            #     #self.ui.label.setStyleSheet("background-image: url(images/1x/crazy_race_480.png);")
            # else:
            #     self.ui.label.setPixmap(QtGui.QPixmap(":/x/images/1x/fair_fight_480.png"))
            #     #self.ui.label.setStyleSheet("background-image: url(images/1x/fair_fight_480.png);")
                
            self.ui.wplayer1.setGeometry(QtCore.QRect(200, 350, 220, 38))
            self.ui.wplayer2.setGeometry(QtCore.QRect(200, 350, 220, 38))
            self.ui.wplayer3.setGeometry(QtCore.QRect(200, 350, 220, 38))
            self.ui.wplayer4.setGeometry(QtCore.QRect(200, 350, 220, 38))
            
            self.ui.lcd1M_1.setGeometry(QtCore.QRect(200, 350, 32, 32))
            self.ui.lcd1M_2.setGeometry(QtCore.QRect(200, 350, 32, 32))
            self.ui.lcd1M_3.setGeometry(QtCore.QRect(200, 350, 32, 32))
            self.ui.lcd1M_4.setGeometry(QtCore.QRect(200, 350, 32, 32))
            
            
            self.ui.ballinplay.setGeometry(QtCore.QRect(200, 350, 272//6, 38))
            self.ui.credit.setGeometry(QtCore.QRect(200, 350, 272//6, 38))
            
            
            self.ui.lcd1M_1.move(QPoint(BX,BY))
            self.ui.wplayer1.move(QPoint(BX+32,BY))
            self.ui.lcd1M_2.move(QPoint(BX,BY+DP))
            self.ui.wplayer2.move(QPoint(BX+32,BY+DP))
            self.ui.lcd1M_3.move(QPoint(BX,BY+2*DP-4))
            self.ui.wplayer3.move(QPoint(BX+32,BY+2*DP-4))
            self.ui.lcd1M_4.move(QPoint(BX,BY+3*DP-7))
            self.ui.wplayer4.move(QPoint(BX+32,BY+3*DP-7))
            
            self.ui.ldsp_1_1.move(BX+32+220, BY-10)
            self.ui.ldsp_1_2.move(BX+32+220, BY+38-10)
            self.ui.ldsp_2_1.move(BX+32+220, BY+DP-10)
            self.ui.ldsp_2_2.move(BX+32+220, BY+DP+38-10)
            self.ui.ldsp_3_1.move(BX+32+220, BY+2*DP-4-10)
            self.ui.ldsp_3_2.move(BX+32+220, BY+2*DP-4+38-10)
            self.ui.ldsp_4_1.move(BX+32+220, BY+3*DP-7-10)
            self.ui.ldsp_4_2.move(BX+32+220, BY+3*DP-7+38-10)
            
            self.ui.credit.move(QPoint(50,15))
            self.ui.ballinplay.move(QPoint(64,405))  #ballinplay is actually freeplay here
            self.setupballinplay()
            for i in range(5):
                self.bip[i].setVisible (True)
                self.bipt[i].setVisible(True)
            self.bip[5].setVisible (False)
            self.bipt[5].setVisible(False)
            self.tiltIndicator.setVisible(True)
        
        elif self.game_type == "Gottlieb":   
            #self.ui.label.setStyleSheet("background-image: url(images/1x/pinballbell480.png);")
            self.ui.label.setPixmap(QtGui.QPixmap(":/x/images/1x/pinballbell480.png"))
            self.ui.lcd1M_1.hide()
            self.ui.lcd1M_2.hide()
            self.ui.lcd1M_3.hide()
            self.ui.lcd1M_4.hide()
            self.ui.ldsp_1_1.hide()
            self.ui.ldsp_1_2.hide()
            self.ui.ldsp_2_1.hide()
            self.ui.ldsp_2_2.hide()
            self.ui.ldsp_3_1.hide()
            self.ui.ldsp_3_2.hide()
            self.ui.ldsp_4_1.hide()
            self.ui.ldsp_4_2.hide()

        if self.game_type == "Gottlieb":
            self.swmRows, self.swmCols = (8, 5)
        else:
            self.swmRows, self.swmCols = (10, 4)

        self.Swtttext = [[None for x in range(self.swmCols)] for y in range(self.swmRows)]       
        self.sh_Swtttext = [[None for x in range(self.swmCols)] for y in range(self.swmRows)]       

        if self.game_type == "Recel":
            self.Swtttext[0][0] = "Ball Home"
            self.Swtttext[8][0] = "Fault"
            self.Swtttext[8][1] = "Coin 3"
            self.Swtttext[8][2] = "Coin 1"
            self.Swtttext[8][3] = "Coin 2"
            self.Swtttext[9][0] = "Tilt"
            self.Swtttext[9][1] = "Replays"
            self.Swtttext[9][2] = "Button 2"
            self.Swtttext[9][3] = "Button 1"
            
            self.setupgpios()
            self.setupb2s()

        self.setupleds()

        self.setupnvram()
            
        self.msg68 = ""
        self.msg83 = ""
        
        self.ui.label_RSSI.setVisible(True)
        self.ui.label_RSSI.setText("")
        self.ui.label_RSSI.setToolTip("-80 < RSSI< -40: good\n -40 < RSSI: Incredibly excellent\nBad otherwise")

        self.lastAstate = 0
        self.lastBstate = 0
        
        
        
        # Create the server, binding to localhost on port 9999
        # HOST, PORT = "192.168.1.26", 23
        # server = Server()
        # server.sessionOpened()
        # server.accept()
        #
        # #server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.bind((HOST, PORT))
        # self.write2Console("socket created \n")
        # self.write2Console(str((HOST, PORT)))
        #  # Receive data from the server and shut down
        # sock.listen()
        # conn, addr = sock.accept()
        # with conn:
        #     self.write2Console(f"Connected by {addr}")
        #     while True:
        #         data = conn.recv(1024)
        #         if not data:
        #             break
        #         conn.sendall(data)            
        #         self.write2Console(str(data))
        # print ("server started")
        # # Activate the server; this will keep running until you
        # # interrupt the program with Ctrl-C
        # server.serve_forever()     
        #
        # # server = Server()
        # # server.StartServer()
        #
        # # self.tcp = Messenger()
        # # self.tcp.slotSendMessage()
        
        self.ui.actionAbout_wiflip.triggered.connect(self.launchAbout)
        self.ui.actionHelp.triggered.connect(self.launchHelp)
        self.ui.actionSettings.triggered.connect(self.launchSettings)
        self.ui.actionReprog.triggered.connect(self.launchReprog)
        self.ui.actionGame_settings.triggered.connect(self.launchGameSet)
        self.ui.actionWifi_config.triggered.connect(self.launchWifiC)
        self.ui.actionSupervision.triggered.connect(self.launchSuperV)

        self.ui.actionSound.toggled.connect(self.toggleSound)


        self.ui.menuFont_size.triggered.connect(self.changefontpt)


        self.ui.pushButton.clicked.connect(self.connect)
        self.ui.lineEdit.setText(self.HOST)
        self.ui.lineEdit_2.setText(str(self.PORT))

        #self.jingle = os.path.join(CURRENT_DIR, "alarm1-b238.wav")

        self.jingle = ":/sound/alarm1-b238.wav"
        self.myDisconnectSound = QSound(self.jingle)
        #QSound.play(self.jingle)
        self.setsound()
        #trace button
        self.ui.pushButton_3.clicked.connect(self.send_trace)
        self.ui.pushButton_6.clicked.connect(self.send_gptrace)
        #dump button
        self.ui.pushButton_2.clicked.connect(self.send_dump)
        #game prom dump button
        # self.ui.pushButton_7.clicked.connect(self.send_dump_game_prom)
        # self.ui.pushButton_8.clicked.connect(self.send_dump_A1762_prom)
        self.ui.pushButton_9.clicked.connect(self.resetthepin_with_ack)
        
        self.ui.pushButton_7.clicked.connect(self.resetthepin)
        # self.ui.pushButton_8.clicked.connect(self.send_dump_A1762_prom)
        # self.ui.pushButton_8.setDisabled(True)
        self.ui.pushButton_7.setText("Reset Pinball w/o ack")
        self.ui.pushButton_7.setToolTip("Reset w/o ack is for early versions of devices, where ack was not yet implemented")

        self.ui.pushButton_8.clicked.connect(self.reqswVers)
        self.ui.pushButton_8.setText("Get Device SW UUID")
        
        #The hard way
        self.pushButton_10 = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents_3)
        self.pushButton_10.setObjectName("pushButton_10")
        self.ui.gridLayout_4.addWidget(self.pushButton_10, 6, 1, 1, 1)
        self.pushButton_10.setText("Dip switches status")
        self.pushButton_10.clicked.connect(self.reqdips)
         
        #nvrdump button
        self.ui.pushButton_R_dump.clicked.connect(self.send_nvrdump)

        #gpdump button
        self.ui.pushButton_4.clicked.connect(self.send_gpdump)
 
        #dpdump button
        self.ui.pushButton_5.clicked.connect(self.send_dpdump)
        
        #IOL control
        self.ui.iolButton.clicked.connect(self.send_iol)
        
        #Selection of hm6508 mode
        self.ui.pushButton_iram.clicked.connect(self.send_hmintern)
        self.ui.pushButton_hram.clicked.connect(self.send_hmreal)
        
        
        #nvrams read/write
        self.ui.pb_rmem.clicked.connect(self.send_reqrread)
        self.ui.pb_flash.clicked.connect(self.send_reqflash)
        self.ui.pb_write_byte.clicked.connect(self.send_reqwrbyte)
        self.ui.pb_wmem.clicked.connect(self.send_reqwriteall)
        self.ui.pb_reset.clicked.connect(self.resetthepin)

        #supervisor
        self.ui.superButton.clicked.connect(self.superReq)
        self.ui.sendButton.clicked.connect(self.superCmd)
        self.mycmds = {"Display A":0x5A, "Display B":0x5B, 
                       "B2":0x20,        "B3-AB":0x30, 
                       "B3-CD":0x31,     "B3-EF":0x32}
        self.ui.comboCmd1.addItems(self.mycmds.keys())
        
        #improve look of buttons
        self.ui.pb_rmem.setStyleSheet(
            '''
QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 rgb( 25, 25, 112), stop: 0.4 rgb( 102, 102, 182),
                                            stop: 0.5 rgb( 75, 75, 162), stop: 1.0 rgb( 25, 25, 112));
    color: Ivory;
    border-style: outset;
    border-width: 1px;
    border-radius: 10px;
    border-color: beige;
    min-width: 10em;
    min-height: 10px;
    padding: 6px;
}
QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 Navy, stop: 0.1 Blue,
                                            stop: 0.3 RoyalBlue, stop: 1.0 MidnightBlue);
    border-style: inset;
    
}            

QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 rgb( 50, 50, 224), stop: 0.4 rgb( 200, 200, 240),
                                            stop: 0.5 rgb( 150, 150, 255), stop: 1.0 rgb( 50, 50, 224));
    border-style: inset;
    
}            
    '''       
            )

        self.ui.pb_flash.setStyleSheet(
            '''
QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 rgb(199, 21, 133), stop: 0.4 rgb( 251, 102, 200),
                                            stop: 0.5 rgb( 240, 75, 162), stop: 1.0 rgb(199, 21, 133));
    color: Ivory;
    border-style: outset;
    border-width: 1px;
    border-radius: 10px;
    border-color: beige;
    min-width: 10em;
    min-height: 10px;
    padding: 6px;
}
QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 rgb(100, 5, 88), stop: 0.4 rgb( 131, 40, 90),
                                            stop: 0.5 rgb( 240, 75, 162), stop: 1.0 rgb(90, 0, 80));
    border-style: inset;

}            

QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 rgb(255, 42, 200), stop: 0.4 rgb( 255, 152, 225),
                                            stop: 0.5 rgb( 255, 180, 254), stop: 1.0 rgb(255, 42, 200));
    border-style: inset;

}            
    '''       
            )
        self.ui.pb_reset.setStyleSheet(
            '''
QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 rgb(220, 21, 40), stop: 0.4 rgb( 255, 30, 50),
                                            stop: 0.5 rgb( 240, 35, 50), stop: 1.0 rgb(220, 20, 40));
    color: Ivory;
    border-style: outset;
    border-width: 1px;
    border-radius: 10px;
    border-color: beige;
    min-width: 10em;
    min-height: 10px;
    padding: 6px;
}
QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 rgb(160, 2, 10), stop: 0.4 rgb( 200, 30, 90),
                                            stop: 0.5 rgb( 180, 25, 60), stop: 1.0 rgb(160, 2, 10));
    border-style: inset;

}            

QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 rgb(255, 60, 60), stop: 0.4 rgb( 250, 50, 50),
                                            stop: 0.5 rgb( 240, 40, 40), stop: 1.0 rgb(255, 60, 60));
    border-style: inset;

}            
    '''       
            )
        
        self.ui.pb_wmem.setStyleSheet(
            '''
QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 rgb(200, 130, 32), stop: 0.4 rgb(225, 165, 80),
                                            stop: 0.5 rgb(215, 145, 60), stop: 1.0 rgb(200, 130, 32));
    color: Ivory;
    border-style: outset;
    border-width: 1px;
    border-radius: 10px;
    border-color: beige;
    min-width: 10em;
    min-height: 10px;
    padding: 6px;
}
QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 rgb(170, 100, 2), stop: 0.4 rgb(200, 135, 50),
                                            stop: 0.5 rgb(195, 125, 40), stop: 1.0 rgb(170, 100, 2));
    border-style: inset;

}            

QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 rgb(230, 160, 62), stop: 0.4 rgb(250, 200, 110),
                                            stop: 0.5 rgb(245, 180, 88), stop: 1.0 rgb(230, 160, 62));
    border-style: inset;

}            
    '''       
            )
        self.ui.pb_write_byte.setStyleSheet(self.ui.pb_wmem.styleSheet())
        
        #switch simu
        self.ui.pushButton_sw.clicked.connect(self.send_reqswclose)
        

        # font = QtGui.QFont()
        # font.setPointSize(5)
        # #font.setBold(True)
        # #font.setWeight(75)
        # self.ui.pushButton.setFont(font)
        font = QtGui.QFont("courier new")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.ui.label_inp.setFont(font)
        self.ui.label_out.setFont(font)
        self.linenb = 0


        uilabels = [
            self.ui.label_D0_F, self.ui.label_D0_E, self.ui.label_D0_D, self.ui.label_D0_C,
            self.ui.label_D0_B, self.ui.label_D0_A, self.ui.label_D0_9, self.ui.label_D0_8,
            self.ui.label_D0_7, self.ui.label_D0_6, self.ui.label_D0_5, self.ui.label_D0_4,
            self.ui.label_D0_3, self.ui.label_D0_2, self.ui.label_D0_1, self.ui.label_D0_0
                    ]
        self.last_uilabels = ["00"]*16
        self.vientdecliquer = 0

        #Reset the window settings on this event
        # QtCore.QObject.connect(self.ui.actionClear_all, 
        #                        QtCore.SIGNAL("triggered()"), 
        #                        self.clearSettin)
        
        self.ui.actionClear_all_2.triggered.connect(self.clearSettin)
        self.ui.actionRearm_warning_messages.triggered.connect(self.clearWarnMsg)
        
        #generic facelift menu generator
        self.actionGame = dict()
        for game, gdata in RscPin.Models.items():
            try:
                gfile = gdata['Backglass']
                #print(game, gfile)
                self.actionGame[game] = QtWidgets.QAction(game)
                self.actionGame[game].setObjectName("qaction"+game)
                self.ui.menuRecel_2.addAction(self.actionGame[game])
                self.actionGame[game].triggered.connect(partial(self.actionGeneric, game))
                #print(game, gfile, actionGame[game])
                
            except:
                #print("Gros pb")
                pass
        
            #self.actionGame = QtWidgets.QAction()
        # self.ui.actionFair_Fight.triggered.connect(self.actionFair_Fight)
        # self.ui.actionCrazy_Race.triggered.connect(self.actionCrazy_Race)

        self.ui.actionSave_nvram.triggered.connect(self.actionSaveNvr)
        self.ui.actionLoad_nvr.triggered.connect(self.actionLoadNvr)

        #calque combo
        #print(RscPin.Models.keys())
        #self.ui.comboBox.addItems(['Crazy Race', 'Fair Fight'])
        self.ui.comboBox.addItems(list(RscPin.Models.keys()))

        # Connect signals to the methods.
        #self.ui.comboBox.activated.connect(self.activated)
        self.ui.comboBox.currentTextChanged.connect(self.text_changed)
        #self.ui.comboBox.currentIndexChanged.connect(self.index_changed)
        calqueStr = self.settings.value('calqueStr', 'Fair Fight')
        self.text_changed(calqueStr)
        self.ui.comboBox.setCurrentText(calqueStr)
        if self.game_type == "Recel":
            #dock des config switches de gottlieb
            #self.ui.dockWidget_5.setFloating(True)
            self.ui.dockWidget_5.setVisible(False)

        #self.ui.dockWidget_4.hide()
        self.ui.dockWidget_5.setEnabled(False)
        self.ui.dockWidget_6.hide()

        
 
        
        
    def text_changed(self, s):
        #print("change calque settings for:", s)
        self.settings.setValue('calqueStr', s)

        
        #self.Swtttext = [[None for x in range(self.swmCols)] for y in range(self.swmRows)]       
        self.sh_Swtttext = [[None for x in range(self.swmCols)] for y in range(self.swmRows)]       

        self.Swtttext    = RscPin.Models[s]["Switches"]
        self.sh_Swtttext = RscPin.Models[s]["Switches short"]


        for i in range(self.swmRows):
            for j in range(self.swmCols): 
                self.led[i][j].setToolTip(self.Swtttext[i][j])
                self.ledlabel[i][j].setText(self.sh_Swtttext[i][j])
                self.ledlabel[i][j].setToolTip(self.Swtttext[i][j])
       
    def reqdips(self):
        print("message request is", b'YDXXX')
        try:
            self.thread.sock.send(b'YDXXX')
        except:
            pass

    def reqswVers(self):
        print("message request is", b'YDDXX')
        try:
            self.thread.sock.send(b'YDDXX')
        except:
            pass

    def superReq(self):
        print("message request is", b'YCXQ0')
        try:
            self.thread.sock.send(b'YCXQ0')
        except:
            pass

        
    def resetthepin_with_ack(self):
        print("message request is", b'YCXQZ')
        try:
            self.thread.sock.send(b'YCXQZ')
        except:
            pass
        
        self.frameCnt = 0
        self.frameCntSig.connect(self.frameCounter)
        
    def resetthepin(self):
        print("message request is", b'YBXQZ')
        try:
            self.thread.sock.send(b'YBXQZ')
        except:
            pass
        
        self.frameCnt = 0
        self.frameCntSig.connect(self.frameCounter)
        

    def toggleSound(self):
        #print("toggle sound", self.ui.actionSound.isChecked(), self.ui.actionSound.isCheckable())
        if self.sound == "on":
            self.sound = "off"
            #self.ui.actionSound.setChecked(False)
        else:
            #self.ui.actionSound.setChecked(True)
            self.sound = "on"
            

    def changefontpt(self, action):

        
        sz = int(action.text())     

        for act in  self.ui.menuFont_size.actions():                 
            if act.text() == action.text():
                act.setChecked(True)
            else:
                act.setChecked(False)                 
        myfont   =  QtGui.QFont("Courier New", sz)
        
        self.settings.setValue('font-sz', str(sz))
        self.fontsz = sz
        
        fm = QFontMetrics(myfont)
        w = fm.boundingRect("0B0000").width()
        h = fm.boundingRect("0B0000").height()
    
        for i in range(16):
            for j in range(16):
                self.nibbleField[i][j].setFixedWidth(w+10)
                self.nibbleField[i][j].setFixedHeight(h+10)
                self.nibbleField[i][j].setFont(myfont)
            
            
    def actionSaveNvr(self):
        nvrfileStr = self.settings.value('nvrfileStr', None)
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                            "Save nvr data",
                                                            nvrfileStr,
                                                            "Nvr data (*.nvr)")
        

        if filename:
            self.settings.setValue("nvrfileStr", filename)
            #print (filename)
            #print(self.nvrlist)
            with open(filename, "w") as f:
                # write contents      
                for i in range(128):
                    val = self.nvrlist[i][1]
                    f.write(f"0X{i:02X}:0X{val:02X}"+os.linesep)      

                

    def actionLoadNvr(self):
        nvrfileStr = self.settings.value('nvrfileStr', None)
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load File",
                                       nvrfileStr,
                                       "NVR data file (*.nvr)")

        if filename:
            with open(filename, "r") as f:
                # read contents      
                lines = f.read().splitlines() 
                #print("lines", lines)
                for ln in lines:
                    mycod = ln.split(":")
                    if len(mycod) == 2:
                        #print(mycod)
                        try:
                            addr = int(mycod[0], 0)
                            byte = int(mycod[1], 0)
                        except:
                            addr = byte = -1
                        #print(addr, byte)
                        if addr >= 0 and addr <= 127 and byte >= 0 and byte <= 255:
                            lb = byte&0xF
                            hb = (byte&0xF0)>>4
                            r  = (addr//8)
                            l  = (addr%8)
                            #print(addr, r, l)
                            self.nvrlist[addr] = ( -1, byte)
                            self.nibbleField[r][2*l].setText(f"{lb:1X}")
                            self.nibbleField[r][2*l+1].setText(f"{hb:1X}")
                            #self.nibbleField[r][2*l].setStyleSheet("background:rgb(120, 120, 120);color:rgb(255, 255, 255);")
                            #self.nibbleField[r][2*l+1].setStyleSheet("background:rgb(120, 120, 120);color:rgb(255, 255, 255);")
                            self.nibbleField[r][2*l].setStyleSheet("background:purple;color:rgb(255, 255, 255);")
                            self.nibbleField[r][2*l+1].setStyleSheet("background:purple;color:rgb(255, 255, 255);")
                #print(self.nvrlist)      

    def frameCounter(self, typ):
        if typ == "A":
            self.frameCnt += 1
        
        #print("frame A cnt", self.frameCnt)
        
        if self.frameCnt == 10:
            self.frameCntSig.disconnect()
            self.send_reqrread()
        
        
    def setsound(self):  
        format = QAudioFormat()
        format.setChannelCount(1)
        format.setSampleRate(44100)
        format.setSampleSize(16)
        format.setCodec("audio/pcm")
        format.setByteOrder(QAudioFormat.LittleEndian)
        format.setSampleType(QAudioFormat.SignedInt)

        info = QAudioDeviceInfo();
        device = info.defaultOutputDevice()
        # print(device.supportedChannelCounts())
        # print(device.supportedCodecs())
        # print(device.supportedSampleRates())
        if not device.isFormatSupported(format):
            print("format audio not supported")
            # self.sound = "off"
            # self.settings.setValue('sound', self.sound)
            format = device.nearestFormat(format)
            print("format changed")
            print("channels", format.channelCount())
            print("rate", format.sampleRate())
            print("size", format.sampleSize())

        self.output = QAudioOutput(device, format, self)

        self.frequency = 440
        self.volume = 32767
        self.sbuffer = QBuffer()
        self.sdata10    = QByteArray()
        self.sdata100   = QByteArray()
        self.sdata1K    = QByteArray()
        self.sdata10K   = QByteArray()
        self.sdata100K  = QByteArray()

        #self.sdata10.clear()
        self.frequency = 440*16
        for i in range(22050//2):
            t = i / 22050.0
            value = int(self.volume * math.sin(2 * math.pi * self.frequency * t))
            self.sdata10.append(struct.pack("<h", value))
        self.frequency = 440*8
        for i in range(22050//2):
            t = i / 22050.0
            value = int(self.volume * math.sin(2 * math.pi * self.frequency * t))
            self.sdata100.append(struct.pack("<h", value))
        self.frequency = 440*4
        for i in range(22050//2):
            t = i / 22050.0
            value = int(self.volume * math.sin(2 * math.pi * self.frequency * t))
            self.sdata1K.append(struct.pack("<h", value))
        self.frequency = 440*2
        for i in range(22050//2):
            t = i / 22050.0
            value = int(self.volume * math.sin(2 * math.pi * self.frequency * t))
            self.sdata10K.append(struct.pack("<h", value))
        self.frequency = 440*1
        for i in range(22050//2):
            t = i / 22050.0
            value = int(self.volume * math.sin(2 * math.pi * self.frequency * t))
            self.sdata100K.append(struct.pack("<h", value))
        

        self.play(self.sdata10+self.sdata100+self.sdata1K+self.sdata10K+self.sdata100K)
        # while self.output.state() == QAudio.ActiveState:
        #     pass
        #self.output.stop()


    def play(self, data):
        #print("play")
        if self.sound == "off":
            return 
        if self.output.state() == QAudio.ActiveState:
            self.output.stop()
        
        if self.sbuffer.isOpen():
            self.sbuffer.close()
        
        #if self.output.error() == QAudio.UnderrunError:
        if self.output.error() != QAudio.NoError:
            print("reset audio channel", self.output.error())
            if self.output.error() == QAudio.UnderrunError:
                print("underrun error")
            self.output.reset()

        self.sbuffer.setData(data)
        self.sbuffer.open(QIODevice.ReadOnly)
        self.sbuffer.seek(0)

        self.output.start(self.sbuffer)
             
    def launchAbout(self):
        """
        Starts the about dialog box
        """
        myabout=MyAbout(self)
        myabout.show()

    def launchHelp(self):
        """
        Starts the help dialog box
        """
        if self.myhelp == None:
            self.myhelp=MyHelp(self)
            self.myhelp.show()
        else:
            self.myhelp.activateWindow()
            #je ne sais pas comment revenir au premier plan
            
    def launchGameSet(self):
        """
        Starts the game settings dialog box
        """
        #V1.2.20 added param 'self' in next command, to avoid window to disappear
        #self.options = options.MyOptions(self)
        self.options = MyOptions(self)
        self.options.config(self.settings)
        self.options.exec_()
        
        # self.mygameset=MyGameSet(self)
        # self.mygameset.exec()
                  
    def launchReprog(self):
        """
        Starts the reprog dialog box
        """
        self.myreprog=MyReprog(self)
        self.myreprog.exec()
                  
    def launchSettings(self):
        """
        Starts the about dialog box
        """
        self.mysettings=MySettings(self)
        #self.mysettings.show()
        self.mysettings.exec()

    def launchWifiC(self):
        """
        Starts the wifi config dialog box
        """
        self.mywificnf=MyWIFICnf(self)
        #self.mysettings.show()
        self.mywificnf.exec()

    def launchSuperV(self):
        """
        Starts the supervisor dialog box
        """
        self.mysuperv=MySuperv(self)
        #self.mysettings.show()
        self.mysuperv.exec()

    def actionGeneric(self, gamename):   
        self.face = gamename
        try:
            fgame =  ":/x/images/1x/"+RscPin.Models[gamename]['Backglass']
        except:
            fgame = ":/x/images/1x/fair_fight_480.png"
        # print("action generic", self.face, fgame)
        # try:
        #     print("action generic2", RscPin.Models[gamename]['Backglass'])  
        # except:
        #     print("game", gamename, "not registered in RscPin")
            
        self.ui.label.setPixmap(QtGui.QPixmap(fgame))
                    
    def actionFair_Fight(self):
        #self.ui.label.setStyleSheet("background-image: url(images/1x/fair_fight_480.png);")
        self.ui.label.setPixmap(QtGui.QPixmap(":/x/images/1x/fair_fight_480.png"))
        self.face = 'fair_fight'
    def actionCrazy_Race(self):
        #self.ui.label.setStyleSheet("background-image: url(images/1x/crazy_race_480.png);")
        self.ui.label.setPixmap(QtGui.QPixmap(":/x/images/1x/crazy_race_480.png"))
        self.face = 'crazy_race'


        
    def clearWarnMsg(self):
        """
        Called by a menu item of the menu bar
        Used to reset the checkboxes of certain warning messages
        """
        #print("clearWarnMsg")
        reply = QMessageBox.question(self, 
                                           'Please confirm',
                                           "You are about to rearm certain warning alert boxes. Are you sure ?", 
                                           QMessageBox.Yes | 
                                           QMessageBox.No, 
                                           QMessageBox.No)
        if reply == QMessageBox.Yes:
            #it is "True", not True, because on PC, qsettings returns strings in general (not always, though...)
            self.settings.setValue('superWarningTick', "True")                        
            self.settings.sync()
            
        
    def clearSettin(self):
        """
        Called by a menu item of the menu bar
        Used to reset windowing to factory default
        """
        #print("clearsettings")
        reply = QMessageBox.question(self, 
                                           'Please confirm',
                                           "You are about to clear your window layout. Are you sure ?", 
                                           QMessageBox.Yes | 
                                           QMessageBox.No, 
                                           QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.restoreGeometry(self.settings.value("MainWindow/default/geometry"))
            self.restoreState(self.settings.value("MainWindow/default/windowState"))
            self.settings.setValue("geometry", self.saveGeometry())
            self.settings.setValue("state", self.saveState())
            self.settings.sync()
            
            #pas beau mais j'arrive pas à me debarrasser de ce dock autrement
            if self.game_type == "Recel":
                #dock des config switches de gottlieb
                #self.ui.dockWidget_5.setFloating(True)
                self.ui.dockWidget_5.setVisible(False)

            #Provisory we don't want that to be displayed but we don't want to lose it either...
            self.ui.dockWidget_4.setVisible(False)
            self.ui.dockWidget_6.setVisible(False)
        

        

    def send_reqswclose(self):
        '''
        Simulate a switch close 
        '''
        try:
            strb = int(self.ui.lineEdit_swstrb.text(), 0)
        except:
            strb = 0
        strb = strb.to_bytes(1, byteorder='big')
        try:
            ret = int(self.ui.lineEdit_swret.text(), 0)
        except:
            ret = 0
        ret = ret.to_bytes(1, byteorder='big')
     
        print("message request is", b'YS'+strb+ret+ret)
        try:
            self.thread.sock.send(b'YS'+strb+ret+ret)
        except:
            pass
    
          
    def send_trace(self): 
        try:
            self.thread.sock.send(b' t')
        except:
            pass
        
    def send_dump(self): 
        self.linenb = 0
        try:
            self.thread.sock.send(b' d')
        except:
            pass

    def send_dump_game_prom(self):
        self.linenb = 0
        memtyp = 4
        print("message request is", b'YR'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            self.thread.sock.send(b'YR'+memtyp.to_bytes(1, byteorder='big')+b'XX')
        except:
            pass

        
    def send_dump_A1762_prom(self):
        self.linenb = 0
        memtyp = 5
        print("message request is", b'YR'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            self.thread.sock.send(b'YR'+memtyp.to_bytes(1, byteorder='big')+b'XX')
        except:
            pass

        
    def send_gptrace(self): 
        try:
            self.thread.sock.send(b' U')
        except:
            pass
        
        
    def send_nvrdump(self): 
        self.linenb = 0
        #print("send command R")
        try:
            self.thread.sock.send(b' R')
        except:
            pass
        
    def send_gpdump(self): 
        self.linenb = 0
        try:
            self.thread.sock.send(b' G')
        except:
            pass
        
    def send_dpdump(self): 
        self.linenb = 0
        try:
            self.thread.sock.send(b' C')
        except:
            pass
        
    def send_hmreal(self): 
        self.linenb = 0
        try:
            self.thread.sock.send(b' h')
        except:
            pass
        
    def send_hmintern(self): 
        self.linenb = 0
        try:
            self.thread.sock.send(b' i')
        except:
            pass
 
    def send_reqwriteall(self): 
        self.linenb = 0
        if   self.ui.rb_sysconf.isChecked():
            memtyp = 0
        elif self.ui.rb_mnprn.isChecked():
            memtyp = 2
        elif self.ui.rb_nvram.isChecked():
            memtyp = 1
        else:
            memtyp = 3
        print("global write to nvram", memtyp)

        for addr in range(128):
            init_byte = self.nvrlist[addr][0]
            byte      = self.nvrlist[addr][1]
            
            if byte != init_byte:
                #print("want to write", byte, "at address", addr)
                baddr = addr.to_bytes(1, byteorder='big')
                bbyt = byte.to_bytes(1, byteorder='big')

                print("message request is", b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)

                try:
                    self.thread.sock.send(b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
                except:
                    pass


    def superCmd(self):
        
        try:
            c1byte = self.mycmds[self.ui.comboCmd1.currentText()]
            #c1byte = int(self.ui.lineEdit_c1.text(), 0)&0xFF
        except:
            c1byte = 0
        try:
            c2byte = int(self.ui.lineEdit_c2.text(), 0)&0xFF
        except:
            c2byte = 0
        try:
            c3byte = int(self.ui.lineEdit_c3.text(), 0)&0xFF
        except:
            c3byte = 0
        
        c1byte = c1byte.to_bytes(1, byteorder='big')   
        c2byte = c2byte.to_bytes(1, byteorder='big')   
        c3byte = c3byte.to_bytes(1, byteorder='big')   
        print("message request is", b'YQ'+c1byte+c2byte+c3byte)

        try:
            self.thread.sock.send(b'YQ'+c1byte+c2byte+c3byte)
        except:
            pass
        

                        
    def send_reqwrbyte(self):
        self.linenb = 0
        if   self.ui.rb_sysconf.isChecked():
            memtyp = 0
        elif self.ui.rb_mnprn.isChecked():
            memtyp = 2
        elif self.ui.rb_nvram.isChecked():
            memtyp = 1
        else:
            memtyp = 3
        
        try:
            addr = int(self.ui.lineEdit_addr.text(), 0)&0x7F
        except:
            addr = 0
        addr = addr.to_bytes(1, byteorder='big')
            
        try:
            mybyte = int(self.ui.lineEdit_byte.text(), 0)&0xFF
        except:
            mybyte = 0
        mybyte = mybyte.to_bytes(1, byteorder='big')
            
        print("message request is", b'YW'+memtyp.to_bytes(1, byteorder='big')+addr+mybyte)

        try:
            self.thread.sock.send(b'YW'+memtyp.to_bytes(1, byteorder='big')+addr+mybyte)
        except:
            pass
        
    def send_reqflash(self):
        self.linenb = 0
        if   self.ui.rb_sysconf.isChecked():
            memtyp = 0
        elif self.ui.rb_mnprn.isChecked():
            memtyp = 2
        elif self.ui.rb_nvram.isChecked():
            memtyp = 1
        else:
            memtyp = 3
            
        print("message request is", b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            self.thread.sock.send(b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')
        except:
            pass
        time.sleep(0.2) #to let time for the previous command to execute
                
    def send_reqrread(self):    
        self.linenb = 0
        if   self.ui.rb_sysconf.isChecked():
            memtyp = 0
        elif self.ui.rb_mnprn.isChecked():
            memtyp = 2
        elif self.ui.rb_nvram.isChecked():
            memtyp = 1
        else:
            memtyp = 3
            
        print("message request is", b'YR'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            self.thread.sock.send(b'YR'+memtyp.to_bytes(1, byteorder='big')+b'XX')
        except:
            pass
            
    def send_iol(self): 
        try:
            cmd = self.ui.lineEdit_Cmd.text()
            cmd = int(cmd, 16)+0x90
        except:
            cmd = 0
        try:
            acc = self.ui.lineEdit_Acc.text()
            acc = int(acc, 16)+0xA0
        except:
            acc = 0
        startcode = 0xB0
        mybytes = bytearray()
        #mybytes.append(startcode)
        mybytes.append(cmd)
        mybytes.append(acc)
        mybytes.append(startcode)
        
        
        try:
            self.thread.sock.send(mybytes)
        except:
            print("error not sending anything")
            pass
        
        self.vientdecliquer = 1
        print("sent:", mybytes)
        
        # mybytes = bytearray([
        #                         0xB0,0x08,0x0, 
        #                      ])   
        # #                     #     0x09,0x0,0xB0, 0x0A,0x0,0xB0, 0x0B,0x0,0xB0,
        # #                     #     0x0C,0x0,0xB0, 0x0D,0x0,0xB0, 0x0E,0x0,0xB0, 0x0F,0x0,0xB0,
        # #                     #     0xB1
        # #                     # ])
        #
        # sleep(1.1)
        # try:
        #     self.thread.sock.send(mybytes)
        # except:
        #     print("error2 not sending anything")
        #     pass
        #
        # print("sent:", mybytes)
        # mybytes = bytearray([
        #                         0xB0,0x09,0x0, 
        #                      ])   
        # #                     #     0x09,0x0,0xB0, 0x0A,0x0,0xB0, 0x0B,0x0,0xB0,
        # #                     #     0x0C,0x0,0xB0, 0x0D,0x0,0xB0, 0x0E,0x0,0xB0, 0x0F,0x0,0xB0,
        # #                     #     0xB1
        # #                     # ])
        #
        # sleep(1.1)
        # try:
        #     self.thread.sock.send(mybytes)
        # except:
        #     print("error2 not sending anything")
        #     pass
        #
        # print("sent:", mybytes)
        #
        #

    def disconnect(self):
        #print("disconnect")
        self.ui.label_12.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
        #self.ui.pushButton.clicked.connect(self.connect)
        self.ui.pushButton.clicked.disconnect(self.disconnect)
        self.ui.pushButton.setText("connect")
        # try:
        #     self.thread.sock.close()
        # except:
        #     pass
        try: # conn. thread
            #self.thread.sock.close()
            #self.thread.sock.shutdown(socket.SHUT_RDWR)
            #self.thread.terminate()
            #print("Request thread interruption")
            self.thread.requestInterruption()
            self.thread.wait()
            #print("Thread is DONE", self.thread)
        except Exception as e:
            print(f"Disconnect exception {e}")
        
    def connect(self):
        #print("connect")
        self.ui.pushButton.clicked.connect(self.disconnect)
        self.ui.pushButton.clicked.disconnect(self.connect)
        self.ui.pushButton.setText("disconnect")
        self.frameCnt = 0
        
        if  True:
            #self.thread = Worker(HOST=self.HOST, PORT=self.PORT)
            self.thread = Worker(HOST=self.ui.lineEdit.text(), 
                                 PORT=self.ui.lineEdit_2.text())

            self.thread.finished.connect(self.pipo)
            self.thread.output.connect(self.cmdMng)
            self.thread.connled.connect(self.connled)
            self.thread.commErr.connect(self.commError)
            self.thread.workerErr.connect(self.work_error_received)
            self.thread.start()
            #print("creation of Thread", self.thread)

    def work_error_received(self, str):
        self.thread.commErr.disconnect(self.commError)
        self.thread.workerErr.disconnect(self.work_error_received)
        dlg = QMessageBox(self.parent())
        dlg.setWindowTitle("Connection error")
        if str.startswith("Connection aborted"):
            dlg.setText(str)
            dlg.setIcon(QMessageBox.Information)
        else:
            dlg.setText(str+"\n"+ "Please, check your connection parameters, restart the device and try again.")
            dlg.setIcon(QMessageBox.Critical)
        dlg.addButton(QPushButton("Dismiss"), QMessageBox.NoRole)
        button = dlg.exec()
        #exit(0)
        self.connled("closing")

    def commError(self, msgStr):
        self.write2Console(f"{msgStr}\r\n", insertMode=True)
        # if msgStr == f"connection lost. Broken pipe. Retry...":
        #     self.thread.commErr.disconnect(self.commError)
        #     self.thread.workerErr.disconnect(self.work_error_received)
        #     self.connect()

    def connled(self, state):
        if state == "green":
            self.ui.label_12.setPixmap(QtGui.QPixmap(":/x/ledgreen"))
            #QSound.stop()
            try:
                self.myDisconnectSound.stop()
            except: pass

        elif state == "grey":
            try:
                self.ui.pushButton.clicked.connect(self.connect)
                self.ui.pushButton.clicked.disconnect(self.disconnect)
            except:
                pass
            self.myDisconnectSound.play()
            #QSound.stop(self.mysound)
            
            self.ui.pushButton.setText("connect")
            self.ui.label_12.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
        elif state == "closing":
            try:
                self.ui.pushButton.clicked.connect(self.connect)
                self.ui.pushButton.clicked.disconnect(self.disconnect)
            except:
                pass
            #self.myDisconnectSound.play()
            #QSound.stop(self.mysound)
            
            self.ui.pushButton.setText("connect")
            self.ui.label_12.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
        elif state == "yellow":
            self.ui.label_12.setPixmap(QtGui.QPixmap(":/x/ledyellow"))
            try:
                self.myDisconnectSound.stop()
            except: pass

    #convenient routine to allow the outside for writing to the script edit text window
    def write2ScriptEdit(self, msg, insertMode=True):
        if insertMode:
            self.ui.plainTextEdit.insertPlainText(msg)
        else:
            self.ui.plainTextEdit.clear()
            self.ui.plainTextEdit.appendPlainText(msg)

    #convenient routine to allow the outside for writing to the script edit text window
    def write2Console(self, msg, insertMode=True):
        if insertMode:
            self.ui.consoleEdit.insertPlainText(msg)
        else:
            self.ui.consoleEdit.clear()
            self.ui.consoleEdit.appendPlainText(msg)
            
        #test
        #self.ui.consoleEdit.setFocus()
        self.ui.consoleEdit.centerOnScroll()
        self.ui.consoleEdit.centerCursor()
        
    def giveFocus2Edit(self):
        self.ui.plainTextEdit.setFocus()
        self.ui.plainTextEdit.centerOnScroll()
        self.ui.plainTextEdit.centerCursor()
           
    def pipo(self):
        print("close conn. thread")
        self.thread.quit()
    
    def pipo2(self):
        print("pipoptage2")

    def cmdMng(self, data, typ):
        #print("received", data, typ, type(typ))
        if typ == 0:
            print("typ=0", str(data))
        elif typ == 84:   #T
            # 8b ROM data
            #12b ROM addr
            # 1b reset state
            # 1b read/write state
            # 1b w_io state
            # 1b bagotting checker
            #print("recu", data[0], data[1], data[2])
            #print("typ=54", str(data))
            self.linenb      += 1
            ramdata      = data[0]
            romdata      = data[1]
            romaddr      = data[2]+(data[3]&0x0F)*0x100
            bagotti  = 1 if data[3]&0x80 else 0
            wiostate = 1 if data[3]&0x40 else 0
            rwstate  = 1 if data[3]&0x20 else 0
            rststate = 1 if data[3]&0x10 else 0
            ramaddr      = data[4]+256*bagotti
            #print(f"{romaddr:03X}\t{romdata:02X} rst={rststate} rw={rwstate} wio={wiostate} bagot={bagotti}")
            self.write2Console(f"{self.linenb:03d} {romaddr:03X} {romdata:02X}\t{ramaddr:03X} {ramdata:02X}\t  rst={rststate} rw={rwstate} wio={wiostate} bgt={bagotti}\r\n", insertMode=True)
            #print("typ=3", str(data))
        #print(str(data), len(data), typ)
        elif typ == 81:    #Q (read 1024 bytes)
            print(f"Dump current ROM (1024B) in progress")
            self.write2Console(f"ROM Current\r\n", insertMode=True)
            #write again but  to  console, this time.        
            for r in range(64):
                self.write2Console(f"{r:02X}\t")
                for l in range(16):
                    self.write2Console(f"{data[r*16+l]:02X} ", insertMode=True)
                self.write2Console(f"\r\n", insertMode=True)
            
            print("Dump ROM terminated")
            
        elif typ == 78:    #N (read 256 bytes)
            print(f"Dump current ROM (256B) in progress")
            self.write2Console(f"ROM Current\r\n", insertMode=True)
            #write again but  to  console, this time.        
            for r in range(16):
                self.write2Console(f"{r:02X}\t")
                for l in range(16):
                    self.write2Console(f"{data[r*16+l]:02X} ", insertMode=True)
                self.write2Console(f"\r\n", insertMode=True)
            
            print("Dump ROM terminated")
            
        elif typ == 82:    #R (read 128 bytes)
            if   self.ui.rb_sysconf.isChecked():
                memtyp = "sys conf"
            elif self.ui.rb_mnprn.isChecked():
                memtyp = "miniprinter"
            elif self.ui.rb_nvram.isChecked():
                memtyp = "nvram live"
            else:
                memtyp = "unknown source"

            print(f"Dump RAM {memtyp} in progress")
            self.write2Console(f"NVRAM Current ({memtyp})\r\n", insertMode=True)

            #write into memory inspection area            
            for r in range(16):
                for l in range(8):
                    lb = data[r*8+l]&0xF
                    hb = data[r*8+l]&0xF0
                    hb = hb>>4
                    self.nibbleField[r][2*l].setText(f"0X{lb:01X}")
                    self.nibbleField[r][2*l].setStyleSheet("background:rgb(21, 120, 34);color:rgb(255, 255, 255);")
                    self.nibbleField[r][2*l+1].setText(f"0X{hb:01X}")
                    self.nibbleField[r][2*l+1].setStyleSheet("background:rgb(21, 120, 34);color:rgb(255, 255, 255);")

                    self.nvrlist[r*8+l] = (data[r*8+l], data[r*8+l]) #(init value, current value)
                    
            #write again but  to  console, this time.        
            for r in range(8):
                self.write2Console(f"{r:02X}\t")
                for l in range(16):
                    self.write2Console(f"{data[r*16+l]:02X} ", insertMode=True)
                self.write2Console(f"\r\n", insertMode=True)
            
            print("Dump RAM terminated")
            self.read128Sig.emit(memtyp)
            
        elif typ == 71:   #G
            # 8b ROM data
            # 8b RAM data
            #12b ROM addr
            # "1010"
            self.linenb      += 1
            romdata      = data[0]
            ramdata      = data[1]
            romaddr      = data[2]+(data[3]&0x0F)*0x100
            gpaddr       = ((data[3]&0x30 )>>4)*0x100 + data[4]
            ramaddr      = data[4]
            #print(f"{romaddr:03X}\t{romdata:02X} rst={rststate} rw={rwstate} wio={wiostate} bagot={bagotti}")
            #next line for GP case (game prom spying
            #self.write2Console(f"{self.linenb:03d} romaddr={romaddr:03X} romdata={romdata:02X}\t ramdata={ramdata:02X}\t gpaddr={gpaddr:03X}\r\n", insertMode=True)
            #next line for standard trace of specific instruction
            self.write2Console(f"{self.linenb:03d} {romaddr:03X} {romdata:02X}\t ramaddr={ramaddr:03X}\t ramdata={ramdata:02X}\r\n", insertMode=True)
            #print("typ=3", str(data))
        #print(str(data), len(data), typ)
        elif typ == 89:   #Y for IO status
            io_os = data[0]*256 + data[1]
            io_is = data[2]*256 + data[3]
            #print("Y got", data[0], data[1], data[2], data[3], data[4], io_os, io_is)
            self.ui.label_out.setText(f"{io_os:016b}")
            self.ui.label_inp.setText(f"{io_is:016b}")
            
            self.ui.lcdNumber.setProperty("value", data[4]&0x0F)
            
            for i in range(24):
                byten = 6 - (i // 8)
                if data[byten]&(1<<(i%8)):
                    self.gpioled[i].setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                    #sound
                    if   i==11:
                        self.play(self.sdata100K)
                    elif i==12:
                        self.play(self.sdata10K)
                    elif i==13:
                        self.play(self.sdata1K)
                    elif i==14:
                        self.play(self.sdata100)
                    elif i==15:
                        self.play(self.sdata10)
                        
                else:
                    self.gpioled[i].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))

            for i in range(16):
                byten = 8 - (i // 8)
                if data[byten]&(1<<(i%8)):
                    self.b2led[i].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                else:
                    self.b2led[i].setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                    

            # if data[4]&0x01:
            #     self.ui.label_bonus1.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
            # else:
            #     self.ui.label_bonus1.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
            # if data[4]&0x02:
            #     self.ui.label_bonus2.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
            # else:
            #     self.ui.label_bonus2.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
            # if data[4]&0x04:
            #     self.ui.label_bonus4.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
            # else:
            #     self.ui.label_bonus4.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
            # if data[4]&0x08:
            #     self.ui.label_bonus8.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
            # else:
            #     self.ui.label_bonus8.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                
                
                
        else:
            if  typ == 65:  #'A'
                self.frameCntSig.emit("A")
                dspAstate = 1 if data[0]&0x80 else 0
                dspBstate = 1 if data[0]&0x40 else 0
                if   dspAstate == 0 and self.lastAstate == 1:
                    self.ui.label_DAState.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                elif dspAstate == 1 and self.lastAstate == 0:
                    self.ui.label_DAState.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                self.lastAstate = dspAstate
                if   dspBstate == 0 and self.lastBstate == 1:
                    self.ui.label_DBState.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                elif dspBstate == 1 and self.lastBstate == 0:
                    self.ui.label_DBState.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                self.lastBstate = dspBstate
                
                if dspAstate == 1:
                    #print("A display A mask")
                    return 
                if dspBstate == 1:
                    #print("A display B mask")
                    pass

                if   self.game_type == "Gottlieb":   
                    ballinplay = data[1:2]
                    tableau1   = data[2:5]
                    freeplay   = data[5:6]
                    tableau2   = data[6:]
                else:  #Recel case
                    ballinplay = data[9:7:-1]     #tilt/game over/ball in play | match number
                    tableau1   = data[7:3:-1]+b'0' #data[8] contains the dots state
                    freeplay   = data[1::-1]      #freeplay|extra ball, here
                    tableau2   = data[-7::]  +b'0' #data[-6] contains dots
                    
                aff1 = [self.ui.lcd1_6, self.ui.lcd1_5, self.ui.lcd1_4, self.ui.lcd1_3, self.ui.lcd1_2, self.ui.lcd1_1]
                aff2 = [self.ui.lcd2_6, self.ui.lcd2_5, self.ui.lcd2_4, self.ui.lcd2_3, self.ui.lcd2_2, self.ui.lcd2_1]
                aff5 = [self.ui.lcd5_2, self.ui.lcd5_1]
                aff6 = [self.ui.lcd6_2, self.ui.lcd6_1]

                aff3 = [self.ui.lcd3_6, self.ui.lcd3_5, self.ui.lcd3_4, self.ui.lcd3_3, self.ui.lcd3_2, self.ui.lcd3_1]
                aff4 = [self.ui.lcd4_6, self.ui.lcd4_5, self.ui.lcd4_4, self.ui.lcd4_3, self.ui.lcd4_2, self.ui.lcd4_1]

                cplleds1 = [self.ui.ldsp_1_1, self.ui.ldsp_1_2, self.ui.lcd1M_1, None]
                cplleds2 = [self.ui.ldsp_2_1, self.ui.ldsp_2_2, self.ui.lcd1M_2, None]

                if   self.game_type == "Gottlieb":                   
                    afflcdi(aff1, data[2:])
                    afflcdi(aff2, data[6:])
                    afflcdi(aff5, data[1:])
                    afflcdi(aff6, data[5:])
                else:
                    #player 1
                    data2=[((data[4]&0x0F)<<4)+((data[4]&0xF0)>>4),
                           ((data[3]&0x0F)<<4)+((data[3]&0xF0)>>4),
                           ((data[2]&0x0F)<<4)+0x0F]
                    #print(f"leds player 1: {((data[2]&0xF0)>>4):04b}")
                    affcplleds(cplleds1, ((data[2]&0xF0)>>4))
                    afflcdi(aff1, data2)   #tableau 1

                    #player2                    
                    data2=[((data[8]&0x0F)<<4)+((data[8]&0xF0)>>4),
                           ((data[7]&0x0F)<<4)+((data[7]&0xF0)>>4),
                           ((data[6]&0x0F)<<4)+0x0F]
                    affcplleds(cplleds2, ((data[6]&0xF0)>>4))
                    
                    
                    afflcdi(aff2, data2)     #tableau 2
                    
                    #afflcdi(aff5, data[5:])    #match number
                    afflcdi(aff6, data[1:])    #freeplay/EB

                    #match number
                    for i in range(10):
                        #print(i,(~data[5]&0x0F),data[5])
                        if i==(~data[5]&0x0F):
                            self.mled[i].setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                        else:
                            self.mled[i].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))

                    #ball in play + game over
                    bstat = (data[5]&0x70)>>4
                    bstat = bstat ^ 0b0111
                    #print(f"{bstat:04b}   { ((data[5]&0x70))>>4:04b}")
                    for i in range(5):
                        if i==bstat:
                            self.bip[i].setVisible (True)
                            self.bipt[i].setVisible(True)
                        else:
                            self.bip[i].setVisible (False)
                            self.bipt[i].setVisible(False)
                    
                    if bstat== 7:
                        self.bip[5].setVisible (True)
                        self.bipt[5].setVisible(True)
                    else:
                        self.bip[5].setVisible (False)
                        self.bipt[5].setVisible(False)
                        
                                
                    #tilt
                    if ((~data[5]&0x80)):
                        self.tiltIndicator.setVisible(True)
                    else:
                        self.tiltIndicator.setVisible(False)
                        

                    
                x = fromBcd2Int(tableau1)
                if x == -1:
                    self.ui.lcdNumber_1.setDigitCount(0)
                else:
                    self.ui.lcdNumber_1.setDigitCount(6)
                    self.ui.lcdNumber_1.setProperty("value", x)
                x = fromBcd2Int(tableau2)
                if x == -1:
                    self.ui.lcdNumber_2.setDigitCount(0)
                else:
                    self.ui.lcdNumber_2.setDigitCount(6)
                    self.ui.lcdNumber_2.setProperty("value", x)
                self.ui.lcdNumber_6.setProperty("value", fromBcd2Int(ballinplay))
                self.ui.lcdNumber_5.setProperty("value", fromBcd2Int(freeplay))
                
            elif typ == 66:  #'B'
                dspAstate = 1 if data[0]&0x80 else 0
                dspBstate = 1 if data[0]&0x40 else 0
                if   dspAstate == 0 and self.lastAstate == 1:
                    self.ui.label_DAState.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                elif dspAstate == 1 and self.lastAstate == 0:
                    self.ui.label_DAState.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                self.lastAstate = dspAstate
                if   dspBstate == 0 and self.lastBstate == 1:
                    self.ui.label_DBState.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                elif dspBstate == 1 and self.lastBstate == 0:
                    self.ui.label_DBState.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                self.lastBstate = dspBstate

                if dspAstate == 1:
                    #print("B display A mask")
                    return 
                if dspBstate == 1:
                    #print("B display B mask")
                    pass

                if   self.game_type == "Gottlieb":   
                    tableau3   = data[2:5]
                    tableau4   = data[6:]
                else:
                           
                    tableau3   = data[-7::]    + b'0'
                    tableau4   = data[7:2:-1]  + b'0'

                x = fromBcd2Int(tableau3)
                if x == -1:
                    self.ui.lcdNumber_3.setDigitCount(0)
                else:
                    self.ui.lcdNumber_3.setDigitCount(6)
                    self.ui.lcdNumber_3.setProperty("value", x)
                    
                    
                x = fromBcd2Int(tableau4)
                if x == -1:
                    self.ui.lcdNumber_4.setDigitCount(0)
                else:
                    self.ui.lcdNumber_4.setDigitCount(6)
                    self.ui.lcdNumber_4.setProperty("value", x)
                    
                aff3 = [self.ui.lcd3_6, self.ui.lcd3_5, self.ui.lcd3_4, self.ui.lcd3_3, self.ui.lcd3_2, self.ui.lcd3_1]
                aff4 = [self.ui.lcd4_6, self.ui.lcd4_5, self.ui.lcd4_4, self.ui.lcd4_3, self.ui.lcd4_2, self.ui.lcd4_1]
                aff5 = [self.ui.lcd5_2, self.ui.lcd5_1]  #credits
                cplleds3 = [self.ui.ldsp_3_1, self.ui.ldsp_3_2, self.ui.lcd1M_3, None]
                cplleds4 = [self.ui.ldsp_4_1, self.ui.ldsp_4_2, self.ui.lcd1M_4, None]

                if   self.game_type == "Gottlieb":                                  
                    afflcdi(aff3, data[2:])
                    afflcdi(aff4, data[6:])
                else:
                    #player 4
                    data2=[((data[4]&0x0F)<<4)+((data[4]&0xF0)>>4),
                           ((data[3]&0x0F)<<4)+((data[3]&0xF0)>>4),
                           ((data[2]&0x0F)<<4)+0x0F]
                           
                    afflcdi(aff4, data2)   #tableau 4
                    affcplleds(cplleds4, ((data[2]&0xF0)>>4))
                    
                    #player3                    
                    data2=[((data[8]&0x0F)<<4)+((data[8]&0xF0)>>4),
                           ((data[7]&0x0F)<<4)+((data[7]&0xF0)>>4),
                           ((data[6]&0x0F)<<4)+0x0F]
                    
                    afflcdi(aff3, data2)     #tableau 3
                    affcplleds(cplleds3, ((data[6]&0xF0)>>4))
                    
                    afflcdi(aff5, data[1:])    #credits

            elif typ == 90: #5A 'Z'
                crc = (data[0]<<8) | (data[1])    
                self.write2Console(f"Fletcher's crc: {crc:04X}\r\n", insertMode=True)
                print(f"Fletcher's crc: {crc:04X}\r\n")
                self.fletcherSig.emit(crc)

            elif typ == 64: #40 '@' reset ack frame
                ident = data[0]
                rtype = data[1]
                #self.write2Console(f"Reset Ack Frame received: Ident: {ident:02X}. Reset Type: {rtype:02X}\r\n")
                self.resetAckSig.emit(rtype)
                    
            elif typ == 67:  #'C'
                #print("typ=67", str(data))
                if not data[0]&0x08:
                    self.ui.checkBox_1.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_1.setCheckState(QtCore.Qt.Unchecked)
                    
                if not data[0]&0x04:
                    self.ui.checkBox_2.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_2.setCheckState(QtCore.Qt.Unchecked)

                if not data[0]&0x02:
                    self.ui.checkBox_3.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_3.setCheckState(QtCore.Qt.Unchecked)

                if not data[0]&0x01:
                    self.ui.checkBox_4.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_4.setCheckState(QtCore.Qt.Unchecked)
                    
                if not data[0]&0x80:
                    self.ui.checkBox_5.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_5.setCheckState(QtCore.Qt.Unchecked)

                if not data[0]&0x40:
                    self.ui.checkBox_6.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_6.setCheckState(QtCore.Qt.Unchecked)
                    
                if not data[0]&0x20:
                    self.ui.checkBox_7.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_7.setCheckState(QtCore.Qt.Unchecked)

                if not data[0]&0x10:
                    self.ui.checkBox_8.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_8.setCheckState(QtCore.Qt.Unchecked)


                if not data[1]&0x01:
                    self.ui.checkBox_9.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_9.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x02:
                    self.ui.checkBox_10.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_10.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x04:
                    self.ui.checkBox_11.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_11.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x08:
                    self.ui.checkBox_12.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_12.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x10:
                    self.ui.checkBox_13.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_13.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x20:
                    self.ui.checkBox_14.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_14.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x40:
                    self.ui.checkBox_15.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_15.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x80:
                    self.ui.checkBox_16.setCheckState(QtCore.Qt.Checked) 
                else:
                    self.ui.checkBox_16.setCheckState(QtCore.Qt.Unchecked)

                    
                if not data[2]&0x01:
                    self.ui.checkBox_17.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_17.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x02:
                    self.ui.checkBox_18.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_18.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x04:
                    self.ui.checkBox_19.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_19.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x08:
                    self.ui.checkBox_20.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_20.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x10:
                    self.ui.checkBox_21.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_21.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x20:
                    self.ui.checkBox_22.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_22.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x40:
                    self.ui.checkBox_23.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_23.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x80:
                    self.ui.checkBox_24.setCheckState(QtCore.Qt.Checked) 
                else:
                    self.ui.checkBox_24.setCheckState(QtCore.Qt.Unchecked)

                    
                                   
                # self.ui.ldip1_2.setText(f"{data[0]:08b}")
                # self.ui.ldip2_2.setText(f"{data[1]:08b}")
                # self.ui.ldip3_2.setText(f"{data[2]:08b}")

            elif typ == 80: #'P'
                #print(str(data))
                uilabels = [
                    self.ui.label_D0_F, self.ui.label_D0_E, self.ui.label_D0_D, self.ui.label_D0_C,
                    self.ui.label_D0_B, self.ui.label_D0_A, self.ui.label_D0_9, self.ui.label_D0_8,
                    self.ui.label_D0_7, self.ui.label_D0_6, self.ui.label_D0_5, self.ui.label_D0_4,
                    self.ui.label_D0_3, self.ui.label_D0_2, self.ui.label_D0_1, self.ui.label_D0_0
                            ]
                #for i in range(16):
                for i in range(16):
                    #print(uilabels[i].text()[-2:])
                    if  uilabels[i].text()[-2:] != f"{data[2*i+1]:02X}":
                        uilabels[i].setStyleSheet("QLabel { background-color : red; color : white; }")
                    else:
                        if self.vientdecliquer >= 50:
                            uilabels[i].setStyleSheet("QLabel { background-color : green; color : white; }")
                            self.vientdecliquer = 0
                        else:
                            self.vientdecliquer += 1
                            
                    
                    
                    
                    self.last_uilabels[i] = uilabels[i].text()[-2:]
                    uilabels[i].setText(f"{data[2*i]:02X} {data[2*i+1]:02X}")
                    
                        
                
            elif typ == 83:  #'S'
                #print(len(data),"\t",str(data))
                rows, cols = self.swmRows, self.swmCols  #(8,5) or (10,4)  

                #self.write2Console(f"switches:\n{data[0]:08b}\n{data[1]:08b}\n{data[2]:08b}\n{data[3]:08b}\n{data[4]:08b}", insertMode=False)
                self.msg83 = f"switches:\n{data[0]:08b}\n{data[1]:08b}\n{data[2]:08b}\n{data[3]:08b}\n{data[4]:08b}"
                #print(self.msg83)
                for i in range(rows*cols):
                    bitnumber  = i%8
                    bytenumber = i//8
                    c = cols-1 - i%cols
                    r = bytenumber*2
                    if bitnumber<4:
                        r+=1
                    #print(i, bitnumber, bytenumber, r,c)
                    if data[bytenumber]&(1<<bitnumber):
                        self.led[r][c].setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                    else:
                        self.led[r][c].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                            
            elif typ == 68:  #'D'
                #print(str(data))
                #self.write2Console(f"diag {data[0]:08b} {data[1]:08b} {data[2]:08b}{data[3]:08b}", insertMode=True)
                self.msg68 = f"diag {data[0]:08b} {data[1]:08b} {data[2]:08b}{data[3]:08b}"

            elif typ == 86:  #'V' 2 bytes
                #data[0] is superMode&010000
                #data[1] is always 0, or 255 after pressing reset button
                if data[1] == 255:
                    self.write2Console(f"Reset Switch pressed: {data[0]:02X} / {data[1]:02X}\r\n", insertMode=True)
                    self.resetButSig.emit(data[0])

            elif typ == 69:  #'E'
                #print(str(data))
                self.write2Console(f"dip switches: {data[0]:08b}\r\n", insertMode=True)
                self.write2Console(f"SPI Flash ID: {data[1]:02X} {data[2]:02X} {data[3]:02X} {data[4]:02X} {data[5]:02X} {data[6]:02X} {data[7]:02X} {data[8]:02X} \r\n", insertMode=True)
                #self.write2Console(f"SPI FlIdent2: {data[14]:02X} {data[15]:02X} {data[16]:02X} {data[17]:02X} {data[18]:02X} {data[19]:02X} {data[20]:02X} {data[21]:02X} {data[22]:02X} {data[23]:02X} {data[24]:02X} {data[25]:02X} {data[26]:02X} \r\n", insertMode=True)
                #self.msg68 = f"diag {data[0]:08b} {data[1]:08b} {data[2]:08b}{data[3]:08b}"

            elif typ == 120:  #'x'
                #print(data[0],data[1],data[2],data[3])
                rssi = int.from_bytes(data, byteorder='little', signed=True)
                #self.write2Console(f"RSSI: {rssi} dB\r\n", insertMode=True)
                rssitxt = f"(RSSI: {rssi} dB)"
                
                self.ui.label_RSSI.setVisible(True)
                self.ui.label_RSSI.setText(rssitxt)
                #self.write2Console(f"SPI FlIdent2: {data[14]:02X} {data[15]:02X} {data[16]:02X} {data[17]:02X} {data[18]:02X} {data[19]:02X} {data[20]:02X} {data[21]:02X} {data[22]:02X} {data[23]:02X} {data[24]:02X} {data[25]:02X} {data[26]:02X} \r\n", insertMode=True)
                #self.msg68 = f"diag {data[0]:08b} {data[1]:08b} {data[2]:08b}{data[3]:08b}"

        #self.write2Console(self.msg83+"\n"+self.msg68, insertMode=False)
            
            #int_val = int.from_bytes(data, "big", signed=False)
            #int_val *= 10
            #self.ui.lcdNumber_1.setProperty("value", 131)
    def closeEvent(self, event):

        # Now we define the closeEvent
        # This is called whenever a window is closed.
        # It is passed an event which we can choose to accept or reject, but in this case we'll just pass it on after we're done.
        
        # First we need to get the current size and position of the window.
        # This can be fetchesd using the built in saveGeometry() method. 
        # This is got back as a byte array. It won't really make sense to a human directly, but it makes sense to Qt.
        print("bye")
        geometry = self.saveGeometry()
        
        #print(geometry)
        # Once we know the geometry we can save it in our settings under geometry
        self.settings.setValue('geometry', geometry)
        self.settings.setValue('state', self.saveState())
        self.settings.setValue('host', self.ui.lineEdit.text())
        self.settings.setValue('port', self.ui.lineEdit_2.text())
        self.settings.setValue('face', self.face)
        self.settings.setValue('sound', self.sound)

        # Finally we pass the event to the class we inherit from. It can choose to accept or reject the event, but we don't need to deal with it ourselves
        super(MainForm, self).closeEvent(event)


    def catch128SigMain(self, memTypStr):
        print("memTyp", memTypStr)
        if memTypStr != "sys conf":
            return 
        
        self.ui.plainTextEdit.clear()             

        #game
        rg = self.nvrlist[2*8+1][1]*256+self.nvrlist[2*8+0][1]
        cg = self.nvrlist[3*8+1][1]*256+self.nvrlist[3*8+0][1]

        #rom
        rr = self.nvrlist[4*8+1][1]*256+self.nvrlist[4*8+0][1]
        cr = self.nvrlist[5*8+1][1]*256+self.nvrlist[5*8+0][1]

        print(f"{cg:04X}")
        print(f"{rg:04X}")
        print(f"{cr:04X}")
        print(f"{rr:04X}")

 
        self.ui.label_crc_cr.setText(f"{cr:04X}")
        
       
        candidates_cg =  [x for x in RscPin.Models.keys() if RscPin.Models[x]["Game Fletcher"]==cg ]
        candidates_rg =  [x for x in RscPin.Models.keys() if RscPin.Models[x]["Game Fletcher"]==rg ]        
        
        mdl_cg  = [RscPin.Models[x]["#Model"] for x in candidates_cg]
        binf_cg = [RscPin.Models[x]["A1762 bin"] for x in candidates_cg]

        print("/".join(candidates_cg) if len(candidates_cg)>0 else "Unknown" )                    
        print("/".join(candidates_rg) if len(candidates_rg)>0 else "Unknown" )
        
        
        if rg != cg:
            cmtTxt = f"Running factory game because crcs don't match. ({rg:04X}/{cg:04X})"
            self.ui.label_txt_cg.setStyleSheet("QLabel { background-color : red; color : white; font: italic; padding-left : 5px;}")
        else:
            cmtTxt = ""
            self.ui.label_txt_cg.setStyleSheet("QLabel { background-color : green; color : white; font: bold; padding-left : 5px;}")
            

        self.ui.label_crc_cg.setText(f"{cg:04X}")
        self.ui.label_txt_cg.setText("/".join(candidates_cg) if len(candidates_cg)>0 else "Unknown" )                    
        self.ui.label_mdl_cg.setText("/".join(mdl_cg) if len(mdl_cg)>0 else "Undef" )                    
        self.ui.plainTextEdit.appendPlainText(cmtTxt)             
        
        try:
            cr_txt = RscPin.Bios[cr][1]
        except:
            cr_txt = "Unknown"
        
        self.ui.label_txt_cr.setText(cr_txt)
        self.ui.label_crc_cr.setText(f"{cr:04X}")
            
        if rr != cr:
            cmtTxt = f"Running factory BIOS because crcs don't match. ({rr:04X}/{cr:04X})"
            self.ui.label_txt_cr.setStyleSheet("QLabel { background-color : red; color : white; font: italic; padding-left : 5px;}")
        else:
            cmtTxt = ""
            self.ui.label_txt_cr.setStyleSheet("QLabel { background-color : green; color : white; font: bold; padding-left : 5px;}")
            
        self.ui.plainTextEdit.appendPlainText(cmtTxt)             

        if len(candidates_cg)>0:  
            try: 
                fnl = RscPin.Bios[cr][0]
                # print("fnl", fnl)     
                # print("binf_cg", binf_cg)     
                for f in binf_cg:
                    if f not in fnl:
                        txt = "/".join(candidates_cg)
                        self.ui.plainTextEdit.appendPlainText(f"Warning : {f} notoriously incompatible with {txt} ")             
            except:
                pass
            

    def magarzolerie(self, i, j):
        '''
        slot for handling signal textchanged in nibbleField
        which is changing color to red
        '''
        #print("zobi", i, j)
        try:
            mynibble   = int(self.nibbleField[i][j].text(), 0)
        except:
            try:
                mynibble = int("0x"+self.nibbleField[i][j].text(), 16)
            except:
                mynibble = -1

        if mynibble != mynibble&0xF:
            badentry = True
            mynibble = 0
        else:
            badentry =  False    
        #print("mynibble", mynibble)    
        pnibblenum = i*16+j
        pbytenum   = pnibblenum//2
        
        #modify current ([1])
        if pnibblenum%2:
            #this is a hi nibble
            mynewbyte = (mynibble<<4) + (self.nvrlist[pbytenum][1] & 0x0F)
            self.nvrlist[pbytenum] = (self.nvrlist[pbytenum][0], mynewbyte)
        else:
            #this is a lo nibble
            mynewbyte = mynibble    + (self.nvrlist[pbytenum][1] & 0xF0)
            self.nvrlist[pbytenum] = (self.nvrlist[pbytenum][0], mynewbyte)

        if badentry == True:
            self.nibbleField[i][j].setStyleSheet("background:rgb(160, 160, 10);color:rgb(255, 255, 255);")
            self.nibbleField[i][j].setToolTip("Bad entry. Will take it as 0")
        elif self.nvrlist[pbytenum][1] == self.nvrlist[pbytenum][0]:            
            self.nibbleField[i][j].setStyleSheet("background:rgb(22, 140, 35);color:rgb(255, 255, 255);")
            self.nibbleField[i][j].setToolTip("Nibble OK")
        else:
            self.nibbleField[i][j].setStyleSheet("background:rgb(140, 34, 35);color:rgb(255, 255, 255);")
            self.nibbleField[i][j].setToolTip("Nibble OK")
            

    def setupb2s(self):
        self.b2led = [0]*16
        self.b2tooltip = [
            "L/51",   #IO-0
            "L/52",   #IO-1
            "L/54",   #IO-2
            "L/58",   #IO-3
            "L/41",   #IO-4
            "L/42",   #IO-5
            "L/44",   #IO-6
            "L/48",   #IO-7
            "L/31",   #IO-8
            "L/32",   #IO-9
            "L/34",   #IO-10
            "L/38",   #IO-11
            "L/21",   #IO-12
            "L/22",   #IO-13
            "L/24",   #IO-14
            "L/28",   #IO-15
            ]

        for i in range(16):
            self.b2led[i]=QtWidgets.QLabel(self.ui.groupBox_7)
            #self.gpioled[i].setGeometry(QtCore.QRect(60+i*28, 90, 20, 20))
            self.b2led[i].setText("")
            self.b2led[i].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
            self.ui.horizontalLayout_16.addWidget(self.b2led[i])
            self.b2led[i].setMaximumSize(QtCore.QSize(31, 31))
            self.b2led[i].setScaledContents(True)
            self.b2led[i].setObjectName(f"b2led_{i}")
            #self.gpioled[i].mousePressEvent = lambda _, x=i, y=j : self.foo(x, y)
            try:
                self.b2led[i].setToolTip(self.b2tooltip[i])
            except:
                self.b2led[i].setToolTip(f"b2led_{i}")
        
        
    def setupgpios(self):
        self.gpioled = [0]*24
        self.gpiotooltip = [
            "C/#F",  #0     group 3-1
            "C/#E",  #1     group 3-2
            "C/#D",  #2     group 3-4
            "C/#C",  #3     group 3-8
            
            "C/#B",  #4     group 4-1
            "C/#A",  #5     group 4-2
            "C/#9",  #6     group 4-4
            "C/#8",  #7     group 4-8
            
            "C/#7",  #8     group 5-1
            "C/#6 (knocker)",  #9     group 5-2
            "NC",    #10     group 5-4
            "Sound-100K",    #11     group 5-8
            
            "Sound-10K",     #12     group 6-1
            "Sound-1K",      #13     group 6-2
            "Sound-100",     #14     group 6-4
            "Sound-10",      #15     group 6-8
            
            "L/61 (bonus)",  #16    group 7-1
            "L/62 (bonus)",  #17    group 7-2
            "L/64 (bonus)",  #18    group 7-4
            "L/68 (bonus)",  #19    group 7-8
            
            "L/71",   #20    group 8-1
            "L/72",   #21    group 8-2
            "L/74",   #22    group 8-4
            "PLAY SIGNAL",   #23    group 8-8
            
            ]
        
        for i in range(24):
            self.gpioled[i]=QtWidgets.QLabel(self.ui.groupBox_5)
            #self.gpioled[i].setGeometry(QtCore.QRect(60+i*28, 90, 20, 20))
            self.gpioled[i].setText("")
            self.gpioled[i].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
            self.ui.horizontalLayout_13.addWidget(self.gpioled[i])
            self.gpioled[i].setMaximumSize(QtCore.QSize(31, 31))
            self.gpioled[i].setScaledContents(True)
            self.gpioled[i].setObjectName(f"gpioled_{i}")
            #self.gpioled[i].mousePressEvent = lambda _, x=i, y=j : self.foo(x, y)
            try:
                self.gpioled[i].setToolTip(self.gpiotooltip[i])
            except:
                self.gpioled[i].setToolTip(f"gpioled_{i+1}")

               
    def setupnvram(self):
        self.nibbleField = [0]*16
        myfont   =  QtGui.QFont("Courier New", self.fontsz)
        
        myfont10 =  QtGui.QFont("Courier New", 10)
        fm = QFontMetrics(myfont)
        w = fm.boundingRect("0B0000").width()
        
        for i in range(16):
            etiq=QtWidgets.QLabel(self.ui.scrollAreaWidgetContents)
            etiq.setText(f"{i:02X}")
            etiq.setObjectName(f"SRlab_{i}")
            #etiq.setStyleSheet("text-align:center;")
            etiq.setAlignment(Qt.AlignCenter)
            etiq.setFont(myfont)
            self.ui.gridLayout_7.addWidget(etiq, 0, i+1, 1, 1)
            

        for i in range(16):
            etiq=QtWidgets.QLabel(self.ui.scrollAreaWidgetContents)
            etiq.setText(f"{i:02X}")
            etiq.setObjectName(f"RRlab_{i}")
            #etiq.setStyleSheet("text-align:center;")
            etiq.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            etiq.setFont(myfont)
            self.ui.gridLayout_7.addWidget(etiq, i+1, 0, 1, 1)

        # for i in range(cols):
        #     rled=QtWidgets.QLabel(self.ui.groupBox)
        #     rled.setGeometry(QtCore.QRect(60-28, 90+i*36, 20, 20))
        #     rled.setText(f"R{i}")
        #     rled.setObjectName(f"rled_{i}")

        self.nvrlist = [(0, 0)]*128        

        for i in range(16):
            self.nibbleField[i] = [0]*16
            for j in range(16):
                self.nibbleField[i][j] = QtWidgets.QLineEdit(self.ui.scrollAreaWidgetContents)
                self.nibbleField[i][j].setObjectName(f"nibbles_{i}{j}")
                #self.nibbleField[i][j].setGeometry(QtCore.QRect(60+i*28, 90+j*36, 20, 20))
                self.nibbleField[i][j].setText("0")
                self.nibbleField[i][j].setStyleSheet("background:rgb(120, 120, 120);color:rgb(255, 255, 255);")
                self.nibbleField[i][j].setAlignment(Qt.AlignCenter)
                self.nibbleField[i][j].setFont(myfont)

                self.nibbleField[i][j].setFixedWidth(w+10)
                self.ui.gridLayout_7.addWidget(self.nibbleField[i][j], i+1, j+1, 1, 1)
                self.nibbleField[i][j].textChanged.connect(partial(self.magarzolerie, i, j))

                #self.nibbleField[i][j].setTextMargins (left, top, right, bottom)
                self.nibbleField[i][j].setTextMargins (1, 3, 1, 3)

    def setupleds(self):
        rows, cols = self.swmRows, self.swmCols    
        self.led = [0]*rows
        self.ledlabel = [0]*rows
        deltax = 50
        deltay = 50
        balldia = 48
        rowSpan = 1
        columnSpan = 1
        self.ui.groupBox.setMinimumSize(QtCore.QSize(balldia*rows+120, balldia*cols+120))
        #self.ui.groupBox.setMaximumSize(QtCore.QSize(balldia*rows+120, balldia*cols+120))
        #self.ui.groupBox.setMinimumSize(QtCore.QSize(deltax*rows+60, deltay*cols+60))
        self.ui.dockWidget_2.setMaximumSize(QtCore.QSize(524287, 524287))
        self.ui.dockWidget_2.setMinimumSize(QtCore.QSize(100, 100))
        #self.ui.groupBox.setGeometry(QtCore.QRect(1000, 0, 5000, 25))
        self.ui.groupBox.setFixedSize((QtCore.QSize(balldia*(rows+2), balldia*(cols+2))))
        for i in range(rows):
            #rled=QtWidgets.QLabel(self.ui.groupBox)
            rled=QtWidgets.QLabel()
            #rled.setGeometry(QtCore.QRect(60+i*deltax, 90-deltax, balldia, balldia))
            rled.setGeometry(QtCore.QRect(0, 0, balldia, balldia))
            rled.setScaledContents(True)
            rled.setText(f"S{i}")
            rled.setObjectName(f"sled_{i}")
            self.ui.groupBox.layout().addWidget(rled, 0, i+1, rowSpan, columnSpan, Qt.AlignCenter)
            #self.ui.groupBox.layout().addWidget(rled, 0, i+1)
        for i in range(cols):
            rled=QtWidgets.QLabel()
            #rled.setGeometry(QtCore.QRect(60-deltax, 90+i*deltay, balldia, balldia))
            rled.setGeometry(QtCore.QRect(0, 0, balldia, balldia))
            rled.setScaledContents(True)
            rled.setText(f"R{chr(i+0x41)}")
            rled.setObjectName(f"rled_{i}")
            self.ui.groupBox.layout().addWidget(rled, i+1, 0)
            
        for i in range(rows):
            self.led[i]=[0]*cols
            self.ledlabel[i]=[0]*cols
            for j in range(cols):
                # self.ledlabel[i][j]=QtWidgets.QLabel()
                # self.led[i][j]=QtWidgets.QLabel()
                self.ledlabel[i][j]= ClkLabel()
                self.led[i][j]     = ClkLabel()
                #self.led[i][j].setGeometry(QtCore.QRect(60+i*deltax, 90+j*deltay, balldia, balldia))
                self.led[i][j].setGeometry(QtCore.QRect(0, 0, balldia, balldia))
                if i%2 and j%2:
                    self.led[i][j].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                else:
                    self.led[i][j].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                self.led[i][j].setScaledContents(True)
                #self.ledlabel[i][j].setScaledContents(True)
                self.led[i][j].setObjectName(f"led_{i}{j}")
                
                # self.led[i][j].mousePressEvent = lambda _, x=i, y=j : self.foo(x, y)
                # self.ledlabel[i][j].mousePressEvent = lambda _, x=i, y=j : self.foo(x, y)
                self.led[i][j].simpleClicked.connect(partial(self.foo2, i, j, 1))
                self.ledlabel[i][j].simpleClicked.connect(partial(self.foo2, i, j, 1))
                self.led[i][j].tripleClicked.connect(partial(self.foo2, i, j, 3))
                self.ledlabel[i][j].tripleClicked.connect(partial(self.foo2, i, j, 3))

                self.led[i][j].setToolTip(self.Swtttext[i][j])
                self.ledlabel[i][j].setToolTip(self.Swtttext[i][j])
                self.ui.groupBox.layout().addWidget(self.led[i][j], j+1, i+1)
                self.ui.groupBox.layout().addWidget(self.ledlabel[i][j], j+1, i+1)
                #self.led[i][j].setText("")
                #self.ledlabel[i][j].setText(self.Swtttext[i][j])
                self.ledlabel[i][j].setAlignment(Qt.AlignCenter)
                #self.ledlabel[i][j].setMinimumHeight(QtGui.QPixmap(":/x/ledgrey.png").height())
                #self.ledlabel[i][j].setGeometry(QtCore.QRect(60+i*deltax, 90-deltax, 120, balldia))
                self.ledlabel[i][j].setStyleSheet("""
                                                    QLabel {background-color: transparent;
                                                    color: white;
                                                    font: bold 10px;
                                                    padding: 0px 10px 0px 10px;
                                                             }
                                                    QToolTip {background-color: white;
                                                    color: #9F1642;
                                                    font:  24px;
                                                    padding: 0px 10px 0px 10px;
                                                             }
                                                  """)
        # print (self.led)
        # for i in range(8):
        #     for j in range(5):
        #         if i%2 and j%2:
        #             self.led[i][j].setPixmap(QtGui.QPixmap(":/x/ledon.png"))

        #print(self.ui.groupBox.layout().objectName())

    def foo(self, i, j):
        strb = i.to_bytes(1, byteorder='big')
        ret  = (1<<j).to_bytes(1, byteorder='big')
        delay = 30 #(300ms)
        dly = delay.to_bytes(1, byteorder='big')
        print("message request is", b'YS'+strb+ret+dly)
        try:
            self.thread.sock.send(b'YS'+strb+ret+dly)
        except:
            pass
   
    def foo2(self, i, j, nbclk):
        strb = i.to_bytes(1, byteorder='big')
        ret  = (1<<j).to_bytes(1, byteorder='big')
        if nbclk == 3:
            delay = 0xFF #(+l'infini)
        else:
            delay = 10 #(300ms)
        dly = delay.to_bytes(1, byteorder='big')
        print("message request is", b'YS'+strb+ret+dly)
        try:
            self.thread.sock.send(b'YS'+strb+ret+dly)
        except:
            pass
   
    def setupballinplay(self):
        self.bip = [0]*6
        self.bipt = [0]*6
        for i in range(5):
            self.bip[i]=QtWidgets.QLabel(self.ui.centralwidget)
            self.bip[i].setGeometry(QtCore.QRect(300+i*30, 365, 20, 20))
            self.bip[i].setPixmap(QtGui.QPixmap(":/x/ledyellow"))
            self.bip[i].setScaledContents(True)
            self.bip[i].setObjectName(f"bip{i}")
            
            self.bipt[i]=QtWidgets.QLabel(self.ui.centralwidget)
            self.bipt[i].setGeometry(QtCore.QRect(300+i*30, 365, 20, 20))
            self.bipt[i].setStyleSheet("QLabel { background-color : transparent; color : darkGreen; font-size: 14; font-weight: bold;}")
            self.bipt[i].setText(f"  {i+1} ")
            self.bipt[i].setScaledContents(True)
            self.bipt[i].setObjectName(f"bipt{i}")

        self.bip[5]=QtWidgets.QLabel(self.ui.centralwidget)
        self.bip[5].setGeometry(QtCore.QRect(300, 365, 20, 20))
        self.bip[5].setPixmap(QtGui.QPixmap(":/x/ledyellow"))
        self.bip[5].setScaledContents(True)
        self.bip[5].setObjectName(f"bip5")
        
        self.bipt[5]=QtWidgets.QLabel(self.ui.centralwidget)
        self.bipt[5].setGeometry(QtCore.QRect(300, 365, 100, 20))
        self.bipt[5].setStyleSheet("QLabel { background-color : orange; color : white; font-weight: bold;}")
        self.bipt[5].setText(f"  GAME OVER")
        self.bipt[5].setScaledContents(True)
        self.bipt[5].setObjectName(f"bipt5")


        self.tiltIndicator = QtWidgets.QLabel(self.ui.centralwidget)
        self.tiltIndicator.setGeometry(QtCore.QRect(175, 425, 50, 20))
        self.tiltIndicator.setStyleSheet("QLabel { background-color : orange; color : white; font-weight: bold;}")
        self.tiltIndicator.setText(f" T I L T")
        self.tiltIndicator.setScaledContents(True)

    def setupmatchleds(self):
        
        self.mled  = [0]*10
        self.mledt = [0]*10
        
        # for i in range(8):
        #     rled=QtWidgets.QLabel(self.ui.groupBox)
        #     rled.setGeometry(QtCore.QRect(60+i*28, 90-28, 20, 20))
        #     rled.setText(f"S{i}")
        #     rled.setObjectName(f"sled_{i}")
            
        ccenter = (419.0, 165.0)
        cr      =  28.0

        for i in range(10):
            self.mledt[i]=QtWidgets.QLabel(self.ui.centralwidget)
            xc = ccenter[0] + (cr+20)*math.cos(2.0*math.pi*i/10.0 + math.pi/2.0)
            yc = ccenter[1] + (cr+20)*math.sin(2.0*math.pi*i/10.0 + math.pi/2.0)
            xc = int(xc)
            yc = int(yc)
            self.mledt[i].setGeometry(QtCore.QRect(xc, yc, 20, 20))
            self.mledt[i].setStyleSheet("QLabel { background-color : black; color : white; }")

            self.mledt[i].setText(str(i)+"0")
            self.mledt[i].setScaledContents(True)
            self.mledt[i].setObjectName(f"matchledt_{i}")
          
        for i in range(10):
            self.mled[i]=QtWidgets.QLabel(self.ui.centralwidget)
            xc = ccenter[0] + cr*math.cos(2.0*math.pi*i/10.0 + math.pi/2.0)
            yc = ccenter[1] + cr*math.sin(2.0*math.pi*i/10.0 + math.pi/2.0)
            xc = int(xc)
            yc = int(yc)
            self.mled[i].setGeometry(QtCore.QRect(xc, yc, 20, 20))
            self.mled[i].setText("")
            self.mled[i].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
            self.mled[i].setScaledContents(True)
            self.mled[i].setObjectName(f"matchled_{i}")


#########################
#
#
#Worker is the place where the comm is
#
#########################
class Worker(QThread):
    output    = pyqtSignal(bytearray, int)
    connled   = pyqtSignal(str)
    workerErr = pyqtSignal(str)
    commErr   = pyqtSignal(str)
    def __init__(self, parent = None, HOST="192.168.1.26", PORT=23):
        QThread.__init__(self, parent)
        self.exiting = False
                
        #HOST, PORT = "192.168.1.26", 23

        self.HOST = HOST
        self.PORT = PORT
        
        
        
        #
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # try:
        #     self.sock.bind((HOST, PORT))
        # except OSError as error :
        #     print(error)
        #     self.exiting = True
        #     self.wait()
            
    def __del__(self):    
        self.exiting = True
        self.wait()
        
    def render(self):    
        self.start()

    
    def quit(self):
        print("socket close")
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except:
            pass
        try:
            self.sock.close()
        except:
            pass
        
    def run(self):        
        # Note: This is never called directly. It is called by Qt once the
        # thread environment has been set up.
        while True:
            print("Hi, connection to", (self.HOST, self.PORT))
            #brutUrl = socket.gethostbyname(self.HOST)
            while True:
                self.connled.emit("yellow")
    
                try:
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.settimeout(8.0)
                    #self.sock.setblocking(False)
                    print("Trying", (self.HOST, self.PORT))
                    #print("  In thread", self)
                    self.sock.connect((self.HOST, int(self.PORT)))
                    #self.sock.bind((self.HOST, int(self.PORT)))
                    #self.sock.connect(("WiFlip_iface", int(self.PORT)))
                    break
                except ConnectionRefusedError:
                    print("Connection refused. Abort")
                    self.workerErr.emit("Connection refused.")
                    
                    return 
                
                except Exception as e:
                    print(f"connection delayed {e}")
                    print("waiting for host...")
                    
                    #self.connled.emit("grey")
                    time.sleep(2)
                if self.isInterruptionRequested():
                    #print("Interruption request handling by Worker (loop2)", self)
                    self.workerErr.emit("Connection aborted by user.")
                    return 
                
            self.commErr.emit(f"socket connected.")
                
            print("connected")
            try:
                print("hostname ", socket.gethostname())
            except Exception as e:
                print(f"error hostname call {e}")
                
            self.connled.emit("green")
            #self.sock.settimeout(None)
            self.sock.settimeout(1.0)
    
            # ready_to_read, ready_to_write, in_error = \
            #                select.select(
            #                   [self.sock],
            #                   [self.sock],
            #                   [self.sock],
            #                   10.0)
            # print(ready_to_read, ready_to_write, in_error)
            
            # Receive data from the server and shut down
            
            total_ns = 0
            while True:
                if self.isInterruptionRequested():
                    #print("Interruption request handling by Worker (loop3)")
                    self.workerErr.emit("Connection aborted by user.")
                    return
                framesz = 0
                received = None
                try:
                    received = self.sock.recv(1)
                    total_ns = 0
                # except socket.error as e:
                #     print(f"socket read error 1: {e}")
                #     break
                except socket.timeout as e:
                    print(f"socket timeout: {e}")
                    #let's check if connection is still there
                    #ask for dip switches b'YDXXX'
                    #self.sock.settimeout(1.0)
                    self.commErr.emit(f"socket timeout: {e}. Retry {total_ns}/4")
                    # ready_to_read, ready_to_write, in_error = \
                    #                select.select(
                    #                   [self.sock],
                    #                   [self.sock],
                    #                   [self.sock],
                    #                   10.0)
                    # print(ready_to_read, ready_to_write, in_error)
            
                    
                    
                    total_ns += 1
                    if total_ns > 4:
                        print(f"broken pipe. Connection lost")
                        break
                except ConnectionResetError:
                    print("socket ConnectionResetError")
                    break
                except Exception as e:
                    print(f"unexpected socket read exception: {e}")
                    break
                
                #print("received", received[0])
                if received is not None:
                    if received == b'A' or received == b'B':
                        framesz = 9
                    elif received == b'C':
                        #3 bytes
                        framesz = 3
                    elif received == b'D':
                        framesz = 4
                    elif received == b'E':
                        framesz = 9
                    elif received == b'G':
                        framesz = 5
                    elif received == b'N':   #4E
                        framesz = 256
                    elif received == b'P':
                        #print("P")
                        framesz = 32 #32
                    elif received == b'Q':
                        framesz = 1024
                    elif received == b'R':
                        framesz = 128
                    elif received == b'S':
                        framesz = 5
                    elif received == b'T':
                        framesz = 5
                    elif received == b'V':   #86 (0x56)
                        framesz = 2
                    elif received == b'Y':   #IO status 7 bytes Oh, Ol, Ih, Il gpioEF, gpioCD, gpioAB
                        framesz = 9
                    elif received == b'Z':
                        framesz = 2 #crc
                    elif received == b'@':
                        framesz = 2 #reset ack frame            
                    elif received == b'x':
                        framesz = 4 #message from the modem one long representing rssi ('x' code 120)
                    
                    else:
                        try:
                            #byteorder is explicitly required because of pyinstaller
                            #otherwise it hangs up
                            print(f"frame error: received={int.from_bytes(received, byteorder='big'):02X}")
                        except Exception as e:
                            print(f"unexpected  exception: {e}")
                            print(f"frame error: received={received}")
                            
                        framesz = 0
        
                          
                    if  framesz > 0:               
                        tsz = framesz
                        msg = b''
                        while tsz > 0:
                            try:
                                msg += self.sock.recv(1)  #(tsz)
                                total_ns2 = 0
                            except ConnectionResetError:
                                print("socket read error 2 ConnectionResetError")
                                # self.sock.close()
                                #
                                # self.connled.emit("grey")
                                # return
                            except Exception as e:
                                print(f"socket read error 2: {e}")
                                #self.commErr.emit(f"socket timeout inside: {e}. Retry {total_ns2}/4")
                                #self.sock.settimeout(1.0)
                                total_ns2 += 1
                                if total_ns2>4:
                                    break
                            lm  = len(msg)
                            #print("lm", framesz, lm, msg)
                            if lm == framesz:
                                #print(f"message ack {received} : {msg[0]} {msg[1]} ")
                                #self.ui.lcdNumber_1.value = 345
                                self.output.emit(bytearray(msg), received[0])
                                break
                            #tsz -= lm
                            tsz -= 1
                        # if received == b'R':
                        #     print(received, msg)
                    else:
                        pass
                        #print(received)
                else:
                    pass
                    #print("received is None")
            # try:
            #     self.sock.shutdown(socket.SHUT_RDWR)
            # except: 
            #     pass
            
            self.sock.close()
            #print("socket closed in loop")
            
            #self.connled.emit("grey")
            self.connled.emit("yellow")
            
            self.commErr.emit(f"connection lost. Broken pipe. Retry...")
            
        #print("Worker: Bye bye les comiques")
        self.sock.close()
        self.connled.emit("grey")


class MSCGui:
    
    def __init__(self):
        self.mainWindow = None

    def runApp(self, argv=['WiFlipApp']):
        """Start WiFlip"""
        print("""Start WiFlip""")
        
            
        
        #HOST = "192.167.1.1"
        #PORT = 23
        
        print(argv)
        app = QtWidgets.QApplication(argv)
        
        # pixmap = QtGui.QPixmap(":/x/images/panthera-bg.png")
        # splash = QtWidgets.QSplashScreen(pixmap)
        # splash.show()
        # app.processEvents()
        # time.sleep(4)
        self.showGui()
        #splash.finish(self.mainWindow)

        app.exec_()

    def showGui(self, parent=None):
        """Show the MSC gui

        In contrast to runApp, this method supposes that the Qt Application object has
        already been created.
        """
        
        self.mainWindow = MainForm( parent=parent )
        self.mainWindow.show()


def fromBcd2Int(barr):
    ret=0
    nbf = 0
    for bi in barr:
        d1=(~bi&0xF0)>>4
        if d1 == 0xF:
            d1 = 0
            nbf += 1
        ret = ret*10+d1
        d2=(~bi&0x0F)
        if d2 == 0xF:
            d2 = 0
            nbf += 1
        ret = ret*10+d2
    if nbf == 2*len(barr):
        ret = -1
    return ret

def swapint(v):
    return ((v&0x0F)<<4)+((v&0xF0)>>4)      

def affcplleds(affls, datanb):
    if not datanb&0b0100:
        #le display du 1M   
        affls[2].display(1.0)
        affls[2].setDecMode()
    else:
        affls[2].display(0.0)
        affls[2].setDecMode()
        
    if datanb&0b0001:
        #le display du 1M   
        affls[0].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
    else:
        affls[0].setPixmap(QtGui.QPixmap(":/x/ledon.png"))
        
    if datanb&0b0010:
        #le display du 1M   
        affls[1].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
    else:
        affls[1].setPixmap(QtGui.QPixmap(":/x/ledon.png"))
        
        
def afflcdi(afftab, data):
    #print(type(data))     => bytearray
    #print(type(data[0]))  => int
    
    for idx in range(len(afftab)):
        afftab[idx].setHexMode()
        if not idx%2:
            #pair
            dx = (~data[idx//2]&0xF0)>>4
        else:
            #impair
            dx = (~data[idx//2]&0x0F)
            
        if dx == 0xF:
            afftab[idx].setDigitCount(0)
        else:
            afftab[idx].setDigitCount(1)
            afftab[idx].display(dx)
            

    
    
    
#
# print("__name__:", __name__)            
# if __name__ == '__main__':
#     MSCGui().runApp(argv=sys.argv)
#


