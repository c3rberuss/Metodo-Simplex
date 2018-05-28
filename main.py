#!/usr/bin/python3
#-*- coding: utf-8 -*-

from PyQt5.Qt import QIntValidator, QDoubleValidator, QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, QDialog, QComboBox,
                             QLineEdit, QLayoutItem, QInputDialog, QMessageBox)

from interfaz import main_interfaz, simplex_interfaz
from metodos import simplex_v4 as sp
from fractions import Fraction
from metodos.report.Reporte import saveReport

import sys

app = QApplication(sys.argv)


class Simplex(QDialog, simplex_interfaz.Ui_Dialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.validator = QDoubleValidator()

        self.txtRestricciones.setClearButtonEnabled(True)
        self.txtVariables.setClearButtonEnabled(True)

        self.txtRestricciones.setValidator( QIntValidator())
        self.txtVariables.setValidator( QIntValidator())

        self.scrollContent.setLayout(self.gridData)
        self.scrollAreaWidgetContents.setLayout(self.func_object)

        self.btnClose.clicked.connect(self.close)

        self.txtRestricciones.textChanged['QString'].connect(
            self.generateInputs)
        self.txtVariables.textChanged['QString'].connect(self.generateInputs)

        self.label_3.setVisible(False)
        self.label_4.setVisible(False)

        self.btnSolve.clicked.connect(self.solve)

    def generateInputs(self):

        self.i = 0
        self.j = 0
        self.ant_i = 0
        self.ant_j = 0

        if self.txtRestricciones.text() != '' and self.txtVariables.text() != '':
            self.clearLayout()
            self.i = int(self.txtRestricciones.text())
            self.j = int(self.txtVariables.text()) + 2

            self.label_3.setVisible(True)
            self.label_4.setVisible(True)
            self.addElements(self.i, self.j)

    def clearLayout(self):

        for x in range(self.func_object.columnCount()):
            if self.func_object.itemAtPosition(0, x) != None:
                self.func_object.itemAtPosition(0, x).widget().setParent(None)

        try:
            for restriccion in range(self.gridData.rowCount()):
                for variable in range(self.gridData.columnCount()):

                    if self.gridData.itemAtPosition(restriccion, variable) != None:
                        self.gridData.itemAtPosition(
                            restriccion, variable).widget().setParent(None)

        except Exception as e:
            print(e, " - ",line_err)

        self.gridLayout.update()
        self.update()
        self.repaint()

    def solve(self):

        print("DATA: ", self.getData())
        data = sp.simplex(self.getData(), self.cbxMax_min.currentText())


        reporte = saveReport(data[0], data[1], data[2], data[3])
        reporte.crear_pdf()
        reporte.mostrar_pdf()

        data = None
        reporte = None

        """mensaje = QMessageBox(self)
        mensaje.setText(str(data))
        mensaje.exec_()"""

    def getData(self):

        data = []
        sub_data = {}
        tmp = {}

        for x in range(self.func_object.columnCount()):
            tmp['X' + str(x + 1)] = float(str(self.func_object.itemAtPosition(0,
                                                                          x).widget().text()))

        sub_data['func_obj'] = tmp
        tmp = {}
        data.append(sub_data)
        sub_data = {}

        for fila in range(self.gridData.rowCount()):
            for columna in range(self.gridData.columnCount()):

                if columna == self.gridData.columnCount() - 2:

                    tmp['desigualdad' + str(fila + 1)] = self.gridData.itemAtPosition(
                        fila, columna).widget().currentText()

                elif columna == self.gridData.columnCount() - 1:

                    tmp['b' + str(fila + 1)] = float(
                        str(self.gridData.itemAtPosition(fila, columna).widget().text()))

                else:

                    tmp['X' + str(columna + 1)] = float(
                        str(self.gridData.itemAtPosition(fila, columna).widget().text()))

            sub_data['restric_' + str(fila + 1)] = tmp
            tmp = {}

            data.append(sub_data)
            sub_data = {}

        return data

    def addElements(self, i=0, j=0):

        for x in range(j - 2):
            input_ = QLineEdit()
            input_.setValidator(self.validator)
            input_.setPlaceholderText("X" + str(x + 1))
            input_.setMinimumWidth(40)
            self.func_object.addWidget(input_, 0, x)

        for restriccion in range(i):

            for variable in range(j):

                if variable == j - 2:

                    combo = QComboBox()
                    combo.addItems(['<=', '>=', '='])

                    self.gridData.addWidget(combo, restriccion, variable)

                elif variable == j - 1:

                    input_ = QLineEdit()
                    input_.setValidator(self.validator)
                    #print("Var: "+str(variable))

                    input_.setPlaceholderText("b" + str(restriccion + 1))
                    input_.setMinimumWidth(40)
                    self.gridData.addWidget(input_, restriccion, variable)

                else:

                    input_ = QLineEdit()
                    input_.setValidator(self.validator)
                    #print("Var: "+str(variable))

                    input_.setMinimumWidth(40)
                    input_.setPlaceholderText("X" + str(variable + 1))
                    self.gridData.addWidget(input_, restriccion, variable)


class Main(QMainWindow, main_interfaz.Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # self.lineEdit.textChanged['QString'].connect(self.mensaje)

        simplex = QAction("SIMPLEX", self)
        simplex.setShortcut("Ctrl+S")

        self.menuM_todos.addAction(simplex)
        simplex.triggered.connect(self.ui_simplex)
        #self.resize(640,480)
        self.setFixedSize(640,380)

        background =QPixmap("back.jpg")
        background = background.scaled(self.size())
        pal = self.palette()
        pal.setBrush(QPalette.Background, QBrush(background))
        self.setPalette(pal)

        self.setStyleSheet(" QMenuBar{ background-color: #e1e1e1} ")

    def mensaje(self):
        print(self.lineEdit.text())

    def ui_simplex(self):
        ventana = Simplex()
        ventana.parent = self
        ventana.exec_()


main = Main()

main.show()

app.exec_()
