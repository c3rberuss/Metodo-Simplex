#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Esquina_Noroeste():

    data = None
    matriz = None
    max_min = None

    def __init__(self, data_, max_min_):

        self.data = data_
        self.max_min = max_min_


    def matriz(self, filas, columnas):
        matriz = []

        for i in range(filas):
            matriz.append([])
            for j in range(columnas):
                matriz[i].append(None)

        return matriz

    def generar_matriz(self):

        n_filas = len(self.data)
        n_columnas = len(self.data[0])

        self.matriz = self.matriz(n_filas, n_columnas)

        for j in range(n_filas):

            for i in range(n_columnas):

                if self.data[j][i] != None:
                    self.matriz[j][i] = self.data[j][i]
                else:
                    self.matriz[j][i] = None


    def is_balancing(self):

        ai = []
        bi = []

        for j in range(1, len(self.matriz)-1, 1):
            ai.append(self.matriz[j][len(self.matriz[0])-1])

        for i in range(1, len(self.matriz[0])-1, 1):
            bi.append(self.matriz[len(self.matriz)-1][i])

        if sum(ai) > sum(bi):
            return False, "Agregar Destino", sum(ai) - sum(bi)
        elif sum(ai) < sum(bi):
            return False, "Agregar Origen", sum(bi) - sum(ai)
        elif sum(ai) == sum(bi):
            return True

    def balancear(self, donde_agregar):
        print(donde_agregar)
        for x in self.matriz:
            print(x)

        if donde_agregar[1] == "Agregar Destino":

            for j in range(1, len(self.matriz), 1):

                if j < len(self.matriz)-2:
                    self.matriz[j].insert(len(self.matriz[0])-1, 0)
                elif j == len(self.matriz)-1:
                    self.matriz[0].insert(len(self.matriz[0])-1, "*")
                    self.matriz[j].insert(len(self.matriz[0])- 1, donde_agregar[2])

            for x in self.matriz:
                print(x)

        else:

            tmp = []

            for i in range(len(self.matriz[0])):

                if i == 0:
                    tmp.append('*')
                elif i < len(self.matriz[0])-2:
                    tmp.append(0)
                elif i == len(self.matriz)-1:
                    tmp.append(0)
                    tmp.append(donde_agregar[2])

            self.matriz.insert(len(self.matriz)-1, tmp)

            for x in self.matriz:
                print(x)



    def sol_factible_basica_inicial(self):
        pass



prueba = [ ["Origen\\Destino", 1,2,3,4,"Oferta"],
           [1,80,70,60,60,8], [2,50,70,80,70,10],
           [3,70,50,80,60,5], ["Demanda",15,4,6,4,None]]

en = Esquina_Noroeste(prueba, "Minimizar")

en.generar_matriz()
en.balancear(en.is_balancing())