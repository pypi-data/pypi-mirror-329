#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
clklabel.py

Created on 15 nov 2024

@author: garzol
Copyright AA55 Consulting 2024

A PyQt5 QLabel that one can get events click, dblclick or tripleClic

'''

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, QTimer

class ClkLabel(QLabel):
    
    simpleClicked = pyqtSignal()
    doubleClicked = pyqtSignal()
    tripleClicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.timer1 = QTimer()
        self.timer1.setSingleShot(True)
        self.timer1.timeout.connect(self.simpleClicked.emit)
        self.timer2 = QTimer()
        self.timer2.setSingleShot(True)
        self.timer2.timeout.connect(self.doubleClicked.emit)
        #super().clicked.connect(self.checkDoubleClick)

    def checkMultiClick(self):
        if self.timer2.isActive():
            self.tripleClicked.emit()
            self.timer2.stop()
        elif self.timer1.isActive():
            self.timer2.start(250)
            self.timer1.stop()
        else:
            self.timer1.start(250)
            


    def mousePressEvent(self, ev):
        #self.clicked.emit()
        pass
        
    def mouseReleaseEvent(self, ev):
        self.checkMultiClick()