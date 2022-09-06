import sys
from datetime import datetime
from PyQt5 import QtWidgets
import zipfile
import shutil
import os.path



import var

#EVENTOS DE LOS CALENDARIOS
class Calendario:

    def abrirCalendarioPrestamo(self):
        '''Abre la ventana de diálogo del calendario que cargará las fechas de préstamo'''

        try:
            var.uiCalendarioPrestamo.show()
        except Exception as error:
            print('Error abrir calendario: %s' % str(error))

    def abrirCalendarioDevolucion(self):
        '''Abre la ventana de diálogo del calendario que cargará las fechas de devolución'''

        try:
            var.uiCalendarioDevolucion.show()
        except Exception as error:
            print('Error abrir calendario: %s' % str(error))

    def abrirCalendarioSancion(self):
        '''Abre la ventana de diálogo del calendario que cargará las fechas de multa'''

        try:
            var.uiCalendarioSancion.show()
        except Exception as error:
            print('Error abrir calendario: %s' % str(error))

    def cargarFechaDesde(qDate):
        '''Carga la fecha de inicio de préstamo desde la ventna de dialogo del calendario de préstamo y cierra esa misma ventana'''

        try:
            data=('{0}/{1}/{2}'.format(qDate.day(),qDate.month(),qDate.year()))
            var.ui.textBrowserFechaDesde.setText(str(data))
            var.uiCalendarioPrestamo.hide()
        except Exception as error:
            print('Error cargar fecha prestamo: %' % str(error))

    def cargarFechaHasta(qDate):
        '''Carga la fecha de fin de préstamo desde la ventna de dialogo del calendario de préstamo'''

        try:
            data = ('{0}/{1}/{2}'.format(qDate.addDays(15).day(), qDate.addDays(15).month(), qDate.addDays(15).year()))
            var.ui.textBrowserFechaHasta.setText(str(data))
        except Exception as error:
            print('Error cargar fecha devolución: %s' % str(error))

    def cargarFechaDevolucion(qDate):
        '''Carga la fecha de devolución desde la ventna de dialogo del calendario de devolución y cierra esa misma ventana'''

        try:
            data=('{0}/{1}/{2}'.format(qDate.day(),qDate.month(),qDate.year()))
            var.ui.textBrowserFechaDevolucion.setText(str(data))
            var.uiCalendarioDevolucion.hide()
        except Exception as error:
            print('Error cargar fecha devolución: %' % str(error))

    def cargarFechaSancion(qDate):
        '''Carga la fecha de multa desde la ventna de dialogo del calendario de sanción y cierra esa misma ventana'''
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.textBrowserSancionHasta.setText(str(data))
            var.uiCalendarioSancion.hide()
        except Exception as error:
            print('Error cargar fecha sancion: %' % str(error))

#EVENTOS DE LOS MENSAJES DE AVISO
class Aviso:

    def abrirVentanaAviso(self):
        '''Abre la ventana de diálogo que contiene el aviso'''
        try:
            var.uiAviso.show()
        except Exception as error:
            print('Error abrir aviso: %s' % str(error))

    def cerrarVentanaAviso(self):
        '''Cierra la ventana de diálogo que contiene el aviso'''
        try:
            var.uiAviso.hide()
        except Exception as error:
            print('Error cerrar aviso: %s' % str(error))

    def mensajeVentanaAviso(mensaje):
        '''Añade el aviso a la ventana de diálogo de avisos'''
        var.uiAviso.setText(mensaje)

#EVENTOS SALIR
class Salir:

    def salir(self):
        '''Cierra el programa'''
        try:
            sys.exit()
        except Exception as error:
            print("Error salir : %s " % str(error))

    def preguntaSalir(self):
        '''Abre la ventana de dialogo de salir.
        Cierra el programa si se pulsa Ok, cierra la ventana si se pulsa Cancel'''

        try:
            var.uiSalir.show()
            if var.uiSalir.exec():
                sys.exit()
            else:
                var.uiSalir.hide()
        except Exception as error:
            print("Error %s: " % str(error))

class Comprimir:

    def BackupBaseDatos(self):
        '''Abre una ventana de dialogo y permite guardar una copia de la base de datos en un archivo zip'''

        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            var.copia = (str(fecha) + 'BibliotecaDB.zip')
            option = QtWidgets.QFileDialog.Options()
            directorio, filename = var.uiAbrir.getSaveFileName(None, 'Guardar Copia', var.copia, '.zip',
                                                                    options=option)
            if var.uiAbrir.Accepted and filename != '':
                ficheroZip = zipfile.ZipFile(var.copia, 'w')
                ficheroZip.write(var.filedb, os.path.basename(var.filedb), zipfile.ZIP_DEFLATED)
                ficheroZip.close()
                Aviso.mensajeVentanaAviso("BASE DE DATOS BIBLIOTECA COPIADA A ARCHIVO ZIP")
                Aviso.abrirVentanaAviso(self)
                shutil.move(str(var.copia), str(directorio))
        except Exception as error:
            print('Error al comprimir: %s' % str(error))

class Abrir:

    def abrirExplorador(self):
        try:
            var.uiAbrir.show()
        except Exception as error:
            print('Error abrir explorador: %s ' % str(error))