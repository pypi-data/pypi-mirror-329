# -*- coding: utf-8 -*-
'''
Created on 29 jan 2025


Lucida Grande L/71 L/51
code rst 
print(f"val
message request is b'YQZ setValue
'''

from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QDialogButtonBox, QMessageBox, QCheckBox, QPushButton

from .clklabel import ClkLabel

from .supervis  import Ui_SupervisDialog 
from PyQt5.Qt import QPixmap



class MySuperv(QtWidgets.QDialog): 
    """
    This dialog box was created with QT
    in supervis.ui
    """
    def __init__(self, parent=None):
        super(MySuperv, self).__init__(parent)
        #QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_SupervisDialog()
        self.ui.setupUi(self)
        
        self.create_gbs()

        self.ui.superButton.clicked.connect(partial(self.superReq,  0))
        self.ui.leaveButton.clicked.connect(partial(self.superLeav, 0))
        
        self.ui.panicButton.clicked.connect(self.resetthepin_with_ack)
        
        self.applyAllBbox = self.ui.buttonBox.addButton("Apply all", QDialogButtonBox.ActionRole)
        self.resetAllBbox = self.ui.buttonBox.addButton("Reset", QDialogButtonBox.ResetRole)
        self.recallAllBbox = self.ui.buttonBox.addButton("Recall", QDialogButtonBox.ResetRole)
        self.applyAllBbox.setDefault(True)
        ap = self.ui.buttonBox.button(QDialogButtonBox.Apply)
        ap.setText("Save")    
        self.ui.buttonBox.clicked.connect(self.bboxClicked)
        self.ui.buttonBox.accepted.connect(self.bboxAccepted)
        self.ui.buttonBox.rejected.connect(self.bboxRejected)

        self.ui.labelStatus.setToolTip("Board status:<br>Black: normal mode<br>Red: Supervision mode")
        #self.parent().resetAckSig.connect(self.catchResetSig)
        self.styliseButtons()
        
        #provisory
        self.cntreq  = 0
        self.cntleav = 0
        
        #check state
        self.parent().resetAckSig.connect(self.catchrstSig)
        self.parent().resetButSig.connect(self.catchrstButSig)
        try:
            self.parent().thread.commErr.connect(self.catchcommErrSig)
        except:
            pass
        try:
            self.parent().thread.sock.send(b'YC123')
        except:
            pass


    def closeEvent(self, event):
        self.parent().resetAckSig.disconnect(self.catchrstSig)
        self.parent().resetButSig.disconnect(self.catchrstButSig)
        try:
            self.parent().thread.commErr.disconnect(self.catchcommErrSig)
        except:
            pass
        QtWidgets.QDialog.closeEvent(self, event)
        
    def catchrstButSig(self, code): 
        #print("catchrstButSig code", code) 
        self.ui.labelStatus.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))  
        for name in ["B2","B3-AB","B3-CD","B3-EF"]: 
            for (x,y,z) in self.gb[name]:
                if y!=0:
                    x.setPixmap(QtGui.QPixmap(":/x/ledyellow"))
                    
    def catchcommErrSig(self, msg):  
        #print("catchcommErrSig msg", msg) 
        self.catchrstButSig(-1)
        try:
            self.parent().thread.sock.send(b'YC123')
        except:
            pass
        
                    
    def catchrstSig(self, code):
        #print("code rst", code)
        if code == 132 or code == 200:
            self.ui.labelStatus.setPixmap(QtGui.QPixmap(":/x/ledon.png"))   
        else:
            self.ui.labelStatus.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))  
            for name in ["B2","B3-AB","B3-CD","B3-EF"]: 
                for (x,y,z) in self.gb[name]:
                    if y!=0:
                        x.setPixmap(QtGui.QPixmap(":/x/ledyellow"))
                 
    def create_gbs(self):
        name = "Display A"
        settingsinit = self.parent().settings.value('super'+name, 16*[15])
        initval = (settingsinit, 16*[""])
        gba = self.create_dsplys(name, initval)
        
        name = "Display B"
        settingsinit = self.parent().settings.value('super'+name, 16*[15])
        initval = (settingsinit, 16*[""])
        gbb = self.create_dsplys(name, initval)
        
        name = "B2"
        settingsinit = self.parent().settings.value('super'+name, 16*[0])
        initval = (settingsinit, self.parent().b2tooltip)
        gbb2 = self.create_ios(name, initval)
        
        name = "B3-AB"
        settingsinit = self.parent().settings.value('super'+name, 8*[0])
        initval = (settingsinit, self.parent().gpiotooltip[:8])
        gbb3ab = self.create_ios(name, initval)

        name = "B3-CD"
        settingsinit = self.parent().settings.value('super'+name, 8*[0])
        initval = (settingsinit, self.parent().gpiotooltip[8:16])
        gbb3cd = self.create_ios(name, initval)

        name = "B3-EF"
        settingsinit = self.parent().settings.value('super'+name, 8*[0])
        initval = (settingsinit, self.parent().gpiotooltip[16:])
        gbb3ef = self.create_ios(name, initval)
        
        self.gb = {"Display B": gbb, 
                   "Display A": gba,
                   "B2"       : gbb2,
                   "B3-AB"    : gbb3ab,
                   "B3-CD"    : gbb3cd,
                   "B3-EF"    : gbb3ef,
                   }



    def create_ios(self, name, tinitval):
        iosobj = list()
        initval, inittxt = tinitval
        _translate = QtCore.QCoreApplication.translate
        groupBox = QtWidgets.QGroupBox(self)
        groupBox.setTitle(_translate("SupervisDialog", name))
        groupBox.setObjectName("groupBox"+name)
        groupBox.setMinimumSize(0, 160)
        verticalLayout_17 = QtWidgets.QVBoxLayout(groupBox)
        verticalLayout_17.setObjectName("verticalLayout_17")
        horizontalLayout_2 = QtWidgets.QHBoxLayout()
        horizontalLayout_2.setObjectName("horizontalLayout_2")

        DsplAApplyButton = QtWidgets.QPushButton(groupBox)
        DsplAApplyButton.setObjectName("DsplAApplyButton"+name)
        DsplAApplyButton.setText(_translate("SupervisDialog", "Apply "+name))
        DsplAApplyButton.clicked.connect(partial(self.setIOs, name))
        
        idx = 0
        for val in initval:
            val = int(val)
            verticalLayout_6 = QtWidgets.QVBoxLayout()
            verticalLayout_6.setObjectName("verticalLayout_6"+name+str(idx))
            #label_IODIR = QtWidgets.QLabel(groupBox)
            label_IODIR = ClkLabel()
            label_IODIR.setText("")
            if val == 0:
                label_IODIR.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
            else:
                #label_IODIR.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                label_IODIR.setPixmap(QtGui.QPixmap(":/x/ledyellow"))
                
            label_IODIR.setScaledContents(True)
            label_IODIR.setAlignment(QtCore.Qt.AlignCenter)
            label_IODIR.setMaximumSize(QtCore.QSize(20, 20))
            label_IODIR.simpleClicked.connect(partial(self.ioClicked, name, idx))
            iosobj.append((label_IODIR, val, inittxt[idx]))
            verticalLayout_6.addWidget(label_IODIR, alignment=Qt.AlignCenter)
            label = QtWidgets.QLabel(groupBox)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setText(_translate("SupervisDialog", inittxt[idx]))
            verticalLayout_6.addWidget(label)
            horizontalLayout_2.addLayout(verticalLayout_6)
            idx += 1
            
        verticalLayout_17.addLayout(horizontalLayout_2)

        verticalLayout_17.addWidget(DsplAApplyButton)
        #self.ui.verticalLayout.insertWidget(1, groupBox)
        self.ui.verticalLayout_2.addWidget(groupBox)
        
        return iosobj
            
       
    
    def create_dsplys(self, name, tinitval):
        initval, inittxt = tinitval
        dspobj = list()
        _translate = QtCore.QCoreApplication.translate
        groupBox = QtWidgets.QGroupBox(self)
        groupBox.setTitle(_translate("SupervisDialog", name))

        groupBox.setObjectName("groupBox"+name)
        #groupBox.setMinimumSize(0, 120)
        
        verticalLayout_14 = QtWidgets.QVBoxLayout(groupBox)
        verticalLayout_14.setObjectName("verticalLayout_14"+name)
        horizontalLayout_A = QtWidgets.QHBoxLayout()
        horizontalLayout_A.setObjectName("horizontalLayout_A"+name)

        DsplAApplyButton = QtWidgets.QPushButton(groupBox)
        DsplAApplyButton.setObjectName("DsplAApplyButton"+name)
        DsplAApplyButton.setText(_translate("SupervisDialog", "Apply "+name))
        DsplAApplyButton.clicked.connect(partial(self.setDspls, name))
        
        idx = 0
        for val in initval:
            val=int(val)
            verticalLayout_A0 = QtWidgets.QVBoxLayout()
            #verticalLayout_A0.setObjectName("verticalLayout_A0"+name+str(idx))
            # lcda0 = QtWidgets.QLCDNumber(groupBox)
            # lcda0.setMinimumSize(QtCore.QSize(0, 0))
            # lcda0.setSmallDecimalPoint(False)
            # lcda0.setDigitCount(1)
            # lcda0.setMode(QtWidgets.QLCDNumber.Hex)
            # #lcda0.setObjectName("lcda0"+name)
            # verticalLayout_A0.addWidget(lcda0)
            #

            lqla0 = QtWidgets.QLineEdit(groupBox)
            lqla0.setAlignment(QtCore.Qt.AlignCenter)
            lqla0.setMinimumSize(QtCore.QSize(30, 30))

            font = QtGui.QFont("Courier New", 14, QtGui.QFont.Bold)
            lqla0.setFont(font)

            try:
                lqla0.setText(f"{val:01X}")
            except:
                lqla0.setText(f"{0:01X}")
                
            lqla0.textChanged.connect(partial(self.dspChanged, name, idx))
            lqla0.editingFinished.connect(partial(self.dspEdFinished, name, idx))
            lqla0.returnPressed.connect(partial(self.dspRetPressed, name, idx))
            lqla0.inputRejected.connect(partial(self.dspInpRejected, name, idx))
            lqla0.setInputMask("H;")
            #lbla0.setObjectName("lbla0"+name)
            dspobj.append((lqla0, val, "D"+str(idx)))
            verticalLayout_A0.addWidget(lqla0)
            
            lbla0 = QtWidgets.QLabel(groupBox)
            lbla0.setAlignment(QtCore.Qt.AlignCenter)
            lbla0.setText(_translate("SupervisDialog", "D"+str(idx)))
            idx+=1
            #lbla0.setObjectName("lbla0"+name)
            verticalLayout_A0.addWidget(lbla0)
            horizontalLayout_A.addLayout(verticalLayout_A0)
            
        verticalLayout_14.addLayout(horizontalLayout_A)

        verticalLayout_14.addWidget(DsplAApplyButton)
        #self.ui.verticalLayout.insertWidget(1, groupBox)
        self.ui.verticalLayout_2.addWidget(groupBox)
        
        return dspobj

    def setIODsp(self, name):
        if name in ["Display A","Display B"]:
            self.setDspls(name)
        else:
            self.setIOs(name)
            
            
    def setIOs(self, name): 
        papa = self.parent()
        try:
            c1 = papa.mycmds[name]
        except:
            c1 = 0

        for (x,y,z) in self.gb[name]:
            if int(y)!=0:
                if z.startswith("C/#"):
                    x.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                else:
                    x.setPixmap(QtGui.QPixmap(":/x/ledgreen"))
            
        vals = [int(x[1]) for x in self.gb[name]]

        cx = 0
        pw = 0
        for b in vals:
            cx += (b<<pw)
            pw += 1
        c1byte = c1.to_bytes(1, byteorder='big') 
        cxbyte = cx.to_bytes(2, byteorder='little')  
        #print("cx", f"{cx:016b}", cxbyte)    
        print("message request is", b'YQ'+c1byte+cxbyte)
        try:
            self.parent().thread.sock.send(b'YQ'+c1byte+cxbyte)
        except:
            pass

    def setDspls(self, name):
        papa = self.parent()
        try:
            c1 = papa.mycmds[name]
        except:
            c1 = 0
        
        ledit = self.gb[name]
        digit_idx = 0
        for val in ledit:
            ivalue = int(val[1])
            c3 = 0
            c2 = (ivalue&0x0F) + ((digit_idx<<4)&0xF0)
            self.superCmd(c1, c2, c3)
            digit_idx += 1
    
    def superCmd(self, c1, c2, c3):        
        c1byte = c1.to_bytes(1, byteorder='big')   
        c2byte = c2.to_bytes(1, byteorder='big')   
        c3byte = c3.to_bytes(1, byteorder='big')   
        print("message request is", b'YQ'+c1byte+c2byte+c3byte)

        try:
            self.parent().thread.sock.send(b'YQ'+c1byte+c2byte+c3byte)
        except:
            pass
        
        
    def superLeav(self, cnt):
        if cnt == 0:
            self.cntleav = 0
        elif cnt >= 2:
            dlg = QMessageBox(self.parent())
            dlg.setWindowTitle("Error")
            dlg.setText("Communication error. Please, switch device off/on, restart the programm and try again.")
            dlg.setIcon(QMessageBox.Critical)
            button = dlg.exec()
            return

        self.parent().resetAckSig.connect(self.catchsuperLeavSig)
        print("message request is", b'YCXQ0')
        try:
            self.parent().thread.sock.send(b'YCXQ0')
        except:
            pass

        self.timertout2 = QTimer(singleShot=True, timeout=self.timeoutt)
        self.timertout2.start(5000)

    def superReq(self, cnt):
        if cnt == 0:
            self.cntreq = 0
        elif cnt >= 5:
            dlg = QMessageBox(self.parent())
            dlg.setWindowTitle("Error")
            dlg.setText("Communication error. Please, switch device off/on, restart the programm and try again.")
            dlg.setIcon(QMessageBox.Critical)
            button = dlg.exec()
            return
        self.parent().resetAckSig.connect(self.catchsuperReqSig)
        print("message request is", b'YCXQ0')
        try:
            self.parent().thread.sock.send(b'YCXQ0')
        except:
            pass

        self.timertout2 = QTimer(singleShot=True, timeout=self.timeoutt)
        self.timertout2.start(5000)

    def resetthepin_with_ack(self):
        self.parent().resetthepin_with_ack()

    def timeoutt(self):
        try:
            self.parent().resetAckSig.disconnect(self.catchsuperLeavSig)
        except:
            pass
        try:
            self.parent().resetAckSig.disconnect(self.catchsuperReqSig)
        except:
            pass

        dlg = QMessageBox(self.parent())
        dlg.setWindowTitle("Network")
        dlg.setText("Time out. Device not responding")
        dlg.setIcon(QMessageBox.Warning)
        button = dlg.exec()


    def catchsuperReqSig(self, code):   
        '''
        reset ack was received, we can continue
        '''
        self.parent().resetAckSig.disconnect(self.catchsuperReqSig)
        #print(f"catchsuperReqSig supervisor, {code:02X}")
        #papa.resetAckSig.disconnect(self.catchResetSig)
        try:
            self.timertout2.stop()    
        except():
            pass

        if code != 0x84:
            self.cntreq += 1
            self.superReq(self.cntreq)

    def catchsuperLeavSig(self, code):   
        '''
        reset ack was received, we can continue
        '''
        self.parent().resetAckSig.disconnect(self.catchsuperLeavSig)
        #print("catchsuperLeavSig supervisor", code)
        #papa.resetAckSig.disconnect(self.catchResetSig)
        try:
            self.timertout2.stop()    
        except():
            pass

        if code == 0x84:
            self.cntleav += 1
            self.superLeav(self.cntleav)


    def ioClicked(self, name, idx ):
        #print(self, name, idx, self.gb[name][idx])
        if self.gb[name][idx][1] == 0:
            dontdothat = False
            if self.gb[name][idx][2].startswith("C/#"):
                if self.parent().settings.value('superWarningTick', "True") == "True":
                    cb  = QCheckBox("Show no more these alerts")
                    dlg = QMessageBox(self.parent())
                    dlg.setCheckBox(cb)
                    dlg.addButton(QPushButton("Yes, burn it all down! "), QMessageBox.AcceptRole)
                    cancelButton = QPushButton("Cancel")
                    dlg.addButton(cancelButton, QMessageBox.RejectRole)
                    dlg.setDefaultButton(cancelButton)
                    dlg.setWindowTitle("Attention")
                    dlg.setText(f"You are going to activate coil {self.gb[name][idx][2]} permanently.\nAre you sure you want to do this?")
                    dlg.setIcon(QMessageBox.Warning)
                    button = dlg.exec()
                    
                    if cb.checkState() == Qt.Checked:
                        self.parent().settings.setValue('superWarningTick', "False")   
                        self.parent().settings.sync()

                    if button == 0:
                        pass
                    else:
                        dontdothat = True
            if not dontdothat:         
                self.gb[name][idx][0].setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                self.gb[name][idx] = (self.gb[name][idx][0], 1, self.gb[name][idx][2])
        else:
            self.gb[name][idx][0].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
            self.gb[name][idx] = (self.gb[name][idx][0], 0, self.gb[name][idx][2])

        self.setIODsp(name)
            
    def dspChanged(self, name, idx):
        #print("dspChanged", name, idx)
        if not self.gb[name][idx][0].text():
            val = 0xF
        else:
            try:
                val = (int(self.gb[name][idx][0].text(), 16)&0x0F)
            except:
                val = 0
                
                
        if not self.gb[name][idx][0].text():
            pass
        else:
            self.gb[name][idx][0].setText(f"{val:01X}")
        self.gb[name][idx] = (self.gb[name][idx][0], val, self.gb[name][idx][2])
        
        
    def bboxClicked(self, button):
        #print("clickd", button, QDialogButtonBox.SaveAll, self.ui.buttonBox.buttonRole(button))
        #print("clickd", button.text())
        
        #if button.text() == "Save All":
        #Apply is button for saving setups
        if button == self.ui.buttonBox.button(QDialogButtonBox.Apply):
            for name,gbx in self.gb.items():
                #print("sav settings", 'super'+name, [x[1] for x in gbx])
                self.parent().settings.setValue('super'+name, [x[1] if not x[2].startswith("C/#") else 0 for x in gbx])
                warn = True in (x[2].startswith("C/#") and x[1]!=0 for x in gbx)
                if warn:
                    self.optionWarning("Refuse to save coil in state active. The rest will be saved normally.", "OK", None)
            self.parent().settings.sync()
        elif button == self.resetAllBbox:
            for name,gbx in self.gb.items():
                #print("reset settings", 'super'+name, [x[1] for x in gbx])
                if name in ["Display A","Display B"]:                    
                    self.gb[name] = [(x,0XF,z) for (x,_,z) in gbx]
                    for x,y,_ in self.gb[name]:
                        x.setText(f"{y:01X}")
                else:
                    self.gb[name] = [(x,0X0,z) for (x,_,z) in gbx]
                    for x,_,_ in self.gb[name]:
                        x.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                self.setIODsp(name)

        elif button == self.recallAllBbox:
            for name in self.gb.keys():
                settingsinit = self.parent().settings.value('super'+name, None)
                if settingsinit is not None:
                    a = [x[0] for x in self.gb[name]]
                    c = [x[2] for x in self.gb[name]]
                    self.gb[name] = list(zip(a,settingsinit,c))
                    if name in ["Display A","Display B"]:                    
                        for x,y,_ in self.gb[name]:
                            iy = int(y)
                            x.setText(f"{iy:01X}")
                    else:
                        for x,y,_ in self.gb[name]:
                            if int(y) != 0:
                                x.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                            else:
                                x.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                    self.setIODsp(name)
            
        elif button == self.applyAllBbox:
            for name in self.gb.keys():
                self.setIODsp(name)
        elif button == self.ui.buttonBox.button(QDialogButtonBox.RestoreDefaults):
            for name,gbx in self.gb.items():
                #print("reset settings", 'super'+name, [x[1] for x in gbx])
                if name in ["Display A","Display B"]:                    
                    self.gb[name] = [(x,0XF,z) for (x,_,z) in gbx]
                    for x,y,_ in self.gb[name]:
                        x.setText(f"{y:01X}")
                else:
                    self.gb[name] = [(x,0X0,z) for (x,_,z) in gbx]
                    for x,_,_ in self.gb[name]:
                        x.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                    
                self.parent().settings.setValue('super'+name, [int(x[1]) for x in self.gb[name]])
            self.parent().settings.sync()
            
    def bboxAccepted(self):        
        #print("accepted")
        self.parent().resetAckSig.disconnect(self.catchrstSig)
        self.parent().resetButSig.disconnect(self.catchrstButSig)
        try:
            self.parent().thread.commErr.disconnect(self.catchcommErrSig)
        except:
            pass
    def bboxRejected(self):
        #print("rejected")
        self.parent().resetAckSig.disconnect(self.catchrstSig)
        self.parent().resetButSig.disconnect(self.catchrstButSig)
        try:
            self.parent().thread.commErr.disconnect(self.catchcommErrSig)
        except:
            pass
        
    def dspEdFinished(self, name, idx):
        #print("dspEdFinished", name, idx)
        if not self.gb[name][idx][0].text():
            try:
                val = self.gb[name][idx][1]
            except:
                val = 0
            self.gb[name][idx][0].setText(f"{val:01X}")
        else:
            self.setIODsp(name)
            
    def dspRetPressed(self, name, idx):
        #print("dspRetPressed", name, idx)
        pass    
    
    def dspInpRejected(self, name, idx):
        print("dspInpRejected", name, idx, self.gb[name][idx][0].text(), "fin")
        try:
            val = self.gb[name][idx][1]
        except:
            val = 0
        self.gb[name][idx][0].setText(f"{val:01X}")
    
    def myValidator(self):
        #print("myValidator")
        pass

    def optionWarning(self, msgTxt, yesTxt, noTxt=None):
        if self.parent().settings.value('superWarningTick', "True") == "True":
            cb  = QCheckBox("Show no more these alerts")
            dlg = QMessageBox(self.parent())
            dlg.setCheckBox(cb)
            dlg.addButton(QPushButton(yesTxt), QMessageBox.AcceptRole)

            if noTxt is not None:
                cancelButton = QPushButton(noTxt)
                dlg.addButton(cancelButton, QMessageBox.RejectRole)
                dlg.setDefaultButton(cancelButton)
            dlg.setWindowTitle("Attention")
            dlg.setText(msgTxt)
            dlg.setIcon(QMessageBox.Warning)
            button = dlg.exec()
            
            if cb.checkState() == Qt.Checked:
                self.parent().settings.setValue('superWarningTick', "False")   
                self.parent().settings.sync()
            return button
        return None
    
    
    def styliseButtons(self):
        self.ui.superButton.setStyleSheet(
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
        
        self.ui.panicButton.setStyleSheet(
            '''
QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 rgb(21, 169, 103), stop: 0.4 rgb( 102, 221, 170),
                                            stop: 0.5 rgb( 75, 210, 132), stop: 1.0 rgb(21, 169, 103));
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
                                            stop: 0 rgb(5, 100, 88), stop: 0.4 rgb( 40, 131, 90),
                                            stop: 0.5 rgb( 75, 240, 162), stop: 1.0 rgb(0, 90, 80));
    border-style: inset;

}            

QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 rgb(42, 255, 200), stop: 0.4 rgb( 152, 255, 225),
                                            stop: 0.5 rgb( 180, 255, 254), stop: 1.0 rgb(42, 255, 200));
    border-style: inset;

}            
    '''       
            )    
        
        self.ui.leaveButton.setStyleSheet(
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