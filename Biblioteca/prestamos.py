import eventos
import var
import conexion
from datetime import datetime
from dateutil.relativedelta import relativedelta


#GESTIÓN DE PRÉSTAMOS
class Prestamos:

    def gestionMultas(prestamo):
        '''Actualiza la multa de un socio en función de los cambios hechos en los préstamos.
        Si un préstamo, a día actual, no se ha devuelto, pondrá multa y salción al socio que tiene el libro.
        Si se registra una devolución y es posterior a la fecha de fin de préstamo, pondrá multa y sanción al socio que devuelve el libro'''

        multa=False
        fmulta=None

        # pestamo=[numSocio,codLibro,desde,hasta,devuelto,fdevolucion]
        hasta = datetime.strptime(prestamo[3], "%d/%m/%Y")
        devuelto = prestamo[4]
        hoy = datetime.now()
        delta = relativedelta(days=+15)

        if prestamo[5] != '':
            fdevolucion = datetime.strptime(prestamo[5], "%d/%m/%Y")
            if devuelto =='True' and fdevolucion > hasta:
                multa=True
                fmulta = fdevolucion + delta
                fmulta = fmulta.strftime('%d/%m/%Y')
            print('Fecha devolucion: ', fdevolucion)

        if devuelto =='False' and hoy > hasta:
            multa = True
            fmulta = hoy + delta
            fmulta = fmulta.strftime('%d/%m/%Y')

        print('Multa: ',multa)
        print('Fecha multa: ',fmulta)

        conexion.Socios.gestionMulta(prestamo[0],str(multa),fmulta)




    def modificarPrestamo(self):
        '''Recoge los datos que ha introducido el usuario para añadir una devolución
        y la registra modificando el dato de préstamo prexistente'''

        devolucion=[str(var.ui.datoCodigoLibroDevolucion.text()),str(var.ui.textBrowserFechaDevolucion.toPlainText())]
        if devolucion[0] !='' and devolucion[1]!='':
            if conexion.Libros.existeLibro(devolucion[0]):
                if not conexion.Libros.libroDisponible(devolucion[0]):
                    #pestamo=[numSocio,codLibro,desde,hasta,devuelto,fdevolucion]
                    prestamo = conexion.Prestamos.obtenerPrestamoDevolucion(devolucion[0])
                    conexion.Prestamos.modificarPrestamo(devolucion[0],devolucion[1])
                    prestamo[4] = 'True'
                    prestamo[5]=devolucion[1]
                    print(prestamo)
                    Prestamos.gestionMultas(prestamo)
                    conexion.Socios.modificarNumeroLibrosSocio(prestamo[0], prestamo[4])
                    conexion.Libros.modificarDisponibilidadLibro(prestamo[1],prestamo[4])
                    eventos.Aviso.mensajeVentanaAviso('DEVOLUCIÓN REGISTRADA')
                    eventos.Aviso.abrirVentanaAviso(self)
                    #conexion.Socios.actualizarSocios(self)
                    conexion.Prestamos.mostrarPrestamos(self)
                    conexion.Libros.mostrarLibros(self)
                    conexion.Socios.mostrarSocios(self)
                else:
                    print('EL LIBRO NO ESTÁ PRESTADO')
                    eventos.Aviso.mensajeVentanaAviso("EL LIBRO '"+devolucion[0]+"' NO ESTÁ PRESTADO\nPOR LO QUE NO ES POSIBLE DEVOLVERLO")
                    eventos.Aviso.abrirVentanaAviso(self)
            else:
                print('EL LIBRO NO EXISTE')
                eventos.Aviso.mensajeVentanaAviso("EL LIBRO '"+devolucion[0]+"' NO EXISTE EN LA BIBLIOTECA")
                eventos.Aviso.abrirVentanaAviso(self)
        else:
            print('DEBE INTRODUCIR:\n-CÓDIGO DEL LIBRO\n-FECHA DE DEVOLUCIÓN')
            eventos.Aviso.mensajeVentanaAviso('PARA AÑADIR UNA DEVOLUCIÓN DEBE INTRODUCIR:\n\n-CÓDIGO DEL LIBRO\n-FECHA DE DEVOLUCIÓN')
            eventos.Aviso.abrirVentanaAviso(self)




    def guardarPrestamo(self):
        '''Recoge los datos que ha introducido el usuario para guardar el el préstamo y guarda el libro'''

        if str(var.ui.datoNumeroSocioPrestamo.text())!='' and str(var.ui.datoCodigoLibroPrestamo.text())!='' and str(var.ui.textBrowserFechaDesde.toPlainText())!='':
            var.ui.textBrowserFechaDevolucion.setText('')
            prestamo = [var.ui.datoNumeroSocioPrestamo.text(), var.ui.datoCodigoLibroPrestamo.text(), var.ui.textBrowserFechaDesde.toPlainText(), var.ui.textBrowserFechaHasta.toPlainText(), 'False',var.ui.textBrowserFechaDevolucion.toPlainText()]
            if conexion.Libros.libroDisponible(prestamo[1]):
                if conexion.Socios.socioAptoPrestamo(prestamo[0]):
                    conexion.Prestamos.guardarPrestamo(prestamo)
                    eventos.Aviso.mensajeVentanaAviso('PRESTAMO REGISTRADO')
                    eventos.Aviso.abrirVentanaAviso(self)
                    Prestamos.gestionMultas(prestamo)
                    conexion.Socios.modificarNumeroLibrosSocio(prestamo[0],prestamo[4])
                    conexion.Libros.modificarDisponibilidadLibro(prestamo[1],prestamo[4])
                    #conexion.Socios.actualizarSocios(self)
                    conexion.Prestamos.mostrarPrestamos(self)
                    conexion.Libros.mostrarLibros(self)
                    conexion.Socios.mostrarSocios(self)
                else:
                    print('EL SOCIO TIENE MULTA O NO PUEDE PEDIR MÁS LIBROS PRESTADOS O EL NÚMERO DE SOCIO NO EXISTE')
                    eventos.Aviso.mensajeVentanaAviso("NO ES POSIBLE REGISTRAR EL PRÉSTAMO DEBIDO A UNO DE ESTOS MOVITOS:\n\n- EL SOCIO TIENE MULTA\n- EL SOCIO NO PUEDE PEDIR MÁS LIBROS PRESTADOS\n- EL NÚMERO DE SOCIO NO EXISTE")
                    eventos.Aviso.abrirVentanaAviso(self)
            else:
                print('EL LIBRO NO ESTÁ DISPONIBLE')
                eventos.Aviso.mensajeVentanaAviso("EL LIBRO '"+prestamo[1]+"' NO ESTÁ DISPONIBLE")
                eventos.Aviso.abrirVentanaAviso(self)
        else:
            print('DEBE INTRODUCIR:\n-NÚMERO DE SOCIO\n-CÓDIGO DEL LIBRO\n-FECHA DE PRÉSTAMO')
            eventos.Aviso.mensajeVentanaAviso('PARA AÑADIR UN PRÉSTAMO DEBE INTRODUCIR:\n\n- NÚMERO DE SOCIO\n- CÓDIGO DEL LIBRO\n- FECHA DE PRÉSTAMO')
            eventos.Aviso.abrirVentanaAviso(self)

    def limpiarPrestamos(self):
        '''Vacía todos los campos del formulario prestamos y devoluciones  de la interfaz gráfica'''

        var.ui.datoNumeroSocioPrestamo.setText("")
        var.ui.datoCodigoLibroPrestamo.setText("")
        var.ui.textBrowserFechaDesde.setText("")
        var.ui.textBrowserFechaHasta.setText("")
        var.ui.datoCodigoLibroDevolucion.setText("")
        var.ui.textBrowserFechaDevolucion.setText("")



