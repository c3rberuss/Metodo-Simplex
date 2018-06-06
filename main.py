#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import copy
from PyQt5.Qt import QIntValidator, QDoubleValidator, QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, QDialog, QComboBox,
                             QLineEdit, QLabel, QMessageBox, QInputDialog)

from interfaz import main_interfaz, simplex_interfaz, transporte_interfaz, about
from metodos import simplex_v4 as sp
from metodos.report.Reporte import saveReport
from resources import recursos_rc

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
                self.func_object.itemAtPosition(0, x).widget().deleteLater()

        try:
            for restriccion in range(self.gridData.rowCount()):
                for variable in range(self.gridData.columnCount()):

                    if self.gridData.itemAtPosition(restriccion, variable) != None:
                        self.gridData.itemAtPosition(
                            restriccion, variable).widget().deleteLater()

        except Exception as e:
            # print(e, " - ", line_err)
            pass

        self.gridLayout.update()
        self.update()
        self.repaint()

    def solve(self):

        print("DATA: ", self.getData())
        data = sp.simplex(self.getData(), self.cbxMax_min.currentText())

        if 'Múltiples' in data[3]['mensaje']:
            message = QMessageBox()
            message.setWindowTitle(data[3]['mensaje'])
            message.setText("El problema tiene soluciones múltiples.")

            sol = ""
            for var in data[1]:
                sol = sol + var + "\n"

            message.setInformativeText("Solución: \n\n" + sol + "\n" + "¿Desea obtener una nueva solución?")
            yes = message.addButton("Sí", QMessageBox.YesRole)
            no = message.addButton("No", QMessageBox.NoRole)
            message.setIcon(QMessageBox.Information)
            message.setStyleSheet("font-weight: bold;")

            message.exec()

            if message.clickedButton() == yes:
                print("1************")
                self.nueva_sol(data[0], data[3], data[1], data[2], data[4], data[5])
            elif message.clickedButton() == no:

                reporte = saveReport(data[0], data[1], data[2], data[3])
                reporte.crear_pdf()
                reporte.mostrar_pdf()

            else:
                print("A: ", message.clickedButton())
                print("B: ", yes)
                print("C: ", no)
        elif "Ilimitadas" in data[3]['mensaje']:
            reporte = saveReport(data[0], data[1], data[2], data[3])
            reporte.crear_pdf()
            reporte.mostrar_pdf()
        else:
            reporte = saveReport(data[0], data[1], data[2], data[3])
            reporte.crear_pdf()
            reporte.mostrar_pdf()

        print("DATA", data)

        data = None
        reporte = None

    def nueva_sol(self, restricciones, mensaje, respuesta, iteraciones, holgura, artificial):

        vars_sol = []

        vars_entrada = []

        ultima_iteracion = iteraciones[len(iteraciones)-1]

        for var in respuesta:
            tmp = str(var).split(" = ")
            if float(tmp[1]) > 0 and tmp[0] != 'Z':
                vars_sol.append(tmp[0])

        print("VARIABLES DE LA SOLUCION: ", vars_sol)

        for var in range(len(ultima_iteracion[0])):
            if ultima_iteracion[0][var] != "V.B" and ultima_iteracion[0][var] != 'bi' and not ultima_iteracion[0][var] in vars_sol:
                if ultima_iteracion[len(ultima_iteracion)-1][var] == 0:
                    vars_entrada.append(ultima_iteracion[0][var])

        print("VARIABLES DE ENTRADA: ", vars_entrada)

        input_ = QInputDialog(self)
        input_.setLabelText("Seleccione la nueva Variable de Entrada")
        input_.setWindowTitle("Seleccione la Nueva Variable de entrada")
        input_.setComboBoxItems(vars_entrada)
        input_.setOkButtonText("Encontrar la nueva Solución")
        input_.setCancelButtonText("Cancelar")
        button = input_.exec()

        print("RESULT: ", input_.textValue())
        print("BUTTON: ", button)

        pivote = sp.special_solution(ultima_iteracion[0].index(input_.textValue()), ultima_iteracion)

        sol_ = copy.deepcopy(ultima_iteracion)
        sol_ = sp.var_salida(sol_, pivote)
        sol_ = sp.reducir_fila_pivote(sol_, pivote)

        sol_ = sp.nueva_solucion_v2(sol_, pivote, holgura, artificial)
        sol_ = sp.depurar_nueva_solucion(sol_)
        iteraciones.append(sol_)

        respuesta = sp.generar_solucion(sol_, 2)

        reporte = saveReport(restricciones, respuesta, iteraciones, mensaje)
        reporte.crear_pdf()
        reporte.mostrar_pdf()

    def getData(self):

        data = []
        sub_data = {}
        tmp = {}
        variables = int(self.txtVariables.text())+2
        filas = int(self.txtRestricciones.text())

        print("COLUMNAS FUNC OBJ: ", self.txtVariables.text())

        for x in range(int(self.txtVariables.text())):
            if self.func_object.itemAtPosition(0, x) != None:
                if str(self.func_object.itemAtPosition(0, x).widget().text()) != '':
                    tmp['X' + str(x + 1)] = float(str(self.func_object.itemAtPosition(0, x).widget().text()))
                else:
                    tmp['X' + str(x + 1)] = float(0)

        sub_data['func_obj'] = tmp
        tmp = {}
        data.append(sub_data)
        sub_data = {}

        for fila in range(filas):
            for columna in range(variables):

                if columna == variables - 2:

                    tmp['desigualdad' + str(fila + 1)] = self.gridData.itemAtPosition(fila,columna).widget().currentText()

                elif columna == variables - 1:

                    tmp['b' + str(fila + 1)] = float(str(self.gridData.itemAtPosition(fila, columna).widget().text()))

                else:

                    if self.gridData.itemAtPosition(fila, columna).widget() != None:
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


class About(QDialog, about.Ui_Dialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)


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
        self.setFixedSize(640, 360)

        background = QPixmap(":/back.jpg")
        background = background.scaled(self.size())
        pal = self.palette()
        pal.setBrush(QPalette.Background, QBrush(background))
        self.setPalette(pal)

        self.setStyleSheet(" QMenuBar{ background-color: #e1e1e1} ")

        self.btnSimplex.clicked.connect(simplex.trigger)
        self.btnTransporte.clicked.connect(transporte.trigger)

        dev = QAction("Desarrolador", self)
        dev.setShortcut("Ctrl+D")
        self.menuAcerca_de.addAction(dev)
        dev.triggered.connect(self.about_dev)

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

    def about_dev(self):
        dev = About()
        dev.parent = self
        dev.exec_()


main = Main()

main.show()

app.exec_()
