#!/usr/bin/python3
#-*- coding: utf-8 -*-

from reportlab.lib import colors
from reportlab.lib.pagesizes import legal, A2 , inch, landscape, portrait
from reportlab.pdfgen import textobject
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas

from fractions import Fraction
from copy import deepcopy
from sympy import Symbol
import os

class saveReport():

    var_holgura = None
    var_artificiales = None
    f_objetivo = None
    sar = None
    f_objetivo_n = None
    nr = None
    respuesta = None
    iteraciones = None
    mensaje = None

    def __init__(self, restricciones_, respuesta_, iteraciones_, mensaje_):

        self.mensaje = mensaje_

        if 'V.A' in restricciones_:
            self.var_holgura = restricciones_[ restricciones_.index("V.H")+1: restricciones_.index("V.A")]
            self.var_artificiales = restricciones_[restricciones_.index("V.A")+1: ]
        else:
            self.var_holgura = restricciones_[ restricciones_.index("V.H")+1 : ]

        #print("Variables de Holgura: ", self.var_holgura)
        #print("Variables Artificiales: ", self.var_artificiales)

        self.respuesta = respuesta_
        #print(respuesta_)

        self.f_objetivo = restricciones_[0]
        print(self.f_objetivo)

        self.sar = restricciones_[ restricciones_.index('S.A.R')+1: restricciones_.index('N.R') ]
        self.nr = restricciones_[ restricciones_.index('N.R')+1: restricciones_.index('V.H')-1]

        print("SAR: ", self.sar)
        print("NR: ",self.nr)

        self.f_objetivo_n = restricciones_[restricciones_.index('V.H')-1: restricciones_.index('V.H')]

        print("Nueva: ", self.f_objetivo_n)

        self.iteraciones = iteraciones_

        self.mejorar_datos()

    def mejorar_datos(self):
        tabla_tmp = deepcopy(self.iteraciones)
        M = Symbol('M')

        for tabla in range(len(self.iteraciones)):
            for fila in range(1, len(self.iteraciones[0]), 1):
                for columna in range(1, len(self.iteraciones[0][0]),1):
                    
                    if not "M" in str(tabla_tmp[tabla][fila][columna]):
                        tabla_tmp[tabla][fila][columna] = str(Fraction(str(tabla_tmp[tabla][fila][columna])).limit_denominator(1000))
                    else:
                        tmp = str(tabla_tmp[tabla][fila][columna]).replace('*M', ',').split(',')
                        
                        if "-M" in tmp[0]:
                            tmp[0] = -1
                        elif "M" in tmp[0]:
                            tmp[0] = 1
                        
                        for i in range(len(tmp)):
                            tmp[i] = str(tmp[i]).replace(' ', '')
                            if tmp[i] == '':
                                tmp[i] = '0'

                        if len(tmp) > 1:
                            tabla_tmp[tabla][fila][columna] = str( (Fraction(tmp[0]).limit_denominator(1000)*M) + Fraction(tmp[1]).limit_denominator(1000) ).replace('*', '') 
                        else:
                            tabla_tmp[tabla][fila][columna] = str( (Fraction(tmp[0]).limit_denominator(1000)*M)).replace('*', '')
                        
                        print("***: ", tabla_tmp[tabla][fila][columna])
        
        self.iteraciones = tabla_tmp



    def crear_pdf(self):
    
        header = None

        doc = SimpleDocTemplate(str(os.environ['HOME'])+"/Solucion_Simplex.pdf", pagesize=landscape(A2))
        elements = []

        styleSheet = getSampleStyleSheet()

        header_ = Paragraph("<b><font color=red >"+str(self.f_objetivo).replace('-', ' - ')+"</font></b>", styleSheet['Heading2'])
        texto1 = Paragraph("<b>S.A.R</b>", styleSheet['Heading3'])
        
        elements.append(header_)
        elements.append(texto1)

        for restriccion in self.sar:
            a = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;"+str(restriccion).replace('-', ' - '), styleSheet['Heading3'])
            elements.append(a)

        space = Paragraph("<b>\n</b>", styleSheet['Heading3'])
        elements.append(space)
        elements.append(space)

        for restriccion in self.nr:
            a = Paragraph( str(restriccion).replace('-', ' - '), styleSheet['Heading3'])
            elements.append( a )        
        
        elements.append( Paragraph(str(self.f_objetivo_n[0]).replace('-', ' - ').replace('*',''), styleSheet['Heading3']) )        

        elements.append(Paragraph("<b>\n</b>", styleSheet['Heading3']))
        
        elements.append(Paragraph("<b>Variables de Holgura: </b>" +str(self.var_holgura), styleSheet['Heading3']))
        
        elements.append(Paragraph("<b>Variables Artificiales: </b>" +str(self.var_artificiales), styleSheet['Heading3']))


        elements.append(Paragraph("<b><font color=red >" + str(self.mensaje['mensaje']) +"</font></b>", styleSheet['Heading3']))

        for x in self.respuesta:
            elements.append(Paragraph("<b>" +str(x)+ "</b>", styleSheet['Heading3']))

        elements.append(Paragraph("",styleSheet['Heading1']))

        for iteracion in self.iteraciones:
            t=Table(iteracion,style=[
                    ('GRID',(0,0),(-1,-1),1,colors.black),
                    ('BACKGROUND', (0, 0), (0, -1), colors.blue),
                    ('TEXTCOLOR',(0,0),(-1,0),colors.white),
                    ('TEXTCOLOR',(0,0),(0,-1),colors.white),
                    ('SIZE', (0,0), (-1,-1), 11),
                    ('VALIGN',(0,0),(-1,-1),'TOP'),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.red),
                    ('SIZE', (1,1),(-1,-1), 11)
            ])

            for i in range(len(iteracion)):
                t._argH[i]=0.3*inch

            elements.append(t)
            elements.append(Paragraph("<b>\n</b>", styleSheet['Heading3']))
            elements.append(Paragraph("<b>\n</b>", styleSheet['Heading3']))

        """t._argW[0]=0.6*inch
        t._argW[1]=1.9*inch
        t._argW[2]=1.9*inch
        t._argW[3]=1.9*inch
        t._argW[4]=2.5*inch"""

        elements.append(Paragraph("<b>\n</b>", styleSheet['Heading3']))
        elements.append(Paragraph("<b>\n</b>", styleSheet['Heading3']))

        elements.append(Paragraph("<b><font color=red >" + str(self.mensaje['mensaje']) +"</font></b>", styleSheet['Heading3']))

        for x in self.respuesta:
            elements.append(Paragraph("<b>" +str(x)+ "</b>", styleSheet['Heading3']))
        
        # write the document to disk
        doc.build(elements)
    
    def mostrar_pdf(self):
        os.system("xdg-open {}/Solucion_Simplex.pdf".format(os.environ['HOME']))