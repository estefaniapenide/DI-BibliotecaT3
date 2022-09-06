from reportlab.pdfgen import canvas
import os
import var
from PyQt5 import QtSql
from datetime import datetime

#IMPRIMIR INFORMES
class Imprimir():

    def pie(self):
        '''Escribe el pie de un informe indicando la página del mismo y la fecha en la que se ha generado'''

        try:
            var.rep.line(45,45,525,45)
            fecha= datetime.today()
            fecha = fecha.strftime('%d.%m.%Y %H.%M.%S')
            var.rep.setFont('Helvetica-Oblique',size=7)
            var.rep.drawString(460,35,str(fecha))
            var.rep.drawString(275, 35, str('Página %s' % var.rep.getPageNumber()))
        except Exception as error:
            print('Error pie informe: %s' % str(error))


    def cabecera(titulo):
        '''Escribe la cebecera de un informe donde se indican los datos
         "BIBLIOTECA IES TEIS, Avenida de Galicia 101- Vigo, 8886 12 04 04"
         más el título del listado correspondiente que se pasa por parámetro'''
        try:
            var.rep.setTitle('INFORMES %s' % titulo)
            var.rep.setAuthor('IES Teis')
            var.rep.setFont('Helvetica', size=10)
            var.rep.line(45,810,525,810)
            var.rep.line(45,745,525,745)
            textnom='BIBLIOTECA IES TEIS'
            textdir='Avenida Galicia, 101 - Vigo'
            texttlfo='886 12 04 04'
            var.rep.drawString(50,790, textnom)
            var.rep.drawString(50,775, textdir)
            var.rep.drawString(50,760, texttlfo)
            var.rep.setFont('Helvetica-Bold', size=9)
            textlistado = 'LISTADO DE %s' % titulo
            var.rep.drawString(240, 695, textlistado)
        except Exception as error:
            print('Error cabecera informe prestamos: %s' % str(error))

    def cuerpoPrestamos(self):
        '''Escribe el cuerpo del informe préstamos que consiste en la lista de los datos Número de Socio,
        Código del Libro, Desde, Hasta, Devuelto y Fecha de devolución'''
        try:
            itemCli=['NUM SOCIO', 'COD LIBRO', 'DESDE','HASTA','DEVUELTO','FECHA DEVOLUCIÓN']
            var.rep.setFont('Helvetica-Bold', size=9)
            var.rep.line(45, 680, 525, 680)
            var.rep.drawString(50,667,itemCli[0])
            var.rep.drawString(120, 667, itemCli[1])
            var.rep.drawString(210, 667, itemCli[2])
            var.rep.drawString(280, 667, itemCli[3])
            var.rep.drawString(350, 667, itemCli[4])
            var.rep.drawString(430, 667, itemCli[5])
            var.rep.line(45,660,525,660)
            query = QtSql.QSqlQuery()
            query.prepare('select numSocio, codLibro, desde, hasta, devuelto, fdevolucion from prestamos order by devuelto')
            if query.exec_():
                i=70
                j=645
                cont=0
                while query.next():
                    var.rep.setFont('Helvetica', size=10)
                    var.rep.drawString(i,j, str(query.value(0)))
                    var.rep.drawString(i+68, j, str(query.value(1)))
                    var.rep.drawString(i+135, j, str(query.value(2)))
                    var.rep.drawString(i+203, j, str(query.value(3)))
                    var.rep.drawString(i +289, j, str(query.value(4)))
                    var.rep.drawString(i + 380, j, str(query.value(5)))
                    j=j-30
                    cont=cont+1
                    if (cont == 20):
                        Imprimir.pie(self)
                        var.rep.showPage()
                        i=70
                        j=745
                        var.rep.setFont('Helvetica-Bold', size=9)
                        var.rep.line(45, 790, 525, 790)
                        var.rep.drawString(50, 777, itemCli[0])
                        var.rep.drawString(120, 777, itemCli[1])
                        var.rep.drawString(210, 777, itemCli[2])
                        var.rep.drawString(280, 777, itemCli[3])
                        var.rep.drawString(350, 667, itemCli[4])
                        var.rep.drawString(430, 667, itemCli[5])
                        var.rep.line(45, 770, 525, 770)
                        cont = 0
                Imprimir.pie(self)
        except Exception as error:
            print('Error cuerpo informe prestamos: %s' % str(error))




    def informePrestamos(self):
        '''Imprime el informe de préstamos en la carpeta raíz'''

        try:
            var.rep = canvas.Canvas('Listado_prestamos.pdf')
            Imprimir.cabecera('PRÉSTAMOS')
            Imprimir.cuerpoPrestamos(self)
            var.rep.save()
            rootPath=".\\"
            cont =0
            for file in os.listdir(rootPath):
                if file.endswith('prestamos.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1
        except Exception as error:
            print('Error informePrestamos %s' % str(error))



    def cuerpoLibros(self):
        '''Escribe el cuerpo del informe libros que consiste en la lista de los datos Código de Libro,
               Estado, Título y Autor'''
        try:
            itemCli = ['CÓDIGO', 'ESTADO', 'TÍTULO', 'AUTOR']
            var.rep.setFont('Helvetica-Bold', size=9)
            var.rep.line(45, 680, 525, 680)
            var.rep.drawString(50, 667, itemCli[0])
            var.rep.drawString(111, 667, itemCli[1])
            var.rep.drawString(228, 667, itemCli[2])
            var.rep.drawString(450, 667, itemCli[3])
            var.rep.line(45, 660, 525, 660)
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, estado, titulo, autor from libros order by codigo')
            if query.exec_():
                i = 68
                j = 645
                cont = 0
                while query.next():
                    var.rep.setFont('Helvetica', size=8)
                    var.rep.drawString(i, j, str(query.value(0)))
                    var.rep.drawString(i + 43, j, str(query.value(1)))
                    var.rep.drawString(i + 160, j, str(query.value(2)))
                    var.rep.drawString(i + 382, j, str(query.value(3)))
                    j = j - 30
                    cont = cont + 1
                    if (cont == 20):
                        Imprimir.pie(self)
                        var.rep.showPage()
                        i = 68
                        j = 745
                        var.rep.setFont('Helvetica-Bold', size=9)
                        var.rep.line(45, 790, 525, 790)
                        var.rep.drawString(50, 777, itemCli[0])
                        var.rep.drawString(111, 777, itemCli[1])
                        var.rep.drawString(228, 777, itemCli[2])
                        var.rep.drawString(450, 777, itemCli[3])
                        var.rep.line(45, 770, 525, 770)
                        cont = 0
                Imprimir.pie(self)
        except Exception as error:
            print('Error cuerpo informe libros: %s' % str(error))

    def informeLibros(self):
        '''Imprime el informe de libros en la carpeta raíz'''

        try:
            var.rep = canvas.Canvas('Listado_libros.pdf')
            Imprimir.cabecera('LIBROS')
            Imprimir.cuerpoLibros(self)
            var.rep.save()
            rootPath = ".\\"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('libros.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1
        except Exception as error:
            print('Error informeLibros %s' % str(error))


    def cuerpoSocios(self):
        '''Escribe el cuerpo del informe socios que consiste en la lista de los datos Número de socio,
         DNI, Nombre y Apellidos'''

        try:
            itemCli = ['NUM SOCIO', 'DNI', 'NOMBRE', 'APELLIDOS']
            var.rep.setFont('Helvetica-Bold', size=9)
            var.rep.line(45, 680, 525, 680)
            var.rep.drawString(50, 667, itemCli[0])
            var.rep.drawString(130, 667, itemCli[1])
            var.rep.drawString(200, 667, itemCli[2])
            var.rep.drawString(350, 667, itemCli[3])
            var.rep.line(45, 660, 525, 660)
            query = QtSql.QSqlQuery()
            query.prepare('select numSocio, dni, nombre, apellidos from socios order by numSocio')
            if query.exec_():
                i = 70
                j = 645
                cont = 0
                while query.next():
                    var.rep.setFont('Helvetica', size=8)
                    var.rep.drawString(i, j, str(query.value(0)))
                    var.rep.drawString(i + 50, j, str(query.value(1)))
                    var.rep.drawString(i + 130, j, str(query.value(2)))
                    var.rep.drawString(i + 280, j, str(query.value(3)))
                    j = j - 30
                    cont = cont + 1
                    if (cont == 20):
                        Imprimir.pie(self)
                        var.rep.showPage()
                        i = 50
                        j = 745
                        var.rep.setFont('Helvetica-Bold', size=9)
                        var.rep.line(45, 790, 525, 790)
                        var.rep.drawString(65, 777, itemCli[0])
                        var.rep.drawString(190, 777, itemCli[1])
                        var.rep.drawString(330, 777, itemCli[2])
                        var.rep.drawString(445, 777, itemCli[3])
                        var.rep.line(45, 770, 525, 770)
                        cont = 0
                Imprimir.pie(self)
        except Exception as error:
            print('Error cuerpo informe libros: %s' % str(error))

    def informeSocios(self):
        '''Imprime el informe de socios en la carpeta raíz'''

        try:
            var.rep = canvas.Canvas('Listado_socios.pdf')
            Imprimir.cabecera('SOCIOS')
            Imprimir.cuerpoSocios(self)
            var.rep.save()
            rootPath = ".\\"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('socios.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1
        except Exception as error:
            print('Error informeLibros %s' % str(error))