#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
options.py

Created on 7 sept. 2011

@author: garzol
Copyright AA55 Consulting 2011

adaptation from options of msc project www
Please reset
'''
import time

from time import sleep

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt, QVariant

from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QTimer
from .gameset  import Ui_GameSettings
#from mytreewidget import MyTreeWidget
#from PyQt5.Qt import *

from .mytreeview import MyTreeView, MyDelegate


class Combo:
    def __init__(self, value, vtl, bitMask, addr):
        self.value = value  #it's an str
        self.vtl   = vtl  #list of 2-tuple (value, "text in combo")
        self.addr  = addr
        self.items       = [itm[1] for itm in vtl]
        self.targetValue = [itm[0] for itm in vtl]
        self.bitMask     = bitMask

    @staticmethod 
    def updateMapFromCombo(bytes, cx):
        nibbles = list(Hex.b2n(bytes))

        index         = cx.items.index(cx.value)
        addr          = cx.addr
        item          = cx.items[index]
        targetValue   = cx.targetValue[index]
        bitMask       = cx.bitMask
        
        #print("nibble avant", nibbles[addr], index, addr, item, targetValue, bitMask)
        nibbles[addr] = (nibbles[addr] & (~bitMask)) | targetValue
        #print("nibble apres", nibbles[addr])
        
        rbytes = [(x<<4)+y for x,y in zip([x for x in nibbles[1::2]], [x for x in nibbles[::2]])]
        return rbytes        
        
    @staticmethod
    def ComboFromMap(bytes, cexemple):  
        '''
        bytes is a list of bytes
        nibbles is a list of nibbles (type bytes < 16), hexemple is a model to base the build on
        return a combo corresponding to spec 
        '''
        nibbles = list(Hex.b2n(bytes))
        
        addr         = cexemple.addr
        vtl          = cexemple.vtl
        bitMask      = cexemple.bitMask
            
        targetValue = nibbles[addr] & bitMask
        try:
            index       = cexemple.targetValue.index(targetValue)
            value       = cexemple.items[index]
        except:
            index       = -1
            value       = f"Unknown target value: {targetValue:04b}"
        
        #print("==================ComboFromMap:", nibbles[addr], value, index, targetValue, bitMask, addr)
        ret = Combo(value, vtl, bitMask, addr)
        return(ret)        


class Hex:
    '''
    This type for
    management of obj from the memroy map
    This is a collection of nibbles
    '''
    def __init__(self, value, addr, typ="hex", dir=1, length=None):
        self.type = typ.lower()   #hex or bcd
        self.addr = addr
        self.dir  = dir
        if type(value) == int:
            value = f"{value:X}"
        elif type(value) != str:
           #print("Hex class: Value cannot be of type", type(value))
           value=""
           
        if length is not None:
           if len(value) < length:
               value = '0'*(length-len(value)) + value
            
        self.value = value
        
        #print("New Hex: ", value, self.value, length)
        
    @staticmethod
    def b2n(bb):
        '''
        create a nibble list from a byte list
        '''
        for b in bb:
            for val in (b & 0xF, b >> 4):  #first lsn, second msn
                yield val
                

    @staticmethod 
    def updateMapFromHex(bytes, hx):
        nibbles = list(Hex.b2n(bytes))

        value  = hx.value
        addr   = hx.addr
        type   = hx.type
        dir    = hx.dir
        if dir != 1:
            value = value[::-1]  #let's reverse
            
        #print("updating map from hex:", value)
        for c in value:
            nibbles[addr] = int(c, 16)&0x0F
            addr += 1
        
        rbytes = [(x<<4)+y for x,y in zip([x for x in nibbles[1::2]], [x for x in nibbles[::2]])]

        return rbytes        
        
    @staticmethod
    def hexFromMap(bytes, hexemple):  
        '''
        bytes is a list of bytes
        nibbles is a list of nibbles (type bytes < 16), hexemple is a model to base the build on
        return an Hex corresponding to spec 
        hex.addr  <= hexemple.addr
        hex.type  <= hexemple.type
        hex.dir   <= hexemple.dir
        hex.value <= "X0X1X2...Xn" where Xi=nibbles[addr++] if dir==1 else Xn-1-i=nibbles[addr++]
        '''
        nibbles = list(Hex.b2n(bytes))
            

        addr   = hexemple.addr
        type   = hexemple.type
        dir    = hexemple.dir
        
        value  = ""    
        for ii in range(len(hexemple.value)):
            if nibbles[addr+ii]>9 and type=="bcd":
                type="hex"
            c = f"{nibbles[addr+ii]:1X}"
            value+=c
        if dir != 1:
            value = value[::-1]  #let's reverse
        ret = Hex(value, addr, type, dir)   
        return(ret)

class MyOptionsUtils:
    @staticmethod
    def myValidateCombo(val, minval, maxval, option):
        #print("in myvalidatecombo line 171", val, minval, maxval, option)
        try:
            index         = option.items.index(val)
        except:
            print("    combo has an invalid value")
            return False, f"Unknown value: {val} in combo box"
        
        return True, f"No Problemo"
    
    @staticmethod
    def myValidateHex(val, minval, maxval, option):
        '''Doc for this static method'''
        hexval = option
        if type(val) != str:
            return False, f"Error: Internal type error in myValidateHex, please report" 
        
        if len(val) > len(hexval.value):
            return False, f"Too long. At most {len(hexval.value)} characters permitted here" 
        
        for c in val:
            try:
                v = int(c, 16)
                if v>15 and hexval.type == 'hex':
                    return False, f"Hexadecimal string: Only chars 0,1,2,3,..9,A,B,..E,F are allowed" 
                if v>9  and hexval.type != 'hex':
                    return False, f"BCD string: Only chars 0,1,2,3,..9 are allowed" 
            except:
                return False, f"Forbidden character"
        return True, "ok"
    
    @staticmethod
    def myValidateInt(val, minval, maxval, option=None):
        '''Doc for this static method'''
        #print("myValidateInt", val, type(val))
        try:
            valInt = int(val)
        except:
            return False 
        
        if valInt<maxval and valInt>minval:
            return True
        return False

    @staticmethod
    def myValidateBool(val, minval, maxval, option=None):
        '''Doc for this static method minval and maxval are dummy'''
        return  str(val).lower() in ("yes", "true", "t", "1")+("no", "false", "f", "0") 

    @staticmethod
    def myInitBoxToolBox(win):

        pipo=QtCore.Qt.WindowFlags(QtCore.Qt.Tool)
        win.setWindowFlags(pipo)
        
        win.setWindowFlags(win.windowFlags().__or__(QtCore.Qt.WindowFlags(QtCore.Qt.CustomizeWindowHint)))
        win.setWindowFlags(win.windowFlags().__iand__(QtCore.Qt.WindowFlags(QtCore.Qt.WindowMinMaxButtonsHint).__invert__()))
        win.setWindowModality(QtCore.Qt.ApplicationModal)
        win.activateWindow()
        

#Here is the options dialog box
class MyOptions(QtWidgets.QDialog):
    """
    This dialog box was created with QT
    adding a settings is very simple
    create a default value, namely "defaultSomething"
    then add an aentry in the dictionary defaults
    such as 
                u"Options/Something":[defaultSomething, 
                                          int, 
                                          MyOptionsUtils.myValidateInt, 10, 200,
                                          "Comment that one can read in the infobubble when hovering the item (10<x<199)"],
    One can only have int, bool types. For str, I don't remember, it does not look like to work at the moment
    """
    #statusCmd = pyqtSignal(int, str)  #obsolete

    PROPERTY, VALUE = range(2)

    defaultStyleName = "Plain UML"
    
    default1stFreeplay         = 54
    default2ndFreeplay         = 71
    defaultExtraBall           = 33
    defaultAdjPlay             = 0x2B
    defaultPrinterSerialNum    = 1
    defaultCreditLimit         = 1
    defaultCredit              = 0
    defaultExtraBall           = 0
    defaultFreeplay            = 0
    default3rdCoinRejector     = 3
    default2ndCoinRejector     = "1 play per coin"
    default1stCoinRejector     = "1 play per coin"
    default1stCoinRejNbCoin    = "1 coin"
    default2ndCoinRejNbCoin    = "1 coin"
    defaultBallPerPlay         = "3 balls per play"
    defaultPrice               = "Normal Price"
    defaultModeEB              = "Extra Ball not Repetitive"
    defaultModeFP              = "Free Play not Repetitive"
    
    defaultGrObjSpacing = 8
    defaultGrObjDeltaCol = 8
    defaultGrObjDeltaLin = 8 
    defaultGrObjArrowSize = 4
    defaultGrObjspaceNote = 10
    defaultGrObjArrowHeight = 5 
    defaultGrObjArrowLength = 15 
    defaultGrObjProcessSize = 8
    defaultGrObjRequirementSize = 24
    defaultModelNum=0
    defaultVerboseScript="True"
    defaultAutoUnmarkOnSave="True"
    defaultProdNum=0x1053
    defaultSymbNameAutoLen=5
    defaultArkiCreateProcLink="True"
    defaultArkiInheritGraphProp="True"
    defaultCompactActorName="True"
    defaultGrObjOIBoxSize = 16
    defaultGrObjMaxChars = 40
    
    
    BasicsStr        = "Basics"
    ScoreTStr        = "Score Threshold"
    InitCoStr        = "Initial Contents"
    GameVaStr        = "Game Variant"
    HandiTStr        = "Handicaps"
    CoinSlStr        = "Coin logic"
    ModePlStr        = "Mode of Play"
    
    topLevelCategory = [BasicsStr, ScoreTStr, InitCoStr, GameVaStr, HandiTStr, CoinSlStr, ModePlStr]
    
    default_tlcid = 0
    parent__tlcid = 6
    
    defaults = {
#                u"Options/styleName":[defaultStyleName, 
#                                      str, 
#                                      None, 0, 0, 
#                                      "Main style's name"],
                u"Production N°":[defaultProdNum, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 10000, 
                                         "Production number on 4 hex digits",
                                         BasicsStr,
                                         Hex("00000", 0x2B, "hex", -1)],
                u"Model N°":[defaultModelNum, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 10000, 
                                         "Model number on 4 hex digits",
                                         BasicsStr,
                                         Hex("0000", 0x24, "hex", -1)],
                u"Serial N° of Printer":[defaultPrinterSerialNum, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 10000, 
                                         "Serial Number of last miniprinter used",
                                         BasicsStr,
                                         Hex("00000", 0x1B, "hex", -1)],
                u"Credit Limit":[defaultCreditLimit, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 9, 
                                         "Maximum credit: 0 for max. 9, 1 for max 19, etc...",
                                         BasicsStr,
                                         Hex("0", 0x20, "bcd", 1)],
                u"Extra Ball":[defaultExtraBall, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 99, 
                                         "Extra ball: 44 means 44K. 0 means no E. Ball given",
                                         ScoreTStr,
                                         Hex("00", 0x80, "bcd", 1)],
                                         
                u"2nd Freeplay":[default2ndFreeplay, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 99, 
                                         "2nd Freeplay. 82 means 820K. 0 means no 2nd freeplay",
                                         ScoreTStr,
                                         Hex("00", 0x70, "bcd", 1)],
                u"1st Freeplay":[default1stFreeplay, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 99, 
                                         "1st Freeplay. 65 means 650K. 0 means no freeplay",
                                         ScoreTStr,
                                         Hex("00", 0x60, "bcd", 1)],
                u"#Credit":[defaultCredit, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 99, 
                                         "Number of credits",
                                         InitCoStr,
                                         Hex("00", 0x50, "bcd", 1)],
                u"#Freeplay":[defaultFreeplay, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 9, 
                                         "Number of freeplays",
                                         InitCoStr,
                                         Hex("0", 0x40, "bcd", 1)],
                u"#Extra Ball":[defaultExtraBall, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 9, 
                                         "Number of Extra Balls",
                                         InitCoStr,
                                         Hex("0", 0x41, "bcd", 1)],
                u"Adj. Play":[defaultAdjPlay, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 255, 
                                         "Adj. Play is game dependent. Generally associated with game difficulty and/or Bonus increment",
                                         GameVaStr,
                                         Hex("00", 0x90, "hex", -1)],
                u"#Handicap #4":[defaultExtraBall, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 99999, 
                                         "4th handicap (High score to date: 1M + param x10 (Player #4)",
                                         HandiTStr,
                                         Hex("00000", 0x73, "bcd", -1)],
                u"#Handicap #3":[defaultExtraBall, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 99999, 
                                         "3rd handicap (High score to date: 1M + param x10 (Player #3)",
                                         HandiTStr,
                                         Hex("00000", 0x7B, "bcd", -1)],
                u"#Handicap #2":[defaultExtraBall, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 99999, 
                                         "2nd handicap (High score to date: 1M + param x10 (Player #2)",
                                         HandiTStr,
                                         Hex("00000", 0x6B, "bcd", -1)],
                u"#Handicap #1":[defaultExtraBall, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 99999, 
                                         "1st handicap (High score to date: 1M + param x10 (Player #1)",
                                         HandiTStr,
                                         Hex("00000", 0x63, "bcd", -1, 5)], #adding the length (here: 5) is useless
                                                                            #while "00000" as an example value is used to determine length...
                
                u"3rd Coin rejector":[default3rdCoinRejector, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 9, 
                                         "Number of plays per coin",
                                         CoinSlStr,
                                         Hex("0", 0xB0, "bcd", 1)],
                
                u"3rd Coin rejector":[default3rdCoinRejector, 
                                         Hex, 
                                         MyOptionsUtils.myValidateHex, 0, 9, 
                                         "Number of plays per coin",
                                         CoinSlStr,
                                         Hex("0", 0xB0, "bcd", 1)],
                u"2nd Coin rejector":[default2ndCoinRejector, 
                                         Combo, 
                                         MyOptionsUtils.myValidateCombo, 0, 9, 
                                         "Number of plays per coin (2nd coin)",
                                         CoinSlStr,
                                         Combo("?Unknown", [(0, "1 play per coin"), (1, "2 plays per coin"), (2, "3 plays per coin"), (3, "4 plays per coin")], 3, 0xA1)],
                u"2nd Coin rejector - #coins":[default2ndCoinRejNbCoin, 
                                         Combo, 
                                         MyOptionsUtils.myValidateCombo, 0, 9, 
                                         "Number of coins (1st coin rejector)",
                                         CoinSlStr,
                                         Combo("?Unknown", [(0, "2 coins"), (4, "1 coin")], 4, 0xA1)],
                u"1st Coin rejector":[default1stCoinRejector, 
                                         Combo, 
                                         MyOptionsUtils.myValidateCombo, 0, 9, 
                                         "Number of plays per coin (1st coin)",
                                         CoinSlStr,
                                         Combo("?Unknown", [(0, "1 play per coin"), (1, "2 plays per coin"), (2, "3 plays per coin"), (3, "4 plays per coin")], 3, 0xA0)],
                u"1st Coin rejector - #coins":[default1stCoinRejNbCoin, 
                                         Combo, 
                                         MyOptionsUtils.myValidateCombo, 0, 9, 
                                         "Number of coins (1st coin rejector)",
                                         CoinSlStr,
                                         Combo("?Unknown", [(0, "2 coins"), (4, "1 coin")], 4, 0xA0)],
                u"Price type":[defaultPrice, 
                                         Combo, 
                                         MyOptionsUtils.myValidateCombo, 0, 9, 
                                         '''
Premium price: 1 Extra Play with 2nd payment (min. 1 play)
WITHOUT PRESSING THE START BUTTON
(This state affects all 3 coin rejectors)
                                         ''',
                                         CoinSlStr,
                                         Combo("?Unknown", [(0, "Normal Price"), (4, "Premium Price")], 8, 0xA1)],
                u"Balls per Play":[defaultBallPerPlay, 
                                         Combo, 
                                         MyOptionsUtils.myValidateCombo, 0, 9, 
                                         "Number of balls per play",
                                         ModePlStr,
                                         Combo("?Unknown", [(0, "5 balls per play"), (8, "3 balls per play")], 8, 0xB1)],
                u"Balls per Play":[defaultBallPerPlay, 
                                         Combo, 
                                         MyOptionsUtils.myValidateCombo, 0, 9, 
                                         "Number of balls per play",
                                         ModePlStr,
                                         Combo("?Unknown", [(0, "5 balls per play"), (8, "3 balls per play")], 8, 0xB1)],
                u"E.B. Mode":[defaultModeEB, 
                                         Combo, 
                                         MyOptionsUtils.myValidateCombo, 0, 9, 
                                         "E.B. Mode",
                                         ModePlStr,
                                         Combo("?Unknown", [(0, "Extra Ball not Repetitive"), (1, "Extra Ball Repetitive"), (2, "Extra Ball Accumulative")], 3, 0xB1)],
                u"F.P. Mode":[defaultModeFP, 
                                         Combo, 
                                         MyOptionsUtils.myValidateCombo, 0, 9, 
                                         "E.B. Mode",
                                         ModePlStr,
                                         Combo("?Unknown", [(0, "Free Play not Repetitive"), (4, "Free Play Repetitive")], 4, 0xB1)],
                
                # u"Options/ArkiCreateProcLink":[defaultArkiCreateProcLink, 
                #                          bool, 
                #                          MyOptionsUtils.myValidateBool, 0, 1, 
                #                          "Activate Actor:P1 creates links between inner process (False/True)"],
                # u"Options/ArkiInheritGraphProp":[defaultArkiInheritGraphProp, 
                #                          bool, 
                #                          MyOptionsUtils.myValidateBool, 0, 1, 
                #                          "Objects inherit several graphics properties from Arkitect. MSC stylesheet is supeseded if True (False/True)"],
                # u"Options/VerboseScript":[defaultVerboseScript, 
                #                          bool, 
                #                          MyOptionsUtils.myValidateBool, 0, 1, 
                #                          'Autoscript will display [label="NAME"] for an Actor in a declaration, even though its symbol has the same name (False/True)'],
                # u"Options/AutoUnmarkOnSave":[defaultAutoUnmarkOnSave, 
                #                          bool, 
                #                          MyOptionsUtils.myValidateBool, 0, 1, 
                #                          'Blue background of objects will disappear automatically after save (False/True)'],
                # u"Options/GrObjSpacing":[defaultGrObjSpacing, 
                #                          int, 
                #                          MyOptionsUtils.myValidateInt, 1, 100, 
                #                          "Box margin (1<x<99)"],
                # u"Options/GrObjMaxChars":[defaultGrObjMaxChars, 
                #                           int, 
                #                           MyOptionsUtils.myValidateInt, 10, 200,
                #                           "Max number of chars per line for actors and messages (10<x<199)"],
                # u"Options/GrObjDeltaCol":[defaultGrObjDeltaCol, 
                #                           int, 
                #                           MyOptionsUtils.myValidateInt, 1, 100,
                #                           "Distance between columns (1<x<99)"],
                # u"Options/GrObjDeltaLin":[defaultGrObjDeltaLin, 
                #                           int, 
                #                           MyOptionsUtils.myValidateInt, 1, 100,
                #                           "Distance between lines (1<x<99)"],
                # u"Options/GrObjArrowSize":[defaultGrObjArrowSize, 
                #                            int, 
                #                            MyOptionsUtils.myValidateInt, 1, 100,
                #                            "size of arrow heads (1<x<99)"],
                # u"Options/GrObjArrowHeight":[defaultGrObjArrowHeight, 
                #                              int, 
                #                              MyOptionsUtils.myValidateInt, 1, 100,
                #                              "Height of arrow, for reflexive messages (1<x<99)"],
                # u"Options/GrObjArrowLength":[defaultGrObjArrowHeight, 
                #                              int, 
                #                              MyOptionsUtils.myValidateInt, 1, 100,
                #                              "Length of arrow, for reflexive messages (1<x<99)"],
                # u"Options/GrObjspaceNote":[defaultGrObjspaceNote, 
                #                            int, MyOptionsUtils.myValidateInt, 1, 100,
                #                            "internal spacing for note objects (1<x<99)"],
                # u"Options/GrObjRequirementSize":[defaultGrObjRequirementSize, 
                #                            int, MyOptionsUtils.myValidateInt, 0, 100,
                #                            "requirement's circle diameter (0<x<99)"],
                # u"Options/GrObjProcessSize":[defaultGrObjProcessSize, 
                #                            int, MyOptionsUtils.myValidateInt, 0, 100,
                #                            "process thickness (0<x<99)"],
                # u"Options/SymbNameAutoLen":[defaultSymbNameAutoLen, 
                #                            int, MyOptionsUtils.myValidateInt, 1, 100,
                #                            "length of actor name below which auto renaming will be performed (2<x<99)"],
                # u"Options/GrObjOIBoxSize":[defaultGrObjOIBoxSize, 
                #                            int, 
                #                            MyOptionsUtils.myValidateInt, 1, 100,
                #                            "size of square pads indicating flow from/to outside (1<x<99)"],
                # u"Options/CompactActorName":[defaultCompactActorName, 
                #                          bool, 
                #                          MyOptionsUtils.myValidateBool, 0, 1, 
                #                          "Either draw full names of actors type:name\\type:name, etc... or just name to spare room (False/True)"],
                #


                             }    
    def __init__(self, parent=None):
        super(MyOptions, self).__init__(parent)
        self.ui = Ui_GameSettings()
        self.ui.setupUi(self)
        #self.setFocusPolicy(QtCore.Qt.ClickFocus)
        MyOptionsUtils.myInitBoxToolBox(self)       
        self.refreshdlg()

    def refreshdlg(self):
        #select sys config
        memtyp = 1
        papa = self.parent()
        papa.ui.rb_nvram.setChecked(True)  #we expect the others to turn unchecked...
        self.ui.label.setWordWrap(True)
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
            


        self.timertout = QTimer(singleShot=True, timeout=self.timeoutt)
        self.timertout.start(5000)

        try:
            papa.read128Sig.disconnect(self.cmdDone)
            #self.statusCmd.disconnect(self.cmdDone)
        except:
            pass   
        #self.statusCmd.connect(self.cmdDone)   
        papa.read128Sig.connect(self.cmdDone)
        
        #self.statusCmd.connect(self.cmdDone)   
        #next lines to emulate the thing
        # self.timerpipo = QTimer(singleShot=True, timeout=self.fpipo)
        # self.timerpipo.start(4000)
              
    def timeoutt(self):
        print("Time out")
        dlg = QMessageBox(self.parent())
        dlg.setWindowTitle("Network")
        dlg.setText("Time out. Please, check your connection")
        dlg.setIcon(QMessageBox.Warning)
        button = dlg.exec()

        if button == QMessageBox.Ok:
            self.ui.label.setText("Can't find device")
        
                
    def cmdDone(self, memTypStr):
        print("Game settings cmdDone memTyp", memTypStr)
        if memTypStr != "nvram live":
            return  
        print("nvr read done")
        self.timertout.stop()
        papa = self.parent()

        
        if memTypStr == "nvram live" and papa.ui.rb_nvram.isChecked():
            #self.ui.groupBox.stateChanged.connect(self.test)
            self.ui.label.setText("Current settings:")
            mininvrl = [x[1] for x in papa.nvrlist]
            
            for objname, objcontent in MyOptions.defaults.items():  
                if objcontent[1] == Hex:
                    h = Hex.hexFromMap(mininvrl, objcontent[7])
                    value = h.value
                    #print("objh", objname, value)
                else:
                    c = Combo.ComboFromMap(mininvrl, objcontent[7])
                    #value = self.settin.value(objname, objcontent[0])    #[0] is default value
                    value = c.value
                    #print("obj", objname, value)
                    
                self.itemvdict[objname].setText(value)

    def config(self, settin):
        _translate = QtCore.QCoreApplication.translate
        treeHeaderLabel=["Property", "Value"]
        self.settin = settin
        #self.myTree = MyTreeWidget()   
        #self.myTree = self.ui.treeWidget   
        
        # self.myTree.setColumnCount(len(treeHeaderLabel))
        # self.myTree.setHeaderLabels(treeHeaderLabel)
        # self.myTree.setAlternatingRowColors(True)
        # self.myTree.setColumnWidth(0, 220)
        # self.myTree.setAllColumnsShowFocus(True)
        # self.myTree.setUniformRowHeights(True)
        # self.myTree.setSortingEnabled(True)
        # self.myTree.header().setMinimumSectionSize(180)
        # self.myTree.header().setCascadingSectionResizes(True)
        #
        # self.myTree.setLineWidth(2)
        # self.myTree.setMidLineWidth(1)
        # self.myTree.setTabKeyNavigation(True)
        # self.myTree.setTextElideMode(QtCore.Qt.ElideLeft)
        # self.myTree.setAnimated(True)

        #self.myTree.setObjectName("treeWidget")

        self.myTreev = self.ui.treeView
        self.myTreev.setRootIsDecorated(True)
        self.myTreev.setAlternatingRowColors(True)
        self.myTreev.setAnimated(True)
        self.myTreev.setLineWidth(2)
        self.myTreev.setMidLineWidth(1)
        self.myTreev.setTabKeyNavigation(True)
        self.myTreev.setColumnWidth(0, 220)
        self.myTreev.setAllColumnsShowFocus(True)
        self.myTreev.setUniformRowHeights(True)
        self.myTreev.setSortingEnabled(True)
        self.myTreev.header().setMinimumSectionSize(180)
        self.myTreev.header().setCascadingSectionResizes(True)
        self.myTreev.setEditTriggers(QAbstractItemView.AllEditTriggers);
        model = self.createPropertyModel(self)
        self.myTreev.setModel(model)
        rootNode = model.invisibleRootItem()
        model.itemChanged.connect(self.onItemDataChange)
        self.tvlis = dict()
        self.brushvdict = dict()
        self.itemvdict  = dict()

        for cat in MyOptions.topLevelCategory:
            myItem = QStandardItem(cat)
            myItem.setEditable(False)
            myItem2 = QStandardItem(None)
            myItem2.setEditable(False)
            rootNode.appendRow([myItem, myItem2])
            self.tvlis[cat] = myItem
        for objname, objcontent in MyOptions.defaults.items():  
            fatherItem = self.tvlis[objcontent[MyOptions.parent__tlcid]]
            value = settin.value(objname, objcontent[0])    #[0] is default value
            myItem = QStandardItem(objname)
            myItem.setEditable(False)
            myItem2 = QStandardItem(str(value))
            if MyOptions.defaults[objname][1] == Combo:
                myecombo = MyOptions.defaults[objname][7]
                myItem2.setData(QVariant(myecombo.items),Qt.UserRole)

            myItem.setToolTip(MyOptions.defaults[objname][5])   #[5] is tool tip string        
            fatherItem.appendRow([myItem, myItem2])
            self.brushvdict[objname]   = myItem.background()
            self.itemvdict[objname] = myItem2
            
            #test
            self.onItemDataChange(myItem2)
            
        self.myTreev.expandAll()
        self.myTreev.doubleClicked.connect(self.onVItemClick)
        self.myTreev.clicked.connect(self.onVItemClick)
        delegate = MyDelegate()
        self.myTreev.setItemDelegate(delegate)    
        #self.myTreev.editorClosed.connect(self.onEditorClose)
        # self.tlis = dict()
        # for cat in MyOptions.topLevelCategory:
        #     item_0 = QtWidgets.QTreeWidgetItem(self.myTree)
        #     #item_0.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled |Qt.ItemIsSelectable)
        #     item_0.setText(0, _translate("GameSettings", cat))
        #     #self.myTree.addTopLevelItem(item_0)
        #     #print(item_0, item_0.text(0), self.myTree.indexOfTopLevelItem(item_0))
        #     item_0.setExpanded(True)
        #     self.tlis[cat] = item_0
        #self.ui.treeWidget.topLevelItem(0).child(0).setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled )

        #print(self.myTree.topLevelItemCount(), len(MyOptions.topLevelCategory))
        #self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("GameSettings", "Production N°"))
        # self.itemdict = dict()
        # self.brushdict = dict()
        # for objname, objcontent in MyOptions.defaults.items():  
        #     fatherItem = self.tlis[objcontent[MyOptions.parent__tlcid]]
        #     #print(objcontent[MyOptions.parent__tlcid], fatherItem, self.myTree.indexOfTopLevelItem(fatherItem))
        #     item = QtWidgets.QTreeWidgetItem(fatherItem, 
        #                                  QtWidgets.QTreeWidgetItem.DontShowIndicatorWhenChildless) 
        #     item.setToolTip(0, MyOptions.defaults[objname][5])   #[5] is tool tip string        
        #     item.setText(0, objname)
        #     #value = str(settin.value(objname, objcontent[0]).toByteArray())
        #
        #     value = settin.value(objname, objcontent[0])    #[0] is default value
        #     item.setText(1, str(value))
        #     self.itemdict[objname] = item
        #     self.brushdict[objname]   = item.background(1)
        #self.ui.verticalLayout.addWidget(self.myTree)
        
        #self.myTree.itemDoubleClicked.connect(self.onItemDoubleClick)
        # self.myTree.itemChanged.connect(self.onItemChanged)
        # self.myTree.currentItemChanged.connect(self.onCurrentItemChanged)
        #QtCore.QObject.connect(self.myTree, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"), self.onItemDoubleClick)
        #QtCore.QObject.connect(self.myTree, QtCore.SIGNAL("itemChanged(QTreeWidgetItem *,int)"), self.onItemChanged)
        
        #self.myTree.itemClicked.connect(self.onItemClick)
        #self.myTree.itemPressed.connect(self.onItemPressed)

        #self.myTree.itemActivated.connect(self.onItemActivated)
        #self.myTree.itemEntered.connect(self.onItemEntered)        

        
        # QtCore.QObject.connect(self.myTree, QtCore.SIGNAL("itemPressed (QTreeWidgetItem *,int)"), self.itemPressed)
        # QtCore.QObject.connect(self.myTree, QtCore.SIGNAL("itemActivated (QTreeWidgetItem *,int)"), self.itemActivated)
        # QtCore.QObject.connect(self.myTree, QtCore.SIGNAL("itemEntered (QTreeWidgetItem *,int)"), self.itemEntered)

 
        # QtCore.QObject.connect(self.ui.OKButton, QtCore.SIGNAL("clicked()"), self.OKAction)
        # QtCore.QObject.connect(self.ui.CancelButton, QtCore.SIGNAL("clicked()"), self.CancelAction)
        # QtCore.QObject.connect(self.ui.r2defButton, QtCore.SIGNAL("clicked()"), self.reset2Default)
        self.ui.applyandresetButton.clicked.connect(self.ApplyAction)
        self.ui.applyandcloseButton.clicked.connect(self.OKAction)
        self.ui.cancelButton.clicked.connect(self.cancelAction)
        
        self.ui.cancelButton.setAutoDefault(False)
        self.ui.applyandresetButton.setAutoDefault(False)
        self.ui.applyandcloseButton.setAutoDefault(False)
        # QtCore.QObject.connect(self.myTree, 
        #                        QtCore.SIGNAL("currentItemChanged (QTreeWidgetItem *,QTreeWidgetItem *)"), 
        #                        self.onCurrentItemChanged)

        #self.myTree.sortItems(0, Qt.AscendingOrder)
        
        
    def onItemPressed(self, witem, col):
        print("onItemPressed")
        pass       
        
    def onItemActivated(self, witem, col):
        print("itemActivated")
        #self.myTree.closePersistentEditor(witem, col)
        
    def onItemEntered(self, witem, col):
        print("itemEntered")
        pass      

    def onVItemClick(self, item):    
        # print("vitem clicvked", item.data()) 
        # print("    ", item.row()) 
        # print("    ", item.column()) 
        pass
                       
    # def onItemClick(self, wItem, col):
    #     #print("itemClicked")
    #     #print(self.myTree.selectedItems())
    #     if col != 1 :return
    #     if wItem in self.tlis.values(): return
    #     objname = wItem.text(0)
    #     if MyOptions.defaults[objname][1] == Hex:
    #         self.myTree.openPersistentEditor(wItem, col)
    #     elif MyOptions.defaults[objname][1] == Combo:
    #         myecombo = MyOptions.defaults[objname][7]
    #         mycombo  = QComboBox()
    #         mycombo.addItems(myecombo.items)
    #         self.myTree.setItemWidget(wItem, 1, mycombo)
    #

            
            
            
    # def itemChanged(self, witem, col):
    #     print("itemChanged")
    #     pass      
    #     newItem.setSelected(True)
        
    # def itemSelectionChanged(self):
    #     print("itemSelectionChanged")
        
                            
    # def onCurrentItemChanged(self, newItem, oldItem):
    #     #print("onCurrentItemChanged", newItem, newItem)
    #     if newItem in self.tlis.values(): return
    #     self.memoVal = newItem.text(1)
    #     objname = oldItem.text(0)
    #     if oldItem not in self.tlis.values():
    #         if MyOptions.defaults[objname][1] == Hex:
    #             self.myTree.closePersistentEditor(oldItem, 1)
    #         elif MyOptions.defaults[objname][1] == Combo:
    #             pass
    #             #self.myTree.setItemWidget(oldItem, 1, mycombo)
    #
    #
    #     self.myTree.openPersistentEditor(newItem, 1)
    #     #self.myTree.setCurrentItem(newItem, 1, QItemSelectionModel.SelectCurrent)
    #     #self.myTree.itemPressed.emit(newItem, 1)
    #     #self.itemPressed(newItem, 1)
    #     #self.myTree.edit(newItem, 1)
    #     #self.myTree.itemClicked.emit(newItem, 1)
    #     #print(self.myTree.selectedItems())
     
     
        
    def onItemPressed (self, wItem, col):
        print("onItemPressed", wItem, col)
        
    # def onItemDoubleClick (self, wItem, col):
    #     print("onItemDoubleClick", wItem, col)
    #     if col != 1 :return
    #     if wItem in self.tlis.values(): return
    #     self.memoVal = wItem.text(1)
    #     self.myTree.openPersistentEditor(wItem, 1)
    #

    # def onItemChanged(self, wItem, col):    
    #     if col != 1 :return
    #     if wItem in self.tlis.values(): return
    #     #print("onitemchanged", wItem, col)
    #     mybrush = QtGui.QBrush()
    #     mybrush.setColor(QtGui.QColor(Qt.red))
    #     mybrush.setStyle(Qt.Dense4Pattern)
    #     mybrushf = QtGui.QBrush()
    #     mybrushf.setColor(QtGui.QColor(Qt.green))
    #     mybrushf.setStyle(Qt.Dense5Pattern)
    #     validFunc = MyOptions.defaults[str(wItem.text(0))][2]       
    #     #print("validFunc", validFunc)
    #     if not validFunc:
    #         print("f invalid")
    #         return
    #     minval = MyOptions.defaults[str(wItem.text(0))][3] 
    #     maxval = MyOptions.defaults[str(wItem.text(0))][4] 
    #     try:
    #         optval = MyOptions.defaults[str(wItem.text(0))][7] 
    #     except:
    #         optval = None
    #     validated, msg = validFunc(wItem.text(1), minval, maxval, option=optval)
    #     if not validated:
    #         #print("nok old bg",wItem.background(1))
    #         #self.brushdict[wItem] = wItem.background(1)
    #         self.myTree.itemChanged.disconnect(self.onItemChanged)
    #         wItem.setBackground(1, mybrush)
    #         wItem.setToolTip(1, msg)
    #         self.myTree.itemChanged.connect(self.onItemChanged)
    #         #wItem.setForeground(1, mybrushf)
    #         #wItem.setText(1, self.memoVal)
    #     else:
    #         objname = list(self.itemdict.keys())[list(self.itemdict.values()).index(wItem)] 
    #         self.myTree.itemChanged.disconnect(self.onItemChanged)
    #         bbase   = self.brushdict[objname]
    #         bbase.setColor(QtGui.QColor(Qt.green))
    #         wItem.setBackground(1, mybrushf)
    #         wItem.setToolTip(1, msg)
    #         self.myTree.itemChanged.connect(self.onItemChanged)
    #         #print("ok new bg",wItem.background(1))
    #     self.myTree.closePersistentEditor(wItem, 1)
    #     #wItem.setSelected(False)

    def ApplyAction(self):
        papa = self.parent()
        if self.applyPresets() != "OK":
            return
        time.sleep(1.0)
        papa.resetthepin_with_ack()
        time.sleep(2.0)
        self.refreshdlg()
            
    def CancelAction(self):
        self.close() 
       
    def OKAction(self):
        if self.applyPresets() != "OK":
            return
        self.close() 

    
            
            
    def applyPresets(self):
        #print("applying presets")
        papa = self.parent()
        mininvrl = [x[1] for x in papa.nvrlist]
        
        errorlist=list()
        for objname, objcontent in MyOptions.defaults.items():  
            if objcontent[1] == Hex or objcontent[1] == Combo:
                #print(objname, self.itemvdict[objname].text())
                validFunc = MyOptions.defaults[objname][2]       
                if not validFunc:
                    print("f invalid")
                    #TODO write msg to console
                    return "KO Internal error Invalid valid func"
                minval = MyOptions.defaults[objname][3] 
                maxval = MyOptions.defaults[objname][4] 
                try:
                    optval = MyOptions.defaults[objname][7] 
                except:
                    optval = None
                validated, msg = validFunc(self.itemvdict[objname].text(), minval, maxval, option=optval)
                if not validated:
                    errorlist.append(objname)
                # print(objname, self.itemvdict[objname].text(), 
                #        optval.addr, 
                #        optval.type, 
                #        optval.dir,
                #        optval.value)
                
            # following elif neutralized 2025-01-11 because combo might have been initialized
            #with invalid value... Then we handle it now correctly in the previous if, like Hex type
            # elif objcontent[1] == Combo:
            #     #no validfunc required since it is a combo
            #     try:
            #         optval = MyOptions.defaults[objname][7] 
            #     except:
            #         optval = None
            #     #print(objname, self.itemvdict[objname].data(0), self.itemvdict[objname].data(Qt.UserRole))
            #     #print(objname, self.itemvdict[objname].data(Qt.UserRole))
            #     ilis = self.itemvdict[objname].data(Qt.UserRole)
                
        if len(errorlist):
            self.ui.label.setText("Please check the following fields: "+ ", ".join(errorlist))
            return "KO Settings invalid"
        else:
            self.ui.label.setText("")

        #print("nvr avant", [(f"{x:02X}", f"{y:02X}") for (x,y) in papa.nvrlist])
        bmap = [x[1] for x in papa.nvrlist]
        for objname, objcontent in MyOptions.defaults.items():  
            if objcontent[1] == Hex:
                hexemple = MyOptions.defaults[objname][7] 

                h = Hex(self.itemvdict[objname].text(),
                        hexemple.addr,
                        hexemple.type,
                        hexemple.dir,
                        len(hexemple.value)
                        )
                bmap = Hex.updateMapFromHex(bmap, h)
            elif objcontent[1] == Combo:
                cexemple = MyOptions.defaults[objname][7]
                
                c = Combo(self.itemvdict[objname].text(),
                    cexemple.vtl,
                    cexemple.bitMask,
                    cexemple.addr,      
                    )
                bmap = Combo.updateMapFromCombo(bmap, c)
        #print(bmap)
        papa.nvrlist = list(zip([x[0] for x in papa.nvrlist], bmap))
        #print("nvr apres", [(f"{x:02X}", f"{y:02X}") for (x,y) in papa.nvrlist])
        papa.send_reqwriteall()
        time.sleep(1.0)
        papa.send_reqflash()
        time.sleep(0.3)
        return "OK"
    # def saveSettings(self):
    #     for i in range(self.myTree.topLevelItemCount()):
    #         item = self.myTree.topLevelItem(i)  
    #         self.settin.setValue(item.text(0), item.text(1))
    #     self.settin.sync()

            
    # def reset2Default(self):
    #     for i in range(self.myTree.topLevelItemCount()):
    #         item = self.myTree.topLevelItem(i) 
    #         item.setText(1, str(MyOptions.defaults[str(item.text(0))][0]))


    def cancelAction(self):
        self.close()
        

    # def onkeyPressEvent(self, event):
    #     # when press key is Tab call your function
    #     if event.key() == Qt.Key_Tab:
    #         print("keytab")
    #     else:
    #         print("pas keytab")

    def createPropertyModel(self, parent):
        model = QStandardItemModel(0, 2, parent)
        model.setHeaderData(self.PROPERTY, Qt.Horizontal, "Property")
        model.setHeaderData(self.VALUE, Qt.Horizontal, "Value")
        return model   
    
    def addProperty(self, model, parentItem, property, value):
        myItem = QStandardItem(property)
        # model.setData(model.index(0, self.PROPERTY), property)
        # model.setData(model.index(0, self.VALUE), value)
        parentItem.appendRow(myItem)


    def onItemDataChange(self, vItem):
        # print("onItemDataChange", vItem.text())
        # print(vItem, vItem.data(Qt.UserRole), vItem.text(), vItem.model(), vItem.index())
        # print(vItem.index().data(self.PROPERTY))
        # print(vItem.index().data(self.VALUE))
        # print(vItem.index().column())
        # print(vItem.index().row())
        modelIndex = vItem.index().siblingAtColumn(0)
        #print(modelIndex.data(0))
        objname = modelIndex.data(0)
        mybrush = QtGui.QBrush()
        mybrush.setColor(QtGui.QColor(Qt.red))
        mybrush.setStyle(Qt.Dense4Pattern)
        mybrushf = QtGui.QBrush()
        mybrushf.setColor(QtGui.QColor(Qt.green))
        mybrushf.setStyle(Qt.Dense5Pattern)
    
        validFunc = MyOptions.defaults[objname][2]       
        #print("validFunc", validFunc)
        if not validFunc:
            print("f invalid")
            return
        vItem.model().itemChanged.disconnect(self.onItemDataChange)
        minval = MyOptions.defaults[objname][3] 
        maxval = MyOptions.defaults[objname][4] 
        try:
            optval = MyOptions.defaults[objname][7] 
        except:
            optval = None
        validated, msg = validFunc(vItem.text(), minval, maxval, option=optval)
        #print("validation", validated, msg, objname, optval)
        

        if not validated:
            #print("nok old bg",wItem.background(1))
            #self.brushdict[wItem] = wItem.background(1)
            vItem.setBackground(mybrush)
            vItem.setToolTip(msg)
            #wItem.setForeground(1, mybrushf)
            #wItem.setText(1, self.memoVal)
        else:
            bbase   = self.brushvdict[objname]
            bbase.setColor(QtGui.QColor(Qt.green))
            vItem.setBackground(mybrushf)
            vItem.setToolTip(msg)
            #print("ok new bg",wItem.background(1))
        #wItem.setSelected(False)
        vItem.model().itemChanged.connect(self.onItemDataChange)


    def onEditorClose(self, editor):
        print("editor closed in treeview", editor)
        