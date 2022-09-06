from PyQt5 import QtWidgets, QtSql

import eventos
import var
from datetime import datetime


#CONEXIÓN Y DESCONEXIÓN CON LA DB
class Conexion:

    def db_connect(filename):
        '''Conecta con la base de datos'''

        db=QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(filename)
        if not db.open():
            QtWidgets.QMessageBox.critical(None,'No se puede abrir la base de datos',
                                           'No se puede establecer conexión.\n' 'Haz Click para Cancelar.',
                                           QtWidgets.QMessageBox.Cancel)
            return False
        else:
            print('Conexión establecida')
            return True

    def db_desconectar(self):
        '''Desconecta con la base de datos'''

        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        if db.open():
            db.close()


#CONSULTAS, ISERCIONES, BAJAS Y MODIFICACIONES DE LA TABLA LIBROS
class Libros:

    def libroDisponible(codigoLibro):
        '''Comprueba si un libro está disponble dado su código de libro'''

        try:
            disponible=False
            query = QtSql.QSqlQuery()
            query.prepare('select estado from libros where codigo=:codigo')
            query.bindValue(':codigo', codigoLibro)
            if query.exec_():
                while query.next():
                    estado = str(query.value(0))
                    if(estado=='DISPONIBLE'):
                        disponible=True
            return disponible
        except Exception as error:
            print('Error disponibilidad libro: %s' % str(error))

    def modificarDisponibilidadLibro(codigoLibro, devuelto):
        '''Si un libro ha sido devuelto cambia su estado a DISPONIBLE
        y si ha sido prestado cambia su estado a NO DISPONIBLE/PRESTADO'''

        if devuelto == 'False':
            estadoLibro='NO DISPONIBLE/PRESTADO'
        elif devuelto == 'True':
            estadoLibro='DISPONIBLE'

        query = QtSql.QSqlQuery()
        query.prepare(
            'update libros set estado=:estado where codigo=:codigo')
        query.bindValue(':codigo', codigoLibro)
        query.bindValue(':estado', estadoLibro)
        if query.exec_():
            print('LIBRO MODIFICADO')
        else:
            print('Error modificar libro: ', query.lastError().text())

    def guardarLibro(libro):
        '''Añade un libro a la tabla libros'''

        query=QtSql.QSqlQuery()
        query.prepare('insert into libros (estado, titulo, autor, genero, etiquetas)'
                      'VALUES (:estado, :titulo, :autor, :genero,:etiquetas)')
        query.bindValue(':estado', str(libro[0]))
        query.bindValue(':titulo', str(libro[1]))
        query.bindValue(':autor', str(libro[2]))
        query.bindValue(':genero', str(libro[3]))
        query.bindValue(':etiquetas', str(libro[4]))

        if query.exec_():
            print('Insercción de libro correcta')
            Libros.mostrarLibros(libro)
        else:
            print('Error guardar libro: ', query.lastError().text())

    def bajaLibro(codigo):
        '''Elimina un libro de la tabla libros dado el código del libro'''

        query = QtSql.QSqlQuery()
        query.prepare('delete from libros where codigo = :codigo')
        query.bindValue(':codigo', codigo)
        if query.exec_():
            print('Libro eliminado')
        else:
            print('Error baja libro: ', query.lastError().text())

    def modificarLibro(modificacion):
        '''Dado el código del libro, modifica los valores de esa fila
        en la tabla libro por los valores nuevos indicados'''

        codigo = modificacion[0]
        query=QtSql.QSqlQuery()
        query.prepare('update libros set estado=:estado, titulo=:titulo, autor=:autor,genero=:genero, etiquetas=:etiquetas where codigo=:codigo')
        query.bindValue(':codigo', str(codigo))
        query.bindValue(':estado', str(modificacion[1]))
        query.bindValue(':titulo', str(modificacion[2]))
        query.bindValue(':autor', str(modificacion[3]))
        query.bindValue(':genero', str(modificacion[4]))
        query.bindValue(':etiquetas', str(modificacion[5]))
        if query.exec_():
            print('LIBRO MODIFICADO')
        else:
            print('Error modificar libro: ',query.lastError().text())


    def mostrarLibros(self):
        '''Recoge los valores de la tabla libros y los añade al QTableWiget tablaLibros de la interfaz gráfica'''

        index = 0
        query =QtSql.QSqlQuery()
        query.prepare('select codigo, estado, titulo, autor, genero from libros')
        if query.exec_():
            while query.next():
                codigo =str(query.value(0))
                estado = query.value(1)
                titulo = query.value(2)
                autor = query.value(3)
                genero = query.value(4)
                var.ui.tablaLibros.setRowCount(index+1)#Crea la fila y a continuación mete los datos
                var.ui.tablaLibros.setItem(index,0, QtWidgets.QTableWidgetItem(codigo))
                var.ui.tablaLibros.setItem(index,1, QtWidgets.QTableWidgetItem(estado))
                var.ui.tablaLibros.setItem(index,2, QtWidgets.QTableWidgetItem(titulo))
                var.ui.tablaLibros.setItem(index,3, QtWidgets.QTableWidgetItem(autor))
                var.ui.tablaLibros.setItem(index,4, QtWidgets.QTableWidgetItem(genero))
                index +=1
        else:
            var.ui.tablaLibros.setRowCount(1)  # Crea la fila y a continuación mete los datos
            var.ui.tablaLibros.setItem(index, 0, QtWidgets.QTableWidgetItem(""))
            var.ui.tablaLibros.setItem(index, 1, QtWidgets.QTableWidgetItem(""))
            var.ui.tablaLibros.setItem(index, 2, QtWidgets.QTableWidgetItem(""))
            var.ui.tablaLibros.setItem(index, 3, QtWidgets.QTableWidgetItem(""))
            var.ui.tablaLibros.setItem(index, 4, QtWidgets.QTableWidgetItem(""))
            print('Error mostrar libros: ',query.lastError().text())

    def existeLibro(id):
        '''Dado un código de libro comprueba si existe en la tabla libros'''

        try:
            salida=False
            query = QtSql.QSqlQuery()
            query.prepare('select codigo from libros')
            if query.exec_():
                while query.next():
                    codigo = str(query.value(0))
                    if(codigo==id):
                        salida=True
            return salida
        except Exception as error:
            print('Error existe libro: %s' % str(error))

    def existeLibroTitulo(id):
        '''Dado un título de libro comprueba si existe en la tabla libros'''

        try:
            salida=False
            query = QtSql.QSqlQuery()
            query.prepare('select titulo from libros')
            if query.exec_():
                while query.next():
                    titulo = query.value(0)
                    if(titulo==id):
                        salida=True
            return salida
        except Exception as error:
            print('Error existe libro titulo: %s' % str(error))

    def existeLibroAutor(id):
        '''Dado un autor de libro comprueba si existe en la tabla libros'''

        try:
            salida=False
            query = QtSql.QSqlQuery()
            query.prepare('select autor from libros')
            if query.exec_():
                while query.next():
                    autor = query.value(0)
                    if(autor==id):
                        salida=True
            return salida
        except Exception as error:
            print('Error existe libro autor: %s' % str(error))

    def existeLibroGenero(id):
        '''Dado un género de libro comprueba si existe en la tabla libros'''

        try:
            salida=False
            query = QtSql.QSqlQuery()
            query.prepare('select genero from libros')
            if query.exec_():
                while query.next():
                    genero = query.value(0)
                    if(genero==id):
                        salida=True
            return salida
        except Exception as error:
            print('Error existe libro genero: %s' % str(error))

    def existeLibroEstado(id):
        '''Dado un estado de libro comprueba si existe en la tabla libros'''

        try:
            salida=False
            query = QtSql.QSqlQuery()
            query.prepare('select estado from libros')
            if query.exec_():
                while query.next():
                    estado = query.value(0)
                    if(estado==id):
                        salida=True
            return salida
        except Exception as error:
            print('Error existe libro genero: %s' % str(error))

    def resultadosBusqueda(query):
        '''Añade los resultados de una consulta de la tabla libros a la QTableWidget tablaLibros de la interfaz gráfica'''

        index = 0
        if query.exec_():
            while query.next():
                var.codigo = query.value(0)
                var.estado = query.value(1)
                var.titulo = query.value(2)
                var.autor = query.value(3)
                var.genero = query.value(4)
                var.etiqueta = query.value(5)

                print(var.etiqueta)

                var.ui.tablaLibros.setRowCount(index + 1)  # Crea la fila y a continuación mete los datos
                var.ui.tablaLibros.setItem(index, 0, QtWidgets.QTableWidgetItem(str(var.codigo)))
                var.ui.tablaLibros.setItem(index, 1, QtWidgets.QTableWidgetItem(var.estado))
                var.ui.tablaLibros.setItem(index, 2, QtWidgets.QTableWidgetItem(var.titulo))
                var.ui.tablaLibros.setItem(index, 3, QtWidgets.QTableWidgetItem(var.autor))
                var.ui.tablaLibros.setItem(index, 4, QtWidgets.QTableWidgetItem(var.genero))
                index += 1
        else:
            print('Error buscar libro: ', query.lastError().text())

    def buscarLibroCodigo(id):
        '''Consulta que devuelve los valores de los campos de la tabla libros, dado el código del libro'''

        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'select codigo, estado, titulo, autor, genero, etiquetas from libros where codigo=:codigo')
            query.bindValue(':codigo', id)
            Libros.resultadosBusqueda(query)
        except Exception as error:
            print('Error buscar libro: %s' % str(error))

    def buscarLibroTitulo(titulo):
        '''Consulta que devuelve los valores de los campos de la tabla libros, dado el título del libro'''

        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'select codigo, estado, titulo, autor, genero, etiquetas from libros where titulo=:titulo')
            query.bindValue(':titulo', titulo)
            Libros.resultadosBusqueda(query)
        except Exception as error:
            print('Error buscar libro titulo: %s' % str(error))

    def buscarLibroAutor(autor):
        '''Consulta que devuelve los valores de los campos de la tabla libros, dado el autor del libro'''

        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'select codigo, estado, titulo, autor, genero, etiquetas from libros where autor=:autor')
            query.bindValue(':autor', autor)
            Libros.resultadosBusqueda(query)
        except Exception as error:
            print('Error buscar libro autor: %s' % str(error))


    def buscarLibroGenero(genero):
        '''Consulta que devuelve los valores de los campos de la tabla libros, dado el genéro del libro'''

        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'select codigo, estado, titulo, autor, genero, etiquetas from libros where genero=:genero')
            query.bindValue(':genero', genero)
            Libros.resultadosBusqueda(query)
        except Exception as error:
            print('Error buscar libro genero: %s' % str(error))

    def buscarLibroEstado(estado):
        '''Consulta que devuelve los valores de los campos de la tabla libros, dado el estado del libro'''

        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'select codigo, estado, titulo, autor, genero, etiquetas from libros where estado=:estado')
            query.bindValue(':estado', estado)
            Libros.resultadosBusqueda(query)
        except Exception as error:
            print('Error buscar libro estado: %s' % str(error))


#CONSULTAS, ISERCIONES, BAJAS Y MODIFICACIONES DE LA TABLA SOCIOS
class Socios:

    def actualizarSocios(self):
        '''Actualiza las sanciones de los socios.
        Si ya a pasado la fecha de su sanción,
        esta se eliminará y se le quitará la multa'''

        sociosSancionExpirada=[]#Lista
        hoy = datetime.now()
        query = QtSql.QSqlQuery()
        query.prepare('select numSocio, fmulta from socios')
        if query.exec_():
            while query.next():
                numSocio = str(query.value(0))
                fmulta = query.value(1)

                if fmulta != '':
                    fsancion = datetime.strptime(fmulta, "%d/%m/%Y")
                    if hoy > fsancion:
                        sociosSancionExpirada.append(numSocio)

        for i in sociosSancionExpirada:
            query = QtSql.QSqlQuery()
            query.prepare(
                'update socios set multa=:multa, fmulta=:fmulta where numSocio=:numSocio')
            query.bindValue(':numSocio', i)
            query.bindValue(':multa', 'False')
            query.bindValue(':fmulta', '')
            if query.exec_():
                print('SOCIO ACTUALIZADO')


    def modificarNumeroLibrosSocio(numSocio, devuelto):
        '''Dado el número de socio y estado de un libro en la tabla prestamos,
        si un libro ha sido devuelto cambia resta 1 al número de libros que ese socio tiene como prestados
        y si ha sido prestado suma 1 al número de libros que ese socio tiene como prestados'''

        numLibros=0
        query1 = QtSql.QSqlQuery()
        query1.prepare('select numLibros from socios where numSocio=:numSocio')
        query1.bindValue(':numSocio', numSocio)
        if query1.exec_():
            while query1.next():
                numLibros = query1.value(0)
        if devuelto=='True':
            numLibros=numLibros-1
        elif devuelto=='False':
            numLibros=numLibros+1

        query = QtSql.QSqlQuery()
        query.prepare(
            'update socios set numLibros=:numLibros where numSocio=:numSocio')
        query.bindValue(':numSocio', str(numSocio))
        query.bindValue(':numLibros', str(numLibros))
        if query.exec_():
            print('SOCIO MODIFICADO')
        else:
            print('Error modificar socio: ', query.lastError().text())

    def socioAptoPrestamo(numSocio):
        '''Dado un número de socio comprueba si este tiene multa o no y el número de libros que tiene prestados,
        si no tiene multa y el número de libros prestados es inferior a tres, es apto para préstamo'''

        try:
            socioApto=False
            query = QtSql.QSqlQuery()
            query.prepare('select multa, numLibros from socios where numSocio=:numSocio')
            query.bindValue(':numSocio', numSocio)
            if query.exec_():
                while query.next():
                    multa = str(query.value(0))
                    numLibros = query.value(1)
                    if(multa=='False' and numLibros<3):
                        socioApto=True
            return socioApto
        except Exception as error:
            print('Error socio apto prestamo: %s' % str(error))

    def guardarSocio(socio):
        '''Añade un socio a la tabla socios'''

        query=QtSql.QSqlQuery()
        query.prepare('insert into socios (dni, nombre, apellidos, direccion, sexo, multa, fmulta, numLibros)'
                      'VALUES (:dni, :nombre, :apellidos, :direccion, :sexo, :multa, :fmulta, :numLibros)')
        query.bindValue(':dni', str(socio[0]))
        query.bindValue(':nombre', str(socio[1]))
        query.bindValue(':apellidos', str(socio[2]))
        query.bindValue(':direccion', str(socio[3]))
        query.bindValue(':sexo', str(socio[4]))
        query.bindValue(':multa', str(socio[5]))
        query.bindValue(':fmulta', str(socio[6]))
        query.bindValue(':numLibros', str(socio[7]))

        if query.exec_():
            print('Insercción de socio correcta')
            eventos.Aviso.mensajeVentanaAviso("SOCIO AÑADIDO")
            eventos.Aviso.abrirVentanaAviso(socio)
            Socios.mostrarSocios(socio)
        else:
            eventos.Aviso.mensajeVentanaAviso("\tNO ES POSIBLE AÑADIR EL SOCIO\n\nEL DNI '"+socio[0]+"' YA ESTÁ REGISTRADO EN LA BIBLIOTECA")
            eventos.Aviso.abrirVentanaAviso(socio)
            print('Error guardar socio: ', query.lastError().text())

    def modificarSocio(socio):
        '''Dado el número de socio, modifica los valores de esa fila
        en la tabla socios por los valores nuevos indicados'''

        numSocio = socio[0]
        query = QtSql.QSqlQuery()
        query.prepare(
            'update socios set dni=:dni, nombre=:nombre, apellidos=:apellidos,direccion=:direccion, sexo=:sexo, multa=:multa, fmulta=:fmulta, numLibros=:numLibros where numSocio=:numSocio')
        query.bindValue(':numSocio', str(numSocio))
        query.bindValue(':dni', str(socio[1]))
        query.bindValue(':nombre', str(socio[2]))
        query.bindValue(':apellidos', str(socio[3]))
        query.bindValue(':direccion', str(socio[4]))
        query.bindValue(':sexo', str(socio[5]))
        query.bindValue(':multa', str(socio[6]))
        query.bindValue(':fmulta', str(socio[7]))
        query.bindValue(':numLibros', str(socio[8]))
        if query.exec_():
            print('SOCIO MODIFICADO')
        else:
            print('Error modificar SOCIO: ', query.lastError().text())

    def bajaSocio(numSocio):
        '''Dado un número de socio lo elimina de la tabla socios'''

        query = QtSql.QSqlQuery()
        query.prepare('delete from socios where numSocio = :numSocio')
        query.bindValue(':numSocio', numSocio)
        if query.exec_():
            print('Socio eliminado')
        else:
            print('Error baja socio: ', query.lastError().text())


    def mostrarSocios(self):
        '''Recoge los valores de la tabla socios y los añade al QTableWiget tablaSocios de la interfaz gráfica'''

        index = 0
        query =QtSql.QSqlQuery()
        query.prepare('select numSocio, dni, nombre, apellidos, direccion, sexo, multa, fmulta, numLibros from socios')
        if query.exec_():
            while query.next():
                numSocio =str(query.value(0))
                dni = query.value(1)
                nombre = query.value(2)
                apellidos = query.value(3)
                direccion = query.value(4)
                sexo = query.value(5)
                multa = query.value(6)
                fmulta = query.value(7)
                numLibros = str(query.value(8))

                var.ui.tablaSocios.setRowCount(index+1)#Crea la fila y a continuación mete los datos
                var.ui.tablaSocios.setItem(index,0, QtWidgets.QTableWidgetItem(numSocio))
                var.ui.tablaSocios.setItem(index,1, QtWidgets.QTableWidgetItem(dni))
                var.ui.tablaSocios.setItem(index,2, QtWidgets.QTableWidgetItem(numLibros))
                var.ui.tablaSocios.setItem(index,3, QtWidgets.QTableWidgetItem(multa))
                var.ui.tablaSocios.setItem(index,4, QtWidgets.QTableWidgetItem(fmulta))
                var.ui.tablaSocios.setItem(index, 5, QtWidgets.QTableWidgetItem(nombre))
                var.ui.tablaSocios.setItem(index, 6, QtWidgets.QTableWidgetItem(apellidos))
                var.ui.tablaSocios.setItem(index, 7, QtWidgets.QTableWidgetItem(direccion))
                var.ui.tablaSocios.setItem(index, 8, QtWidgets.QTableWidgetItem(sexo))
                index +=1
        else:
            var.ui.tablaSocios.setRowCount(1)  # Crea la fila y a continuación mete los datos
            var.ui.tablaSocios.setItem(index, 0, QtWidgets.QTableWidgetItem(""))
            var.ui.tablaSocios.setItem(index, 1, QtWidgets.QTableWidgetItem(""))
            var.ui.tablaSocios.setItem(index, 2, QtWidgets.QTableWidgetItem(""))
            var.ui.tablaSocios.setItem(index, 3, QtWidgets.QTableWidgetItem(""))
            var.ui.tablaSocios.setItem(index, 4, QtWidgets.QTableWidgetItem(""))
            var.ui.tablaSocios.setItem(index, 5, QtWidgets.QTableWidgetItem(""))
            var.ui.tablaSocios.setItem(index, 6, QtWidgets.QTableWidgetItem(""))
            var.ui.tablaSocios.setItem(index, 7, QtWidgets.QTableWidgetItem(""))
            var.ui.tablaSocios.setItem(index, 8, QtWidgets.QTableWidgetItem(""))

            print('Error mostrar libros: ',query.lastError().text())


    def existeSocioDni(id):
        '''Dado un dni de un socio comprueba si existe en la tabla socios'''

        try:
            salida = False
            query = QtSql.QSqlQuery()
            query.prepare('select dni from socios')
            if query.exec_():
                while query.next():
                    dni = query.value(0)
                    if (dni == id):
                        salida = True
            return salida
        except Exception as error:
            print('Error existe socio dni: %s' % str(error))

    def existeSocioNumero(numSocio):
        '''Dado un numero de socio de un socio comprueba si existe en la tabla socios'''

        try:
            salida = False
            query = QtSql.QSqlQuery()
            query.prepare('select numSocio from socios')
            if query.exec_():
                while query.next():
                    socio = str(query.value(0))
                    if (socio == numSocio):
                        salida = True
            return salida
        except Exception as error:
            print('Error existe socio numero: %s' % str(error))


    def buscarSocioDni(dni):
        '''Consulta que devuelve los valores de los campos de la tabla socios, dado el dni del socio'''

        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'select numSocio, dni, nombre, apellidos, direccion, sexo, multa, fmulta ,numLibros from socios where dni=:dni')
            query.bindValue(':dni', dni)
            Socios.resultadosBusqueda(query)
        except Exception as error:
            print('Error buscar libro estado: %s' % str(error))


    def buscarSocioNumero(numSocio):
        '''Consulta que devuelve los valores de los campos de la tabla socios, dado el número de socio'''

        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'select numSocio, dni, nombre, apellidos, direccion, sexo, multa, fmulta ,numLibros from socios where numSocio=:numSocio')
            query.bindValue(':numSocio', numSocio)
            Socios.resultadosBusqueda(query)
        except Exception as error:
            print('Error numero Socio : %s' % str(error))


    def resultadosBusqueda(query):
        '''Añade los resultados de una consulta de la tabla socios a la QTableWidget tablaSocios de la interfaz gráfica'''

        index = 0
        if query.exec_():
            while query.next():
                var.numSocio = query.value(0)
                var.dni = query.value(1)
                var.nombre = query.value(2)
                var.apellidos = query.value(3)
                var.direccion = query.value(4)
                var.sexo = query.value(5)
                var.multa = query.value(6)
                var.fmulta = query.value(7)
                var.numLibros=query.value(8)

                var.ui.tablaSocios.setRowCount(index + 1)  # Crea la fila y a continuación mete los datos
                var.ui.tablaSocios.setItem(index, 0, QtWidgets.QTableWidgetItem(str(var.numSocio)))
                var.ui.tablaSocios.setItem(index, 1, QtWidgets.QTableWidgetItem(var.dni))
                var.ui.tablaSocios.setItem(index, 2, QtWidgets.QTableWidgetItem(str(var.numLibros)))
                var.ui.tablaSocios.setItem(index, 3, QtWidgets.QTableWidgetItem(var.multa))
                var.ui.tablaSocios.setItem(index, 4, QtWidgets.QTableWidgetItem(var.fmulta))
                var.ui.tablaSocios.setItem(index, 5, QtWidgets.QTableWidgetItem(var.nombre))
                var.ui.tablaSocios.setItem(index, 6, QtWidgets.QTableWidgetItem(var.apellidos))
                var.ui.tablaSocios.setItem(index, 7, QtWidgets.QTableWidgetItem(var.direccion))
                var.ui.tablaSocios.setItem(index, 8, QtWidgets.QTableWidgetItem(var.sexo))
                index += 1
        else:
            print('Error buscar socio: ', query.lastError().text())


    def gestionMulta(numSocio, multa, fmulta):
        '''Dado un número de socio, modifica los valores de multa y fecha de multa por los nuevos indicados'''

        query = QtSql.QSqlQuery()
        query.prepare(
            'update socios set multa=:multa, fmulta=:fmulta where numSocio=:numSocio')
        query.bindValue(':numSocio', str(numSocio))
        query.bindValue(':multa', multa)
        query.bindValue(':fmulta', fmulta)
        if query.exec_():
            print('MULTA SOCIO MODIFICADA')
        else:
            print('Error modificar multa socio: ', query.lastError().text())




#CONEXION DE LOS PRÉSTAMOS
class Prestamos:

    def guardarPrestamo(prestamo):
        '''Añade un préstamo a la tabla prestamos'''

        query=QtSql.QSqlQuery()
        query.prepare('insert into prestamos (numSocio, codLibro, desde, hasta, devuelto)'
                      'VALUES (:numSocio, :codLibro, :desde, :hasta, :devuelto)')
        query.bindValue(':numSocio', str(prestamo[0]))
        query.bindValue(':codLibro', str(prestamo[1]))
        query.bindValue(':desde', str(prestamo[2]))
        query.bindValue(':hasta', str(prestamo[3]))
        query.bindValue(':devuelto', str(prestamo[4]))

        if query.exec_():
            #var.ui.tbEstado.setText("CLIENTE DNI '" +cliente[0] + "' HA SIDO DADO DE ALTA")
            print('Insercción de prestamo correcta')
            Prestamos.mostrarPrestamos(prestamo)
        else:
            #var.ui.tbEstado.setText("CLIENTE DNI '" + cliente[0] + "' YA EXISTE EN LA BD")
            print('Error guardar prestamo: ', query.lastError().text())

    def mostrarPrestamos(self):
        '''Recoge los valores de la tabla prestamos y los añade al QTableWiget tabla prestamos de la interfaz gráfica'''

        try:
            index = 0
            query =QtSql.QSqlQuery()
            query.prepare('select numSocio, codLibro, desde, hasta, devuelto, fdevolucion from prestamos order by devuelto')
            if query.exec_():
                while query.next():
                    numSocio =str(query.value(0))
                    codLibro = str(query.value(1))
                    desde = query.value(2)
                    hasta = query.value(3)
                    devuelto = str(query.value(4))
                    fdevolucion = query.value(5)
                    var.ui.tablaPrestamos.setRowCount(index+1)#Crea la fila y a continuación mete los datos
                    var.ui.tablaPrestamos.setItem(index,0, QtWidgets.QTableWidgetItem(numSocio))
                    var.ui.tablaPrestamos.setItem(index,1, QtWidgets.QTableWidgetItem(codLibro))
                    var.ui.tablaPrestamos.setItem(index,2, QtWidgets.QTableWidgetItem(desde))
                    var.ui.tablaPrestamos.setItem(index,3, QtWidgets.QTableWidgetItem(hasta))
                    var.ui.tablaPrestamos.setItem(index,4, QtWidgets.QTableWidgetItem(devuelto))
                    var.ui.tablaPrestamos.setItem(index, 5, QtWidgets.QTableWidgetItem(fdevolucion))
                    index +=1
            else:
                var.ui.tablaLibros.setRowCount(1)  # Crea la fila y a continuación mete los datos
                var.ui.tablaLibros.setItem(index, 0, QtWidgets.QTableWidgetItem(""))
                var.ui.tablaLibros.setItem(index, 1, QtWidgets.QTableWidgetItem(""))
                var.ui.tablaLibros.setItem(index, 2, QtWidgets.QTableWidgetItem(""))
                var.ui.tablaLibros.setItem(index, 3, QtWidgets.QTableWidgetItem(""))
                var.ui.tablaLibros.setItem(index, 4, QtWidgets.QTableWidgetItem(""))
                var.ui.tablaLibros.setItem(index, 5, QtWidgets.QTableWidgetItem(""))
                print('Error mostrar libros: ',query.lastError().text())
        except Exception as error:
            print('Excepcion aaaa: ', error)


    def modificarPrestamo(codLibro, fdevolucion):
        '''Dado el código del libro y la nueva fecha de devolución, modifica el valor de la fecha de devolución,
        marcándolo como devueltoesa fila en la tabla prestamos'''

        query = QtSql.QSqlQuery()
        query.prepare(
            'update prestamos set devuelto=:devuelto, fdevolucion=:fdevolucion where codLibro=:codLibro and devuelto="False"')
        query.bindValue(':codLibro', codLibro)
        query.bindValue(':devuelto', 'True')
        query.bindValue(':fdevolucion', fdevolucion)
        if query.exec_():
            print('DEVOLUCIÓN REALIZADA')
            # var.ui.tbEstado.setText('LIBRO CON CODIGO %s HA SIDO MODIFICADO' % codigo)
        else:
            print('Error devolucion prestamo: ', query.lastError().text())

    def obtenerPrestamoDevolucion(codLibro):
        '''Dado un código de libro, devuelve los valores de la fila de la tabla prestamos
        donde este figura como no devuelto'''

        numSocio=''
        cod=''
        desde=''
        hasta=''
        devuelto=''
        fdevolucion=''
        query = QtSql.QSqlQuery()
        # pestamo=[numSocio,codLibro,desde,hasta,devuelto,fdevolucion]
        query.prepare('select numSocio, codLibro, desde, hasta, devuelto, fdevolucion from prestamos where codLibro=:codLibro and devuelto=:devuelto')
        query.bindValue(':codLibro', int(codLibro))
        query.bindValue(':devuelto', 'False')
        if query.exec_():
            while query.next():
                numSocio = str(query.value(0))
                cod = str(query.value(1))
                desde = query.value(2)
                hasta = query.value(3)
                devuelto = str(query.value(4))
                fdevolucion = query.value(5)

        prestamo=[numSocio,codLibro,desde,hasta,devuelto,fdevolucion]
        return prestamo

