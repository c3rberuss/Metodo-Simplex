#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.Qt import QIntValidator, QDoubleValidator, QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, QDialog, QComboBox,
                             QLineEdit, QLabel)

from interfaz import main_interfaz, simplex_interfaz, transporte_interfaz
from metodos import simplex_v4 as sp
from metodos.report.Reporte import saveReport

app = QApplication(sys.argv)


class Simplex(QDialog, simplex_interfaz.Ui_Dialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.validator = QDoubleValidator()

        self.txtRestricciones.setClearButtonEnabled(True)
        self.txtVariables.setClearButtonEnabled(True)

        self.txtRestricciones.setValidator(QIntValidator())
        self.txtVariables.setValidator(QIntValidator())

        self.scrollContent.setLayout(self.gridData)
        self.scrollAreaWidgetContents.setLayout(self.func_object)

        self.btnClose.clicked.connect(self.close)

        self.txtRestricciones.textChanged['QString'].connect(
            self.generateInputs)
        self.txtVariables.textChanged['QString'].connect(self.generateInputs)

        self.label_3.setVisible(False)
        self.label_4.setVisible(False)

        self.btnSolve.clicked.connect(self.solve)

        self.btnLimpiar.clicked.connect(self.clearLayout)

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

        self.label_3.setVisible(False)
        self.label_4.setVisible(False)

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
            # print(e, " - ", line_err)
            pass

        self.gridLayout.update()
        self.update()
        self.repaint()

    def solve(self):

        print("DATA: ", self.getData())
        data = sp.simplex(self.getData(), self.cbxMax_min.currentText())

        print("DATA", data)

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
            if str(self.func_object.itemAtPosition(0, x).widget().text()) != '':
                tmp['X' + str(x + 1)] = float(str(self.func_object.itemAtPosition(0, x).widget().text()))
            else:
                tmp['X' + str(x + 1)] = float(0)

        sub_data['func_obj'] = tmp
        tmp = {}
        data.append(sub_data)
        sub_data = {}

        for fila in range(self.gridData.rowCount()):
            for columna in range(self.gridData.columnCount()):

                if columna == self.gridData.columnCount() - 2:

                    tmp['desigualdad' + str(fila + 1)] = self.gridData.itemAtPosition(fila,
                                                                                      columna).widget().currentText()

                elif columna == self.gridData.columnCount() - 1:

                    tmp['b' + str(fila + 1)] = float(
                        str(self.gridData.itemAtPosition(fila, columna).widget().text()))

                else:

                    if str(self.gridData.itemAtPosition(fila, columna).widget().text()) != '':
                        tmp['X' + str(columna + 1)] = float(
                            str(self.gridData.itemAtPosition(fila, columna).widget().text()))
                    else:
                        tmp['X' + str(columna + 1)] = float(0)

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
                    # print("Var: "+str(variable))

                    input_.setPlaceholderText("b" + str(restriccion + 1))
                    input_.setMinimumWidth(40)
                    self.gridData.addWidget(input_, restriccion, variable)

                else:

                    input_ = QLineEdit()
                    input_.setValidator(self.validator)
                    # print("Var: "+str(variable))

                    input_.setMinimumWidth(40)
                    input_.setPlaceholderText("X" + str(variable + 1))
                    self.gridData.addWidget(input_, restriccion, variable)


class Transporte(QDialog, transporte_interfaz.Ui_Dialog):
    validator = None
    n_origenes = None
    n_destinos = None

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.btnClose.clicked.connect(self.close)

        self.validator = QDoubleValidator()

        self.txtDestinos.setClearButtonEnabled(True)
        self.txtOrigenes.setClearButtonEnabled(True)

        self.txtDestinos.setValidator(QIntValidator())
        self.txtOrigenes.setValidator(QIntValidator())

        self.scrollContent.setLayout(self.gridData)

        self.txtOrigenes.textChanged['QString'].connect(self.generate_inputs)
        self.txtDestinos.textChanged['QString'].connect(self.generate_inputs)

        self.resize(720, 480)

    def generate_inputs(self):

        if self.txtOrigenes.text() == '' or self.txtDestinos.text() == '':
            self.n_destinos = 0
            self.n_origenes = 0
        else:
            self.n_origenes = int(self.txtOrigenes.text()) + 2
            self.n_destinos = int(self.txtDestinos.text()) + 2

        i = 1

        for origen in range(self.n_origenes):

            for destino in range(self.n_destinos):

                if origen == 0 and destino == 0:

                    label = QLabel("Origen\\Destino")
                    self.gridData.addWidget(label, origen, destino)

                elif origen == 0 and destino != self.n_destinos - 1:

                    input_ = QLineEdit()
                    input_.setPlaceholderText("Destino " + str(destino))
                    self.gridData.addWidget(input_, origen, destino)

                elif origen == 0 and destino == self.n_destinos - 1:

                    label = QLabel("Oferta")
                    self.gridData.addWidget(label, origen, destino)

                elif origen != self.n_origenes - 1 and destino == 0:

                    input_ = QLineEdit()
                    input_.setPlaceholderText("Origen " + str(origen))
                    self.gridData.addWidget(input_, origen, destino)

                elif origen == self.n_origenes - 1 and destino == 0:

                    label = QLabel("Demanda")
                    self.gridData.addWidget(label, origen, destino)

                elif origen == self.n_origenes - 1 and destino < self.n_destinos - 1:

                    input_ = QLineEdit()
                    input_.setValidator(QDoubleValidator())
                    input_.setPlaceholderText("Demanda " + str(destino))
                    self.gridData.addWidget(input_, origen, destino)

                elif origen > 0 and origen < self.n_origenes - 1 and destino == self.n_destinos - 1:

                    input_ = QLineEdit()
                    input_.setValidator(QDoubleValidator())
                    input_.setPlaceholderText("Oferta " + str(origen))
                    self.gridData.addWidget(input_, origen, destino)

                elif origen > 0 and origen < self.n_origenes - 1 and destino > 0 and destino < self.n_destinos - 1:

                    input_ = QLineEdit()
                    input_.setValidator(QDoubleValidator())
                    input_.setPlaceholderText("costo " + str(i))
                    self.gridData.addWidget(input_, origen, destino)

                    i += 1

        # for restriccion in range(i):
        #
        #     for variable in range(j):
        #
        #         if variable == j - 2:
        #
        #             combo = QComboBox()
        #             combo.addItems(['<=', '>=', '='])
        #
        #             self.gridData.addWidget(combo, restriccion, variable)
        #
        #         elif variable == j - 1:
        #
        #             input_ = QLineEdit()
        #             input_.setValidator(self.validator)
        #             # print("Var: "+str(variable))
        #
        #             input_.setPlaceholderText("b" + str(restriccion + 1))
        #             input_.setMinimumWidth(40)
        #             self.gridData.addWidget(input_, restriccion, variable)
        #
        #         else:
        #
        #             input_ = QLineEdit()
        #             input_.setValidator(self.validator)
        #             # print("Var: "+str(variable))
        #
        #             input_.setMinimumWidth(40)
        #             input_.setPlaceholderText("X" + str(variable + 1))
        #             self.gridData.addWidget(input_, restriccion, variable)


class Main(QMainWindow, main_interfaz.Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # self.lineEdit.textChanged['QString'].connect(self.mensaje)

        simplex = QAction("SIMPLEX", self)
        simplex.setShortcut("Ctrl+S")

        self.menuM_todos.addAction(simplex)
        simplex.triggered.connect(self.ui_simplex)

        transporte = QAction("TRANSPORTE", self)
        transporte.setShortcut("Ctrl+T")

        self.menuM_todos.addAction(transporte)
        transporte.triggered.connect(self.ui_transporte)

        # self.resize(640,480)
        self.setFixedSize(640, 380)

        background = QPixmap("back.jpg")
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

    def ui_transporte(self):
        ventana = Transporte()
        ventana.parent = self
        ventana.exec_()


main = Main()

main.show()

app.exec_()
