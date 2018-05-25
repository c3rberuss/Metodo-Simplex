#!/usr/bin/python3
#-*- coding: utf-8 -*-

from sympy import Symbol
from fractions import Fraction
from decimal import Decimal

prueba = [{'func_obj': {'X2': 8.0, 'X1': 7.0, 'X4': 6.0, 'X3': 12.0}}, {'restric_1': {'desigualdad1': '>=', 'b1': 28.0, 'X3': 6.0, 'X2': 2.0, 'X1': 3.0, 'X4': 1.0}}, {'restric_2': {
    'X3': 5.0, 'desigualdad2': '=', 'X2': 3.0, 'X1': 2.0, 'X4': 2.0, 'b2': 35.0}}, {'restric_3': {'b3': 27.0, 'X3': 5.0, 'X2': 1.0, 'X1': 4.0, 'X4': 1.0, 'desigualdad3': '<='}}]


def penalizacion(data, max_min):

    data_original = data
    n = len(data)  # cantidad de funciones (objetiva y restricciones)
    indice_var = len(data[1]['restric_1']) - 2  # cantidad de variables
    funcion_objetiva = data[0]['func_obj']  # la función objetiva
    var_holgura = {}  # futuras variables de holgura
    var_arti = {}  # futuras variables artificiales
    M = Symbol('M')  # Variable M

    # se recorre cada una de las restricciones
    for i in range(1, n, 1):

        # se verifica el tipo de desigualdad
        if data[i]['restric_' + str(i)]['desigualdad' + str(i)] == '<=':

            # se agrega una variable de holgura
            var_holgura['X' + str(indice_var + 1)] = 1
            # se agrega la variable de holgura a la
            funcion_objetiva['X' + str(indice_var + 1)] = 0
                                                            # funcion objetiva

            # se agrega la variable de holgura a la restriccion
            data[i]['restric_' + str(i)].update({'X' + str(indice_var + 1): 1})

            indice_var += 1

        elif data[i]['restric_' + str(i)]['desigualdad' + str(i)] == '>=':

            # se agrega una variable de holgura
            var_holgura['X' + str(indice_var + 1)] = -1

            # se agrega la variable de holgura a la restriccion
            data[i]['restric_' +
                str(i)].update({'X' + str(indice_var + 1): -1})

            # se agrega la variable de holgura a la
            funcion_objetiva['X' + str(indice_var + 1)] = 0
                                                            # funcion objetiva
            indice_var += 1

            var_art_tmp = 'X' + str(indice_var + 1)
            var_arti[var_art_tmp] = 1

            data[i]['restric_' + str(i)].update({var_art_tmp: 1})

            if max_min == "Maximizar":
                funcion_objetiva[var_art_tmp] = -M
            else:
                funcion_objetiva[var_art_tmp] = M

            indice_var += 1

        elif data[i]['restric_' + str(i)]['desigualdad' + str(i)] == '=':

            var_art_tmp = 'X' + str(indice_var + 1)
            var_arti[var_art_tmp] = 1

            data[i]['restric_' + str(i)].update({'X' + str(indice_var + 1): 1})

            if max_min == "Maximizar":
                funcion_objetiva[var_art_tmp] = -M
            else:
                funcion_objetiva[var_art_tmp] = M

            indice_var += 1

        # print("restriccion_"+str(i)+": "+str(data[i]['restric_'+str(i)]))

    # print("func_obj: ant: ",funcion_objetiva)

    for x in range(len(funcion_objetiva)):
        if funcion_objetiva['X' + str(x + 1)]:
            funcion_objetiva['X' +
                str(x + 1)] = funcion_objetiva['X' + str(x + 1)] * -1

    funcion_objetiva['b'] = 0

    var_agregadas = list(var_arti.keys())
    for add in list(var_holgura.keys()):
        var_agregadas.append(add)

    # print("var_agregadas: ",var_agregadas)

    for i in range(1, n, 1):

        tm = list(data[i]['restric_' + str(i)].keys())
        # print("tm: ", tm)
        tm.remove('desigualdad' + str(i))
        tm.remove('b' + str(i))

        for var in var_agregadas:
            # print("var: ",var)

            if not var in tm:
                # print('variable: {0} --- agregada: {1}'.format(var, var_agregadas))
                data[i]['restric_' + str(i)][var] = 0

    # print("func_obj: act",funcion_objetiva)
    # print(var_holgura)
    # print(var_arti)
    # print(data[1],data[2],data[3])

    data[0]['func_obj'] = funcion_objetiva

    return data_original, data, var_holgura, var_arti


def generar_tabla(sistema, max_mini):

    filas = len(sistema[1]) + 1
    columnas = len(sistema[1][0]['func_obj']) + 1

    solucion = matriz(filas, columnas)

    for i in range(1,columnas,1):
        if i == columnas-1:
            solucion[0][i] = 'bi'
        else:
            solucion[0][i] = 'X'+str(i)
    
    for i in range(filas):
        if i == 0:
            solucion[i][0] = "Var Basic"
        elif i == filas-1:
            solucion[i][0] = 'Z'
        else:
            solucion[i][0] = 'X'
    
    for i in range(1,filas,1):
        res = None

        if i == filas-1:
            res = sistema[1][0]['func_obj']
        else:
            res = sistema[1][i]['restric_'+str(i)]

        for j in range(1, columnas, 1):
            
            if i == filas-1 and j == columnas-1:
                
                solucion[i][j] = res['b']

            elif j == columnas-1 and i < filas-1:
                solucion[i][j] = res['b'+str(i)]
            else:
                solucion[i][j] = res['X'+str(j)]
    
    for x in range(filas):
        print(solucion[x])

    return solucion

def solucion_basica_inicial(matriz,var_hol, var_art, max_min):
    filas = len(matriz) - 1
    columnas = len(matriz[1])

    pos_m = []

    z_tmp = matriz[filas][1:columnas-1]
    eme = False

    for x in range(columnas-2):
        
        if "M" in str(z_tmp[x]):
            eme = True
            pos_m.append(x+1)

    pos_m = sorted(pos_m)

    var_agregadas_pos = []

    for arti in var_art:
        var_agregadas_pos.append(matriz[0].index(arti))
    
    for hol in var_hol:
        var_agregadas_pos.append(matriz[0].index(hol))

    var_agregadas_pos = sorted(var_agregadas_pos)

    i = 1

    for columna in var_agregadas_pos:

        basic = False
        verdades = 0

        for fila in range(1, filas, 1):
            
            if matriz[fila][columna] >= 0:
                basic = True
                verdades+=1
        
        if basic and verdades >= 3:
            matriz[i][0] = matriz[0][columna]
            i = i +1
            basic = False
        

    filas_pivote = []
    

    print("filas: ",filas)
    print("Columnas: ",columnas)

    for fila in range(1, filas, 1):
        for columna in range(1, columna+1, 1):
            print("fila, columna: ", fila, columna)
            if matriz[fila][columna] == 1 and (columna in pos_m):
                filas_pivote.append(fila)
    
    print('filas pivote: ', filas_pivote)
    filas_pivote = sorted(filas_pivote)

    M = Symbol('M')


    for fila in filas_pivote:
        for columna in range(1, columnas, 1):
            if max_min == "Maximizar":
                matriz[filas][columna] = (matriz[fila][columna] * - M) + matriz[filas][columna]
            else:
                matriz[filas][columna] = (matriz[fila][columna] * M) + matriz[filas][columna]

    for x in range(filas+1):
        print(matriz[x])

    return matriz

def segmentar(fila):
    
    columnas = len(fila)
    items = []

    for columna in range(1, columnas, 1):
        #print("val z: ", matriz[filas][columna])

        if '+' in str(fila[columna]):
            
            print("+* : ",str(fila[columna]).replace('*M','').split())
            items.append(str(fila[columna]).replace('*M','').split()[0])

        elif '-' in str(fila[columna]):
            
            print("-* : ", str(fila[columna]).replace('*M','').split())
            items.append(str(fila[columna]).replace('*M','').split()[0])

        elif 'M' in str(fila[columna]):
            print("* : ",str(fila[columna]).replace('*M','').split())
            items.append(str(fila[columna]).replace('*M','').split()[0])
        else:
             items.append(str(fila[columna]))

    for item in range(len( items)):
        if items[item] == '-M':
            items[item] = '-1'
        elif items[item] == 'M':
            items[item] = '1'

        #items[item] = Fraction(items[item])

    print('lista_z_segmentada: ', items)

    return items


def var_entrada_salida(matriz, max_min):
    var_entrada = []  

    filas = len(matriz) - 1
    columnas = len(matriz[1])  

    for columna in range(1, columnas - 1, 1):
        print("val z: ", matriz[filas][columna])

        if '+' in str(matriz[filas][columna]):
            
            print("+* : ",str(matriz[filas][columna]).replace('*M','').split())
            var_entrada.append(str(matriz[filas][columna]).replace('*M','').split()[0])

        elif '-' in str(matriz[filas][columna]):
            
            print("-* : ", str(matriz[filas][columna]).replace('*M','').split())
            var_entrada.append(str(matriz[filas][columna]).replace('*M','').split()[0])

        elif 'M' in str(matriz[filas][columna]):
            print("* : ",str(matriz[filas][columna]).replace('*M','').split())
            var_entrada.append(str(matriz[filas][columna]).replace('*M','').split()[0])
        else:
            var_entrada.append(str(matriz[filas][columna]))

    print(var_entrada)

    for item in range(len( var_entrada)):
        
        if var_entrada[item] == '-M':
            var_entrada[item] = '-1'
        elif var_entrada[item] == 'M':
            var_entrada[item] = '1'
        
        var_entrada[item] = float(var_entrada[item])
    
    columna_var_entrada = 0

    if max_min == 'Maximizar':
        print("Maximizando")
        print(min(var_entrada))
        columna_var_entrada = var_entrada.index(min(var_entrada))+1
    else:
        print("Minimizando")
        print(max(var_entrada))
        columna_var_entrada = var_entrada.index(max(var_entrada))+1
    
    print('columna pivote: ', columna_var_entrada)

    pivot = {}
    tmp = []

    for restriccion in range(1, filas, 1):
        print("restriccion_entrada: ",matriz[restriccion])
        tmp.append( float(Fraction(matriz[restriccion][columnas-1])) / float(Fraction(matriz[restriccion][columna_var_entrada])))

    #revisar si es negativo o indeterminado (luego)

    pivot['columna'] = columna_var_entrada
    pivot['fila'] = tmp.index(min(tmp))+1
    pivote = matriz[pivot['fila']][pivot['columna']]

    print("pivote: ", matriz[pivot['fila']][pivot['columna']])

    for i  in range(1, columnas, 1):
        matriz[pivot['fila']][i] = str(Fraction(int(matriz[pivot['fila']][i]), int(pivote)))


    matriz[ pivot['fila']][0] = 'X'+str(pivot['columna'])

    for fila in range(1, filas+1, 1):

        factor = matriz[fila][pivot['columna']] * -1 

        for columna in range(1, columnas, 1):

            if fila != pivot['fila'] and fila != filas:

                print('fila ', matriz[fila])

                matriz[fila][columna] = str((Fraction(factor) * Fraction(matriz[pivot['fila']][columna])) + Fraction(matriz[fila][columna]) )

            elif fila == filas:

                matriz[fila][columna] = (factor * float(eval(matriz[pivot['fila']][columna]))) + matriz[fila][columna]
    
    for x in range(filas+1):
        print(matriz[x])

    return matriz

def condicion(lista, max_min):

    print("fila_z : ",lista)

    for i in range(len(lista)):
        
        if max_min == "Maximizar":
            if Fraction(lista[i]) < 0:
                return False
                break
        else:
            if Fraction(lista[i]) > 0:
                return False
                break

    return True

def simplex(data, max_min):
    var_entrada = []  

    filas = len(data) - 1
    columnas = len(data[1])  

    for columna in range(1, columnas - 1, 1):
        print("val z: ", data[filas][columna])

        if '+' in str(data[filas][columna]):
            
            print("+* : ",str(data[filas][columna]).replace('*M','').split())
            var_entrada.append(str(data[filas][columna]).replace('*M','').split()[0])

        elif '-' in str(data[filas][columna]):
            
            print("-* : ", str(data[filas][columna]).replace('*M','').split())
            var_entrada.append(str(data[filas][columna]).replace('*M','').split()[0])

        elif 'M' in str(data[filas][columna]):
            print("* : ",str(data[filas][columna]).replace('*M','').split())
            var_entrada.append(str(data[filas][columna]).replace('*M','').split()[0])
        else:
            var_entrada.append(str(data[filas][columna]))

    print(var_entrada)

    for item in range(len( var_entrada)):
        
        if var_entrada[item] == '-M':
            var_entrada[item] = '-1'
        elif var_entrada[item] == 'M':
            var_entrada[item] = '1'
        
        var_entrada[item] = Fraction(var_entrada[item])
    
    columna_var_entrada = 0

    if max_min == 'Maximizar':
        print("Maximizando")
        print(min(var_entrada))
        columna_var_entrada = var_entrada.index(min(var_entrada))+1
    else:
        print("Minimizando")
        print(max(var_entrada))
        columna_var_entrada = var_entrada.index(max(var_entrada))+1
    
    print('columna pivote: ', columna_var_entrada)

    pivot = {}
    tmp = []

    for restriccion in range(1, filas, 1):
        print("restriccion_entrada: ", data[restriccion])
        
        tmp.append(str(Fraction(Fraction(data[restriccion][columnas-1]) / Fraction(data[restriccion][columna_var_entrada]))))

    #revisar si es negativo o indeterminado (luego)

    print("tmp_ : ",tmp)
    pivot['columna'] = columna_var_entrada
    pivot['fila'] = tmp.index(min(tmp))
    pivote = data[pivot['fila']][pivot['columna']]

    print("pivote: ", data[pivot['fila']][pivot['columna']])

    for i  in range(1, columnas, 1):
        data[pivot['fila']][i] = str(Fraction(Fraction(data[pivot['fila']][i]), Fraction(str(pivote))))


    data[pivot['fila']][0] = 'X'+str(pivot['columna'])

    for fila in range(1, filas+1, 1):

        if fila == filas:
            print("fila: ", fila) 
            factor = data[fila][pivot['columna']] * -1
        else:
            factor = str(Fraction(data[fila][pivot['columna']]) * Fraction(-1, 1))

        print("factor: ", factor)

        for columna in range(1, columnas, 1):

            if fila != pivot['fila'] and fila != filas:

                print('fila ', data[fila])

                data[fila][columna] = str((Fraction(factor) * Fraction(data[pivot['fila']][columna])) + Fraction(data[fila][columna]) )



            elif fila == filas:
                M = Symbol('M')

                print('1: ', factor)
                print('2: ', Fraction(data[pivot['fila']][columna]))
                print('3: ', data[fila][columna])

                list_factor = str(factor).replace('*M', ',').split(',')
                
                for i in range(len(list_factor)):
                    list_factor[i] = list_factor[i].replace(' ', '')
                    

                list_columna_0 = str(data[fila][columna]).replace('*M', ',').split(',')

                if len(list_columna_0) == 1:
                    list_columna_0.append('0')

                for i in range(len(list_columna_0)):
                    list_columna_0[i] = list_columna_0[i].replace(' ', '')

                multiplicador = Fraction(data[pivot['fila']][columna])
                elemento_r = []

                print("lista_factor: ", list_factor)
                print("lista_eliminar: ", list_columna_0)
                print("Pivote: ", multiplicador)

                for i in range(len(list_factor)):

                    if i == 1:
                        elemento_r.append(str((Fraction(list_factor[i]) * multiplicador) + Fraction(list_columna_0[i])))
                    else:
                        elemento_r.append(str(round((float(list_factor[i]) * multiplicador) + float(list_columna_0[i]))))
                   
                    
                print("elementos_obtenidos: ", elemento_r)

                data[fila][columna] = str((float(elemento_r[0]) * M)+(Fraction(elemento_r[1])))

                #data[fila][columna] = (factor * Fraction(data[pivot['fila']][columna])) + data[fila][columna]
                print('fila_z_post: ', data[fila][columna])

    return data

    for x in range(filas+1):
        print(data[x])

def matriz(filas, columnas):
    matriz = []

    for i in range(filas):
        matriz.append([])
        for j in range(columnas):
            matriz[i].append(None)

    return matriz

penali = penalizacion(prueba, "Minimizar")
tabla = generar_tabla(penali, "Minimizar")
sol_ini = solucion_basica_inicial(tabla, penali[2], penali[3], "Minimizar")
sol2 = var_entrada_salida(sol_ini, "Minimizar")
lista_seg = segmentar(sol2[len(sol2)-1])
print("Solución: ",condicion(lista_seg, "Minimizar"))

sol3 = simplex(sol2, "Minimizar")
lista_seg = segmentar(sol3[len(sol3)-1])
print("Solución: ", condicion(lista_seg, "Minimizar"))

sol4 = simplex(sol3, "Minimizar")
lista_seg = segmentar(sol3[len(sol3)-1])
print("Solución: ",condicion(lista_seg, "Minimizar"))


