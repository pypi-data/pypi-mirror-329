#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 29 mars 2016

@author: a030466

recupere de msc project
obsolete
'''

from PyQt5 import QtCore, QtGui, QtWidgets

class MyTreeWidget(QtWidgets.QTreeWidget):
    """
    reimplemented from QTreeWidget
    Because we want to handle our specific mimedata
    
    """
    def __init__(self, mimeTyp="application/x-aa55tree", parent=None):
        super(MyTreeWidget, self).__init__(parent)
        self.mimeTyp=mimeTyp
    
    
    def mimeData(self, itemList):
#         super(MyTreeWidget, self).mimeData(itemList)
        if not len(itemList):
            return 0
        
        mimeData = QtCore.QMimeData()
        itemData = QtCore.QByteArray("garzol") #dummy use provisory

        txt=""
        for it in itemList:
            itemData += QtCore.QByteArray("garzol")
            txt += it.data(0, QtCore.Qt.UserRole).toString()+'\n'
        
        mimeData.setData(self.mimeTyp, itemData)
        mimeData.setText(txt)
        
        return mimeData
