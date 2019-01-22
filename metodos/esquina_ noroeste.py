#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Esquina_Noroeste():

    data = None
    matriz = None
    max_min = None
    matriz_asignacion = None

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
            return True, "Esta balanceada"

    def balancear(self, donde_agregar):
        print(donde_agregar)
        for x in self.matriz:
            print(x)

        if donde_agregar[0] == False:
            if donde_agregar[1] == "Agregar Destino":

                for j in range(1, len(self.matriz), 1):

                    if j < len(self.matriz) - 2:
                        self.matriz[j].insert(len(self.matriz[0]) - 1, 0)
                    elif j == len(self.matriz) - 1:
                        self.matriz[0].insert(len(self.matriz[0]) - 1, "*")
                        self.matriz[j].insert(len(self.matriz[0]) - 1, donde_agregar[2])

                for x in self.matriz:
                    print(x)

            else:

                tmp = []

                for i in range(len(self.matriz[0])):

                    if i == 0:
                        tmp.append('*')
                    elif i < len(self.matriz[0]) - 2:
                        tmp.append(0)
                    elif i == len(self.matriz) - 1:
                        tmp.append(0)
                        tmp.append(donde_agregar[2])

                self.matriz.insert(len(self.matriz) - 1, tmp)

                for x in self.matriz:
                    print(x)



    def sol_factible_basica_inicial(self):

        self.matriz_asignacion = self.create_matriz(len(self.matriz)-2, len(self.matriz[0])-2)

        columna = 1
        j = 0
        i = 0

        for fila in range(1, len(self.matriz)-1 ,1):

            print("Fila: ", fila)

            tmp = None

            if self.matriz[fila][len(self.matriz[0])-1] < 1:
                # oferta - demanda
                tmp = [1000000000, self.matriz[len(self.matriz) - 1][columna]]
            elif self.matriz[fila][len(self.matriz[0])-1] > 0:
                tmp = [self.matriz[fila][len(self.matriz[0])-1], self.matriz[len(self.matriz) - 1][columna]]
            elif self.matriz[len(self.matriz) - 1][columna] < 1:
                tmp = [self.matriz[fila][len(self.matriz[0])-1], 1000000000]
            elif self.matriz[len(self.matriz) - 1][columna] > 0:
                tmp = [self.matriz[fila][len(self.matriz[0]) - 1], self.matriz[len(self.matriz) - 1][columna]]

            min_ = tmp.index(min(tmp))

            if min_ == 0:

                self.matriz_asignacion[j][i] = self.matriz[fila][len(self.matriz[0]) - 1]
                self.matriz[fila][len(self.matriz[0]) - 1] = 0

                self.matriz[len(self.matriz) - 1][columna] = self.matriz[len(self.matriz) - 1][columna] - self.matriz_asignacion[j][i]

                j = j+1
                continue

                #self.matriz[fila][columna] = self.matriz[fila][len(self.matriz[0]) - 1]

                #asignación
                # self.matriz[fila][columna] = self.matriz[fila][len(self.matriz[0]) - 1]
                # self.matriz[len(self.matriz) - 1][columna] = self.matriz[len(self.matriz) - 1][columna] - self.matriz[fila][len(self.matriz[0]) - 1]
                # if self.matriz[len(self.matriz) - 1][columna] == 0:
                #     columna = columna + 1
                #
                # #la oferta se hace cero
                # self.matriz[fila][len(self.matriz[0]) - 1] = 0

            else:

                self.matriz_asignacion[j][i] = self.matriz[len(self.matriz) - 1][columna]
                self.matriz[len(self.matriz) - 1][columna] = 0

                self.matriz[fila][len(self.matriz[0]) - 1] = self.matriz[fila][len(self.matriz[0]) - 1] - self.matriz_asignacion[j][i]

                i = i +1
                columna = columna +1
                continue
                #asignacion
                # self.matriz[fila][columna] = self.matriz[len(self.matriz) - 1][columna]
                #
                # self.matriz[fila][len(self.matriz[0]) - 1] = self.matriz[fila][len(self.matriz[0]) - 1] - self.matriz[len(self.matriz) - 1][columna]
                #
                # self.matriz[len(self.matriz) - 1][columna] = 0
                #
                # if self.matriz[fila][len(self.matriz[0]) - 1] == 0:
                #     continue


        print("SNW")
        for x in self.matriz_asignacion:
            print(x)



    def create_matriz(self, filas, columnas):
        matriz__ = []
        for i in range(filas):
            matriz__.append([])
            for j in range(columnas):
                matriz__[i].append(None)

        return matriz__



prueba = [ ["Origen\\Destino", 1,2,3,"Oferta"],
           [1,1,2,6,7], [2,0,4,2,12],
           [3,3,1,5,11], ["Demanda",10,10,7,None]]

en = Esquina_Noroeste(prueba, "Minimizar")

en.generar_matriz()
en.balancear(en.is_balancing())
en.sol_factible_basica_inicial()