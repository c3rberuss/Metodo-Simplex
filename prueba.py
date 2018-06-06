#!/usr/bin/python3
#-*- coding: utf-8 -*-

def matriz(filas, columnas):
    matriz = []

    for i in range(filas):
        matriz.append([])
        for j in range(columnas):
            matriz[i].append(None)

    return matriz


from sympy import Symbol, Max, Min, Poly

from fractions import Fraction


M = Symbol('M')

poli1 = str((Fraction(3, 8)*M))

n = poli1.find('*M')

poli1 = (poli1[0:n] + poli1[n+2:])

poli2 = str((Fraction(1, 6)*M) + 5)

n2 = poli2.find('*M')
poli2 = '+' in poli2

M = 1
print(eval(poli1))
print(poli2)

lista = ["X2", 'X1', 'X3']


print(sorted(lista))


n = Fraction('1/5')

print(n * Fraction(1.5))

M = Symbol('M', real=True)



a = '-2/3'
b = '3/2'

lista = ["X1", "X2", "X3"]
lista2 = ["X4", "X5", "X1"]

print( max(lista) )

"""print(str(a).replace('*M', '').split())
#print(Fraction('3*M/6'))

print(lista*2)"""

if not lista2 in lista:
    print("SI")

a = 12 * M


print(float("6.2"))

print("hola\ncomo estas?\nBien :)")

lista = [1, 2, 3]

print(sum(lista))

if -4.251515215e-17 > 0:
    print("A huevo, es mayor")