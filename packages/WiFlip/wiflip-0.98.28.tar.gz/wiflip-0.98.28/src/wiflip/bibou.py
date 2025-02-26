'''
Created on 23 mars 2022

@author: garzol
'''



import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MyWindow( QMainWindow ):
    
    def __init__ ( self ) :
        QMainWindow.__init__( self )
        self.setWindowTitle( 'First steps With PyQt and Python3' )
        self.resize(400, 300)

        self.__button1 = QPushButton( "First button", self )
        self.__button1.setGeometry(10, 10, 200, 35)
    
        self.__button2 = QPushButton( "Second button", self )
        self.__button2.setGeometry(10, 50, 200, 35)
        

if __name__ == "__main__" :
    app = QApplication( sys.argv )
    print("c'est parti")
    myWindow = MyWindow()
    myWindow.show()
    
    app.exec_()
