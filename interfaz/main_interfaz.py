# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_interfaz.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 404)
        MainWindow.setMinimumSize(QtCore.QSize(320, 240))
        MainWindow.setMaximumSize(QtCore.QSize(640, 480))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/calculator.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet("")
        MainWindow.setWindowFilePath("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnSimplex = QtWidgets.QPushButton(self.centralwidget)
        self.btnSimplex.setMinimumSize(QtCore.QSize(0, 50))
        self.btnSimplex.setMaximumSize(QtCore.QSize(16777215, 100))
        self.btnSimplex.setStyleSheet("font: 75 14pt \"Noto Sans\";\n"
"background-color: #e1e1e1;\n"
"color: black;")
        self.btnSimplex.setObjectName("btnSimplex")
        self.horizontalLayout.addWidget(self.btnSimplex)
        self.btnTransporte = QtWidgets.QPushButton(self.centralwidget)
        self.btnTransporte.setMinimumSize(QtCore.QSize(0, 50))
        self.btnTransporte.setMaximumSize(QtCore.QSize(16777215, 100))
        self.btnTransporte.setStyleSheet("font: 75 14pt \"Noto Sans\";\n"
"background-color: #e1e1e1;\n"
"color: black;")
        self.btnTransporte.setObjectName("btnTransporte")
        self.horizontalLayout.addWidget(self.btnTransporte)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 23))
        self.menubar.setObjectName("menubar")
        self.menuM_todos = QtWidgets.QMenu(self.menubar)
        self.menuM_todos.setObjectName("menuM_todos")
        self.menuAcerca_de = QtWidgets.QMenu(self.menubar)
        self.menuAcerca_de.setObjectName("menuAcerca_de")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSIMPLEX = QtWidgets.QAction(MainWindow)
        self.actionSIMPLEX.setObjectName("actionSIMPLEX")
        self.menubar.addAction(self.menuM_todos.menuAction())
        self.menubar.addAction(self.menuAcerca_de.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Métodos de Optimización"))
        self.btnSimplex.setText(_translate("MainWindow", "SIMPLEX - (Ctrl+S)"))
        self.btnTransporte.setText(_translate("MainWindow", "TRANSPORTE - (Ctrl+T)"))
        self.menuM_todos.setTitle(_translate("MainWindow", "Métodos"))
        self.menuAcerca_de.setTitle(_translate("MainWindow", "Acerca de"))
        self.actionSIMPLEX.setText(_translate("MainWindow", "SIMPLEX"))

from resources import recursos_rc
