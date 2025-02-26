#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
mytreeview.py

Created on 7 sept. 2011

@author: garzol
Copyright AA55 Consulting 2011

my own tree view

'''
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from PyQt5.QtWidgets import QTreeView, QStyledItemDelegate, QComboBox
#from PyQt5.Qt import QComboBox

class MyTreeView(QTreeView):
    '''
    unused at the moment
    '''
    def __init__(self):
        super().__init__()



class MyDelegate(QStyledItemDelegate):
    '''
    This is the means to have editors such as combo in a treeview widget
    '''
    def __init__(self):
        super().__init__()
        self.closeEditor.connect(self.onEditorClose)
    
    def createEditor(self, parent, option, index):
        #print("createeditor", parent, option, index)
        if index.data(Qt.UserRole) is None:
            return super().createEditor(parent, option, index)
        
        comboEditor = QComboBox(parent)
        #comboEditor.view().installEventFilter(self)
        #self.closeEditor.connect(self.onEditorClose)

        return comboEditor


    def setEditorData(self, editor, index):
        if type(editor) != QComboBox:
            return super().setEditorData(editor, index)

        options = index.data(Qt.UserRole)
        editor.addItems(options)
        value = index.data()
        try:
            current = options.index(value)
        except:
            current = -1
        if current > -1:
            editor.setCurrentIndex(current)

        editor.setStyleSheet(
            """
            
           QComboBox {background-color: MidnightBlue;
           /*color: white;*/
           }
           
            QComboBox:!editable, QComboBox::drop-down:editable {
                /*color: white;*/
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 Navy, stop: 0.4 Blue,
                                            stop: 0.5 RoyalBlue, stop: 1.0 MidnightBlue);
            }


            """
                            )
        #editor.showPopup()

        # model = editor.model()
        # for row in range(editor.count()):
        #     model.setData(model.index(row, 0), QtGui.QColor("red"), Qt.BackgroundRole)
        #
        # editor.setModel(model)

    def setModelData(self, editor, model, index):
        if type(editor) != QComboBox:
            return super().setModelData(editor, model, index)
        model.setData(index, editor.currentText())
    
    # def closeEditor(self):
    #     print("closeditor!")
    #     #return super().onEditorClose(parent, editor, hint)
    #

    def onEditorClose(self, editor, hint):
        #print("editor closed", editor, hint)
        #editor.hidePopup()
        pass

