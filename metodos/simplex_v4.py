#!/usr/bin/python3
#-*- coding: utf-8 -*-

from sympy import Symbol
from fractions import Fraction
from decimal import Decimal

prueba = [{'func_obj': {'X2': 8.0, 'X1': 7.0, 'X4': 6.0, 'X3': 12.0}}, {'restric_1': {'desigualdad1': '>=', 'b1': 28.0, 'X3': 6.0, 'X2': 2.0, 'X1': 3.0, 'X4': 1.0}}, {'restric_2': {
    'X3': 5.0, 'desigualdad2': '=', 'X2': 3.0, 'X1': 2.0, 'X4': 2.0, 'b2': 35.0}}, {'restric_3': {'b3': 27.0, 'X3': 5.0, 'X2': 1.0, 'X1': 4.0, 'X4': 1.0, 'desigualdad3': '<='}}]

prueba2 = [{'func_obj': {'X2':4, 'X1': 5.0, 'X3': 5}}, {'restric_1': {'desigualdad1': '<=', 'b1': 20, 'X3': 2.0, 'X2': 5.0, 'X1': 2.0 }}, {'restric_2': {
    'X3': 1.0, 'desigualdad2': '<=', 'X2': 6.0, 'X1': 3.0, 'b2': 18.0}}]

prueba3 = [{'func_obj': {'X2': 8.0, 'X3': 7.0, 'X1': 5.0}}, {'restric_1': {'b1': 30.0, 'X2': 3.0, 'X3': 3.0, 'desigualdad1': '>=', 'X1': 3.0}}, {'restric_2': {'X2': 2.0, 'X3': 5.0, 'b2': 30.0, 'desigualdad2': '>=', 'X1': 0.0}}, {'restric_3': {'desigualdad3': '=', 'X2': 4.0, 'X3': 0.0, 'b3': 24.0, 'X1': 4.0}}]

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
                funcion_objetiva[var_art_tmp] = -1.0 * M
            else:
                funcion_objetiva[var_art_tmp] = 1.0 * M

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
    
    """for x in range(filas):
        print(solucion[x])"""

    return solucion


def solucion_basica_inicial(matriz,var_hol, var_art, max_min):
    filas = len(matriz) - 1
    columnas = len(matriz[1])

    if len(var_art) != 0:
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

        print("Variables de Holgura: ", var_hol)
        
        for hol in var_hol:
            if float(var_hol[hol]) > 0:
                var_agregadas_pos.append(matriz[0].index(hol))

        var_agregadas_pos = sorted(var_agregadas_pos)

        print("VARIABLES POSIBLES: ", var_agregadas_pos)

        i = 1

        for columna in var_agregadas_pos:

            basic = False
            verdades = 0

            for fila in range(1, filas, 1):
                
                if matriz[fila][columna] >= 0:
                    basic = True
                    verdades+=1
            
            if basic and verdades >= len(var_agregadas_pos):
                matriz[i][0] = matriz[0][columna]
                i = i +1
                basic = False
            

        filas_pivote = []
        

        """print("filas: ",filas)
        print("Columnas: ",columnas)"""

        for fila in range(1, filas, 1):
            for columna in range(1, columna+1, 1):
                #print("fila, columna: ", fila, columna)
                if matriz[fila][columna] == 1 and (columna in pos_m):
                    filas_pivote.append(fila)
        
        #print('filas pivote: ', filas_pivote)
        filas_pivote = sorted(filas_pivote)

        M = Symbol('M')


        for fila in filas_pivote:
            for columna in range(1, columnas, 1):
                if max_min == "Maximizar":
                    matriz[filas][columna] = (matriz[fila][columna] * - M) + matriz[filas][columna]
                else:
                    matriz[filas][columna] = (matriz[fila][columna] * M) + matriz[filas][columna]

    else:
        
        var_agregadas_pos = []
        
        for hol in var_hol:
            var_agregadas_pos.append(matriz[0].index(hol))

        var_agregadas_pos = sorted(var_agregadas_pos)
        print("VARIABLES BASICAS:::::: ", var_agregadas_pos)

        i  = 0

        for x in range(1, len(matriz)-1, 1):
            matriz[x][0] = 'X'+str(var_agregadas_pos[i])
            i+=1


    print("Matriz: ")

    for x in range(filas+1):
        print(matriz[x])

    return matriz


def matriz(filas, columnas):
    matriz = []

    for i in range(filas):
        matriz.append([])
        for j in range(columnas):
            matriz[i].append(None)

    return matriz

def var_entrada(matriz, max_min):
    var_entrada = []  

    filas = len(matriz) - 1
    columnas = len(matriz[1])  

    #if 'M' in str(matriz[filas][columnas-1]):
    for columna in range(1, columnas - 1, 1):
        #print("val z: ", matriz[filas][columna])
        if '+' in str(matriz[filas][columna]):
            
            #print("+* : ",str(matriz[filas][columna]).replace('*M','').split())
            var_entrada.append(str(matriz[filas][columna]).replace('*M','').split()[0])

        elif '-' in str(matriz[filas][columna]):
            
            #print("-* : ", str(matriz[filas][columna]).replace('*M','').split())
            var_entrada.append(str(matriz[filas][columna]).replace('*M','').split()[0])
        elif 'M' in str(matriz[filas][columna]):
            #print("* : ",str(matriz[filas][columna]).replace('*M','').split())
            var_entrada.append(str(matriz[filas][columna]).replace('*M','').split()[0])
        else:
            var_entrada.append(str(matriz[filas][columna]))

        #print("VARIABLES", var_entrada)

    for item in range(len( var_entrada)):
            
        if var_entrada[item] == '-M':
            var_entrada[item] = '-1'
        elif var_entrada[item] == 'M':
            var_entrada[item] = '1'
        
        var_entrada[item] = float(var_entrada[item])
    

        """else:
        for columna in range(1, columnas - 1, 1):
            var_entrada.append(matriz[filas][columna])"""

    #print("VARIABLES", var_entrada)

    columna_var_entrada = 0

    if max_min == 'Maximizar':
        print("Maximizando")
        #print(min(var_entrada))
        columna_var_entrada = var_entrada.index(min(var_entrada))+1
    else:
        print("Minimizando")
        #print(max(var_entrada))
        columna_var_entrada = var_entrada.index(max(var_entrada))+1

    pivot = {}
    tmp = []

    for restriccion in range(1, filas, 1):
        """print("restriccion_entrada: ",matriz[restriccion])
        tmp.append(matriz[restriccion][columnas-1] / matriz[restriccion][columna_var_entrada])"""

        if matriz[restriccion][columna_var_entrada] > 0:
            tmp.append(matriz[restriccion][columnas-1] / matriz[restriccion][columna_var_entrada])
        elif matriz[restriccion][columna_var_entrada] < 0:
            tmp.append(100000)
        elif float(matriz[restriccion][columna_var_entrada]) == 0:
            tmp.append(100000)

    #revisar si es negativo o indeterminado (luego)

    pivot['columna'] = columna_var_entrada
    pivot['fila'] = tmp.index(min(tmp))+1
    pivote = matriz[pivot['fila']][pivot['columna']]

    print("Pivote: ", pivote)
    return pivot

def var_salida(matriz, pivote):
    
    matriz[pivote['fila']][0] = matriz[0][pivote['columna']]

    """for x in range(len(matriz)):
        print(matriz[x])"""

    return matriz

def reducir_fila_pivote(matriz, pivote_data):
    
    pivote = matriz[pivote_data['fila']][pivote_data['columna']]

    for columna in range(1, len(matriz[1]), 1):
        matriz[pivote_data['fila']][columna] = matriz[pivote_data['fila']][columna] / pivote

    for x in range(len(matriz)):
        print(matriz[x])

    return matriz

def nueva_solucion(matriz, pivote, var_hol, var_art):
    
    pivote_fila = 0
    factor = 0

    for restriccion in range(1, len(matriz), 1):
        
        pivote_fila = matriz[restriccion][pivote['columna']] * -1

        """print("Pivote_fila: ", pivote_fila)
        print('Fila a Eliminar: ', matriz[restriccion])"""

        for columna in range(1, len(matriz[1]), 1):
            
            if restriccion != pivote['fila'] and restriccion != len(matriz)-1:
                
                """print("pivote_fila: ", pivote_fila)
                print("matriz1: ", matriz[pivote['fila']][columna])
                print("Valor anterior: ",matriz[restriccion][columna])"""
                matriz[restriccion][columna] = (float(pivote_fila) * float(matriz[pivote['fila']][columna])) +  float(matriz[restriccion][columna])

                #print("resultado: ",matriz[restriccion][columna])
            
            elif restriccion == len(matriz)-1:
                #aqui van cuando lleva a la funcion z

                lista_factor_eliminativo = str(pivote_fila).replace('*M', ',').split(',')
                tiene_m = 'M' in str(pivote_fila)
                
                for i in range(len(lista_factor_eliminativo)):
                    lista_factor_eliminativo[i] = lista_factor_eliminativo[i].replace(' ', '')

                #print("Lista*1 original: ", lista_factor_eliminativo)

                if len(lista_factor_eliminativo) == 1 :
                    lista_factor_eliminativo.append('0')

                #print("Lista*1 ceros agregados: ", lista_factor_eliminativo)
                
                if '' in lista_factor_eliminativo and len(var_art) > 0:
                    lista_factor_eliminativo[lista_factor_eliminativo.index('')] = '0'

                #print("Lista*1 espacios sustituidos: ", lista_factor_eliminativo)

                #tiene_m = 'M' in str(matriz[restriccion][columna])
                #print("Tiene M: ", matriz[restriccion][columna])

                lista_fila_eliminar = str(matriz[restriccion][columna]).replace('*M', ',').split(',')

                if len(lista_fila_eliminar) == 1:
                    lista_fila_eliminar.append('0')

                for i in range(len(lista_fila_eliminar)):
                    lista_fila_eliminar[i] = lista_fila_eliminar[i].replace(' ', '')

                if '' in lista_fila_eliminar and len(var_art) > 0:
                    lista_fila_eliminar[lista_fila_eliminar.index('')] = '0'
                
                for i in range(len(lista_fila_eliminar)):
                    if '-M' in lista_fila_eliminar[i]:
                        lista_fila_eliminar[i] = lista_fila_eliminar[i].replace('-M', '-1')
                    elif 'M' in lista_fila_eliminar[i]:
                        lista_fila_eliminar[i] = lista_fila_eliminar[i].replace('M', '1')

                #print("Lista*2 : ", lista_fila_eliminar)
                
                #multiplicador = str( matriz[pivote['fila']][columna] ).replace('*M', ',').split(',')
                multiplicador = matriz[pivote['fila']][columna]

                """print("*****************************************************")
                print("Multiplicador anterior: ", multiplicador)
                print("*****************************************************")"""

                """if len(multiplicador) == 1:
                    multiplicador.append('0')
                
                for i in range(len(multiplicador)):
                    multiplicador[i] = multiplicador[i].replace(' ', '')
                
                if '' in multiplicador:
                    multiplicador[multiplicador.index('')] = '0'"""

                elemento_r = []

                """print("=================================================")
                print("lista_eliminativo: ", lista_factor_eliminativo)
                print("multiplicador: ", multiplicador)
                print("lista_eliminar: ", lista_fila_eliminar)
                print("=================================================")"""

                for i in range(len(lista_factor_eliminativo)):

                    elemento_r.append((float(lista_factor_eliminativo[i]) * float(multiplicador) ) + float(lista_fila_eliminar[i]))

                #print("elementos_obtenidos: ", elemento_r)

                M = Symbol('M')

                a = elemento_r[0]
                
                if tiene_m:
                    a = eval("a*M") # a +"*" +str(M)
                    
                b = elemento_r[1]

                """if b > 0 and len(var_art) > 0:
                    b = "+"+b"""

                matriz[restriccion][columna] =  a + b

        """for columna in range(1, len(matriz[0]), 1):
        
        element = matriz[len(matriz)-1][columna]

        print("elemento: ", element)
        print("n: ", len(element))

        if len(element) > 1:
            matriz[len(matriz)-1][columna] = str(matriz[len(matriz)-1][columna])[0:len(element)-1]    """  
    
    """for x in range(len(matriz)):
        print(matriz[x])"""

    return matriz


def nueva_solucion_v2(matriz, pivote, var_hol, var_art):
    
    pivote_fila = 0
    pivote_ = 0

    for restriccion in range(1, len(matriz), 1):
        
        pivote_fila = matriz[restriccion][pivote['columna']] * -1

        for variable in range(1, len(matriz[1]), 1):
            pivote_ = matriz[pivote['fila']][variable]

            if restriccion != pivote['fila']:
                
                eliminar = matriz[restriccion][variable]

                matriz[restriccion][variable] = (pivote_fila * pivote_) + eliminar
    
    return matriz

def condicion(lista, max_min):
    
    print("fila_z : ",lista)

    for i in range(1, len(lista), 1):
        
        if max_min == "Maximizar":
            
            if 'M' in str(lista[i]):
                #print('Elemento maximizar M: ', str(lista[i]).replace('*M', ',').split(',')[0])
                if Fraction(str(lista[i]).replace('*M', ',').split(',')[0]) < 0:
                    return False
                    break                   
            else:
                #print('Elemento maximizar: ', lista[i])
                if lista[i] < 0:
                    return False
                    break

        else:
            if 'M' in str(lista[i]):
                
                #print('Elemento minimizar M: ', str(lista[i]).replace('*M', ',').split(',')[0])
                if Fraction(str(lista[i]).replace('*M', ',').split(',')[0]) > 0:
                    return False
                    break                   
            else:
                #print('Elemento minimizar: ', lista[i])
                if lista[i] > 0:
                    return False
                    break

    return True


def condicion_v2(lista, max_min):

    print("fila_z_inicial: ", lista)
    elemento = lista[len(lista)-1]
    
    tmp = []

    for item in lista:
        
        if 'M' in str(item) and item != 'Z':
            a = str(item).replace('*M', ',').split(',')
            
            print("Elementos seccionados: ", a)

            if '' in a:
                n = a.index('')
                a[n] = '0'

            if 'e' in a[0]:
                tmp.append(float(a[1].replace(' ', '')))
            elif a[0] == '-M':
                tmp.append(float(a[0].replace('-M', '-1.0')))
            elif a[0] == 'M':
                tmp.append(float(a[0].replace('M', '1.0')))
            else:
                tmp.append(float(a[0].replace(' ', '')))
                

            print("Elementos seccionados nuevos: ", a)

            
        
        elif not 'X' in str(item) and not 'Z' in str(item):
            tmp.append(float(item))
            print("No tiene M", item)
    
    print('Seleccionados: ', tmp)

    for i in range(len(tmp)-1):
            
        if max_min == "Maximizar":
            print("-*: ", tmp[i])
            if tmp[i] < 0:
                
                return False
                break
        else:
            print("-*: ", tmp[i])

            if tmp[i] > 0:
                return False
                break

    return True


def depurar_nueva_solucion(matriz):
    
    M = Symbol('M')
    fila_z = matriz[len(matriz)-1]
    fila_z = fila_z[1:]
    print("DEPURAR: ", fila_z)

    tmp = []

    for item in fila_z:
        
        if 'M' in str(item):
            a = str(item).replace('*M', ',').split(',')
            print("Elemento A: ", a)
            
            b = 0

            if '' in a:
                a[a.index('')] = '0'

            for i in range(len(a)):
                
                a[i] = a[i].replace(' ', '')

                if 'e' in a[i]:
                    a[i] = round(float(a[i]))
                else:
                    a[i] = eval(a[i])

            if len(a) < 2:
                print("MENOR: ", a)
                if -M in a or M in a:
                    a.append(0)
                    print("NUEVA: ",a)
            
            tmp.append(a)
        else:
            tmp.append([0, eval(str(item))])

    
    final = []

    for item in tmp:
        
        if len(item) == 2:
            if str(item[0]) != 'M' and str(item[0]) != "-M":
                final.append( (item[0]*M)+item[1]  )
            else:
                final.append( (item[0])+item[1]  )
        else:
            final.append(item)

    final.insert(0, 'Z')

    matriz[len(matriz)-1] = final

    print("DEPURAR NUEVA: ", final)
    return matriz




def simplex(data, max_min):
    
    penali = penalizacion(data, max_min)
    tabla = generar_tabla(penali, max_min)
    sol_ini = solucion_basica_inicial(tabla, penali[2], penali[3], max_min)

    encontrar_nueva_solucion = False

    while not encontrar_nueva_solucion:
        pivote = var_entrada(sol_ini, max_min)
        sol_ini = var_salida(sol_ini, pivote)
        sol_ini = reducir_fila_pivote(sol_ini, pivote)

        sol_ini = nueva_solucion_v2(sol_ini, pivote, penali[2], penali[3])
        sol_ini = depurar_nueva_solucion(sol_ini)

        print(" NUEVA SOLUCION ".center(100, "="))
        for x in sol_ini:
            print(x)


        encontrar_nueva_solucion = condicion_v2(sol_ini[len(sol_ini)-1], max_min)

    print(" Solucion Optima ".center(100, '='))

    z = sol_ini[len(sol_ini)-1][len(sol_ini[0])-1]

    tmp = []

    if 'M' in str(z):
        tmp = str(z).replace('*M', ',').split(',')
        tmp[0] = tmp[0].replace(' ', '')
        tmp[1] = tmp[1].replace(' ', '')

        if 'e' in tmp[0]:
            tmp[0] = round(float(tmp[0]))

        M = Symbol('M')

        z = (float(tmp[0]) * M) + float(tmp[1])

        sol_ini[len(sol_ini)-1][len(sol_ini[0])-1] = z

    respuesta = []

    for i in range(1, len(sol_ini), 1):
        respuesta.append(sol_ini[i][0] + ' = ' + str(Fraction(str(sol_ini[i][len(sol_ini[0])-1])).limit_denominator(1000)))
        print( sol_ini[i][0] + ' = ' + str(Fraction(str(sol_ini[i][len(sol_ini[0])-1])).limit_denominator(1000)))

    return respuesta
#simplex(prueba2, "Maximizar")

"""pivote = var_entrada(nueva_sol, "Maximizar")
nueva_sol = var_salida(nueva_sol, pivote)
nueva_sol = reducir_fila_pivote(nueva_sol, pivote)

sol_nueva = nueva_solucion(nueva_sol, pivote, penali[2], penali[3])

print()"""


#max_min = "Maximizar"
max_min = "Minimizar"

prueba4 = [{'func_obj': {'X3': 7.0, 'X1': 4.0, 'X2': 6.0, 'X5': 9.0, 'X4': 5.0}}, {'restric_1': {'X3': 4.0, 'b1': 20.0, 'X1': 1.0, 'X2': 3.0, 'desigualdad1': '>=', 'X5': 7.0, 'X4': 5.0}}, {'restric_2': {'X3': 7.0, 'desigualdad2': '<=', 'b2': 15.0, 'X1': 0.0, 'X2': 6.0, 'X5': 0.0, 'X4': 8.0}}, {'restric_3': {'X3': 0.0, 'b3': 30.0, 'X1': 7.0, 'X2': 8.0, 'X5': 9.0, 'X4': 7.0, 'desigualdad3': '='}}, {'restric_4': {'X3': 1.0, 'b4': 20.0, 'desigualdad4': '<=', 'X1': 7.0, 'X2': 2.0, 'X5': 8.0, 'X4': 0.0}}]

#simplex(prueba3, max_min)

"""penali = penalizacion(prueba3, max_min)
tabla = generar_tabla(penali, max_min)
sol_ini = solucion_basica_inicial(tabla, penali[2], penali[3], max_min)

pivote = var_entrada(sol_ini, max_min)
sol_ini = var_salida(sol_ini, pivote)
sol_ini = reducir_fila_pivote(sol_ini, pivote)

print(" PRIMERA ITERACION".center(100, "*"))
sol_ini = nueva_solucion_v2(sol_ini, pivote, penali[2], penali[3])

pivote = var_entrada(sol_ini, max_min)
sol_ini = var_salida(sol_ini, pivote)
sol_ini = reducir_fila_pivote(sol_ini, pivote)


print(" SEGUNDA ITERACION".center(100, "*"))
sol_ini = nueva_solucion_v2(sol_ini, pivote, penali[2], penali[3])

pivote = var_entrada(sol_ini, max_min)
sol_ini = var_salida(sol_ini, pivote)
sol_ini = reducir_fila_pivote(sol_ini, pivote)

print(" TERCERA ITERACION".center(100, "*"))
sol_ini = nueva_solucion_v2(sol_ini, pivote, penali[2], penali[3])

pivote = var_entrada(sol_ini, max_min)
sol_ini = var_salida(sol_ini, pivote)
sol_ini = reducir_fila_pivote(sol_ini, pivote)

print(" CUARTA ITERACION".center(100, "*"))
sol_ini = nueva_solucion_v2(sol_ini, pivote, penali[2], penali[3])

print(condicion_v2(sol_ini[len(sol_ini)-1], max_min))


"""