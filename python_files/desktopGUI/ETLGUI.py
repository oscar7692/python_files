#!/usr/bin/python3
# -*- coding: utf-8 -*-

###########################
#         ETL GUI         #
# Author --> oscar pulido # QMainWindow  buscar
###########################

import sys
from PyQt5.QtWidgets import (QToolTip, QPushButton, QApplication, QWidget,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QFont

class Login(QWidget):           #clase de la ventana de login

    def __init__(self):         #constructor

        super(Login, self).__init__()
        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))    #define el tipo de fuente

        #self.setToolTip('Type your credentials') #permite usar texto enriquesido

        loginButton = QPushButton("Login")          #crea los botones
        cancelButton = QPushButton("Cancel", self)  #login y cancel
        cancelButton.clicked.connect(QApplication.instance().quit)    #llama la instancia QPushButton para cerrar el software
        #cancelButton.resize(cancelButton.sizeHint())

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(cancelButton)
        hbox.addWidget(loginButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('SoftETL')
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    log = Login()
    sys.exit(app.exec_())