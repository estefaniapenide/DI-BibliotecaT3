import eventos
import var
import conexion

#GESTIÓN DE LIBROS
class Libros:

    def cargarGenero(self):
        '''Carga los géneros que puede tener el libro en el comboBox de la interfaz gráfica'''

        try:
            genero=['','Narrativa','Teatro','Poesía','Ensayo']
            for i in genero:
                var.ui.comboBoxGenero.addItem(i)
        except Exception as error:
            print('Error al cargar género: %s'% str(error))

    def seleccionarGenero(genero):
        '''Selecciona el género que ha marcado el usuario'''

        try:
            var.generoLibro=genero
        except Exception as error:
            print('Error: %s' % str(error))

    def seleccionarEstado(self):
        '''Selecciona el estado que ha marcado el usuario'''

        try:
            index = var.ui.spinBoxEstado.value()
            estado = ['DISPONIBLE', 'NO DISPONIBLE/PRESTADO']
            var.estadoLibro = estado[index]
            var.ui.indicadorEstado.setText(var.estadoLibro)
            var.ui.indicadorEstado.setText(var.estadoLibro)
        except Exception as error:
            print('Error seleccionar estado: %s' % str(error))


    def seleccionarEtiquetas(self):
        '''Selecciona las etiquetas que ha marcado el usuario'''

        try:
            var.etiquetas = [] #Se guardará en la base de datos
            if var.ui.checkBoxAventuras.isChecked():
                var.etiquetas.append('Aventuras')
            if var.ui.checkBoxFantasia.isChecked():
                var.etiquetas.append('Fantasía')
            if var.ui.checkBoxFilosofia.isChecked():
                var.etiquetas.append('Filosofía')
            if var.ui.checkBoxIntriga.isChecked():
                var.etiquetas.append('Intriga')
            if var.ui.checkBoxHistorica.isChecked():
                var.etiquetas.append('Histórica')
            if var.ui.checkBoxRomantica.isChecked():
                var.etiquetas.append('Romántica')

        except Exception as error:
            print('Error selccionar etiquetas: %s' % str(error))

    def marcarEtiquetas(self):
        '''Escucha la marcación de etiquetas por parte del usuario'''

        var.checkBoxEtiquetas = (var.ui.checkBoxAventuras, var.ui.checkBoxFantasia, var.ui.checkBoxFilosofia, var.ui.checkBoxIntriga, var.ui.checkBoxHistorica, var.ui.checkBoxRomantica)
        for i in var.checkBoxEtiquetas:
            i.stateChanged.connect(Libros.seleccionarEtiquetas)

    def guardarLibro(self):
        '''Recoge los datos que ha introducido el usuario para guardar el libro y guarda el libro'''

        try:
            libro = [var.estadoLibro, var.ui.lineEditTitulo.text().upper(), var.ui.lineEditAutor.text().upper(), var.generoLibro, var.etiquetas]

            if var.ui.lineEditTitulo.text()!='':
                conexion.Libros.guardarLibro(libro)
                eventos.Aviso.mensajeVentanaAviso('LIBRO AÑADIDO')
                eventos.Aviso.abrirVentanaAviso(self)
                #Libros.buscarLibroCodigo(self)
                conexion.Libros.mostrarLibros(self)
                print('LIBRO AÑADIDO')
            else:
                print('PARA AÑADIR UN LIBRO DEBE INTRODUCIR AL MENOS EL TÍTULO')
                eventos.Aviso.mensajeVentanaAviso('PARA AÑADIR UN LIBRO DEBE INTRODUCIR AL MENOS EL TÍTULO')
                eventos.Aviso.abrirVentanaAviso(self)

        except Exception as error:
            print('Error guardar libro (libros): %s ' % str(error))


    def eliminarLibro(self):
        '''Recoge el dato de código de libro indicado por el usuario para eliminar el libro y elimina el libro'''

        try:
            codigo = var.ui.labelCodigoGenerado.text()
            if (conexion.Libros.existeLibro(codigo)):
                conexion.Libros.bajaLibro(codigo)
                eventos.Aviso.mensajeVentanaAviso("LIBRO ELIMINADO")
                eventos.Aviso.abrirVentanaAviso(self)
                conexion.Libros.mostrarLibros(self)
                Libros.limpiarLibro(self)

            else:
                print('NO EXISTE EL CLIENTE')
                if var.ui.labelCodigoGenerado.text()=='':
                    print("NO HA SELECCIONADO NINGÚN LIBRO")
                    eventos.Aviso.mensajeVentanaAviso("NO HA INTRODUCIDO NINGÚN CÓDIGO DE LIBRO\nEN LA BARRA DE BÚSQUEDA")
                    eventos.Aviso.abrirVentanaAviso(self)
                else:
                    print("LIBRO CON CÓDIGO '" + codigo + "' NO EXISTE EN LA BD")
                    eventos.Aviso.mensajeVentanaAviso("LIBRO CON CÓDIGO '" + codigo + "' NO EXISTE EN LA BIBLIOTECA")
                    eventos.Aviso.abrirVentanaAviso(self)
        except Exception as error:
            print('Error eliminar libro: %s' % str(error))


    def modificarLibro(self):
        '''Recoge los datos que ha introducido el usuario para modificar el libro y modifica el libro'''

        try:
            libro = [var.ui.labelCodigoGenerado.text(), var.estadoLibro, var.ui.lineEditTitulo.text().upper(), var.ui.lineEditAutor.text().upper(), var.generoLibro, var.etiquetas]
            if (conexion.Libros.existeLibro(libro[0])):
                conexion.Libros.modificarLibro(libro)
                eventos.Aviso.mensajeVentanaAviso('LIBRO MODIFICADO')
                eventos.Aviso.abrirVentanaAviso(self)
                conexion.Libros.mostrarLibros(self)
            else:
                print('NO EXISTE EL LIBRO')
                if var.ui.lineEditCodigo.text() == '':
                    print("NO HA INTRODUCIDO NINGÚN CÓDIGO")
                    eventos.Aviso.mensajeVentanaAviso("NO HA INTRODUCIDO NINGÚN CÓDIGO DE LIBRO\nEN LA BARRA DE BÚSQUEDA")
                    eventos.Aviso.abrirVentanaAviso(self)
                    #var.ui.tbEstado.setText("NO HA INTRODUCIDO NINGÚN CÓDIGO")
                else:
                    eventos.Aviso.mensajeVentanaAviso("LIBRO CON CÓDIGO '" + libro[0].text()+ "' NO EXISTE EN LA BIBLIOTECA")
                    eventos.Aviso.abrirVentanaAviso(self)
                    print("LIBRO CON CÓDIGO '" + libro[0].text()+ "' NO EXISTE EN LA BD")
        except Exception as error:
            print('Error modificando libro: %s' % str(error))


    def limpiarLibro(self):
        '''Vacía todos los campos del formulario libro de la interfaz gráfica'''

        var.ui.lineEditCodigo.setText("")
        var.ui.lineEditTitulo.setText("")
        var.ui.lineEditAutor.setText("")
        var.ui.comboBoxGenero.setCurrentIndex(0)
        var.ui.labelCodigoGenerado.setText("")
        var.ui.spinBoxEstado.setValue(0)
        var.ui.checkBoxAventuras.setChecked(False)
        var.ui.checkBoxFantasia.setChecked(False)
        var.ui.checkBoxFilosofia.setChecked(False)
        var.ui.checkBoxIntriga.setChecked(False)
        var.ui.checkBoxHistorica.setChecked(False)
        var.ui.checkBoxRomantica.setChecked(False)
        var.ui.pushButtonModificarLibro.setHidden(True)
        var.ui.pushButtonEliminarLibro.setHidden(True)



    def buscarLibroCodigo(self):
        '''Recoge el código del libro introducido por el ususario y devuelve los valores del libro en los
        distintos campos del formulario y en la tabla de la interfaz gráfica'''

        id = var.ui.lineEditCodigo.text()
        if conexion.Libros.existeLibro(id):
            conexion.Libros.buscarLibroCodigo(id)

            Libros.limpiarLibro(self)

            var.ui.lineEditCodigo.setText(str(var.codigo))
            var.ui.labelCodigoGenerado.setText(str(var.codigo))
            var.ui.lineEditTitulo.setText(var.titulo)
            var.ui.lineEditAutor.setText(var.autor)

            var.ui.pushButtonModificarLibro.setHidden(False)
            var.ui.pushButtonEliminarLibro.setHidden(False)

            if (var.estado == 'DISPONIBLE'):
                var.ui.spinBoxEstado.setValue(0)
            elif (var.estado == 'NO DISPONIBLE/PRESTADO'):
                var.ui.spinBoxEstado.setValue(1)

            if (var.genero == ""):
                var.ui.comboBoxGenero.setCurrentIndex(0)
            elif (var.genero == "Narrativa"):
                var.ui.comboBoxGenero.setCurrentIndex(1)
            elif (var.genero == "Teatro"):
                var.ui.comboBoxGenero.setCurrentIndex(2)
            elif (var.genero == "Poesía"):
                var.ui.comboBoxGenero.setCurrentIndex(3)
            elif (var.genero == "Ensayo"):
                var.ui.comboBoxGenero.setCurrentIndex(4)

            if 'Aventuras' in var.etiqueta:
                var.ui.checkBoxAventuras.setChecked(True)
            if 'Romántica' in var.etiqueta:
                var.ui.checkBoxRomantica.setChecked(True)
            if 'Histórica' in var.etiqueta:
                var.ui.checkBoxHistorica.setChecked(True)
            if 'Intriga' in var.etiqueta:
                var.ui.checkBoxIntriga.setChecked(True)
            if 'Fantasía' in var.etiqueta:
                var.ui.checkBoxFantasia.setChecked(True)
            if 'Filosofía' in var.etiqueta:
                var.ui.checkBoxFilosofia.setChecked(True)

        else:
            Libros.limpiarLibro(self)
            var.ui.lineEditCodigo.setText(id)
            conexion.Libros.mostrarLibros(self)
            eventos.Aviso.mensajeVentanaAviso("LIBRO CON CÓDIGO '" + id+ "' NO EXISTE EN LA BIBLIOTECA ")
            eventos.Aviso.abrirVentanaAviso(self)
            print('NO EXISTE EL LIBRO EN LA DB ')

    def buscarLibroTitulo(self):
        '''Recoge el título del libro introducido por el ususario y devuelve los datos del libro
        o libros coincidentes con ese título en la tabla de la interfaz gráfica'''

        titulo = var.ui.lineEditTitulo.text().upper()
        if conexion.Libros.existeLibroTitulo(titulo):
            conexion.Libros.buscarLibroTitulo(titulo)

            Libros.limpiarLibro(self)

            var.ui.lineEditTitulo.setText(titulo)
        else:
            Libros.limpiarLibro(self)
            var.ui.lineEditTitulo.setText(titulo)
            conexion.Libros.mostrarLibros(self)
            eventos.Aviso.mensajeVentanaAviso("EL LIBRO '"+titulo.upper()+"' NO EXISTE EN LA BIBLIOTECA")
            eventos.Aviso.abrirVentanaAviso(self)
            print('NO EXISTE EL LIBRO EN LA DB ')

    def buscarLibroAutor(self):
        '''Recoge el autor del libro introducido por el ususario y devuelve los datos del libro
               o libros coincidentes con ese autor en la tabla de la interfaz gráfica'''

        autor = var.ui.lineEditAutor.text().upper()
        if conexion.Libros.existeLibroAutor(autor):
            conexion.Libros.buscarLibroAutor(autor)

            Libros.limpiarLibro(self)

            var.ui.lineEditAutor.setText(autor)
        else:
            Libros.limpiarLibro(self)
            var.ui.lineEditAutor.setText(autor)
            conexion.Libros.mostrarLibros(self)
            eventos.Aviso.mensajeVentanaAviso("NO EXISTEN LIBROS DEL AUTOR '"+autor.upper()+"' EN LA BIBLIOTECA")
            eventos.Aviso.abrirVentanaAviso(self)
            print('NO EXISTEN LIBROS DEL AUTOR '+autor.upper()+' EN LA BIBLIOTECA')


    def buscarLibroGenero(self):
        '''Recoge el género del libro introducido por el ususario y devuelve los datos del libro
               o libros coincidentes con ese género en la tabla de la interfaz gráfica'''

        genero = var.generoLibro
        if conexion.Libros.existeLibroGenero(genero):
            conexion.Libros.buscarLibroGenero(genero)

            Libros.limpiarLibro(self)

            if (var.genero == ""):
                var.ui.comboBoxGenero.setCurrentIndex(0)
            elif (var.genero == "Narrativa"):
                var.ui.comboBoxGenero.setCurrentIndex(1)
            elif (var.genero == "Teatro"):
                var.ui.comboBoxGenero.setCurrentIndex(2)
            elif (var.genero == "Poesía"):
                var.ui.comboBoxGenero.setCurrentIndex(3)
            elif (var.genero == "Ensayo"):
                var.ui.comboBoxGenero.setCurrentIndex(4)
        else:
            eventos.Aviso.mensajeVentanaAviso('NO HAY LIBROS DEL GÉNERO '+var.generoLibro.upper()+' EN LA BIBLIOTECA')
            eventos.Aviso.abrirVentanaAviso(self)
            print('NO HAY LIBROS DEL GÉNERO'+var.generoLibro.upper()+' EN LA BIBLIOTECA')
            Libros.limpiarLibro(self)
            if (var.generoLibro == ""):
                var.ui.comboBoxGenero.setCurrentIndex(0)
            elif (var.generoLibro == "Narrativa"):
                var.ui.comboBoxGenero.setCurrentIndex(1)
            elif (var.generoLibro == "Teatro"):
                var.ui.comboBoxGenero.setCurrentIndex(2)
            elif (var.generoLibro == "Poesía"):
                var.ui.comboBoxGenero.setCurrentIndex(3)
            elif (var.generoLibro == "Ensayo"):
                var.ui.comboBoxGenero.setCurrentIndex(4)
            conexion.Libros.mostrarLibros(self)


    def buscarLibroEstado(self):
        '''Recoge el estado del libro introducido por el ususario y devuelve los datos del libro
               o libros coincidentes con ese estado en la tabla de la interfaz gráfica'''

        estado = var.estadoLibro
        if conexion.Libros.existeLibroEstado(estado):
            conexion.Libros.buscarLibroEstado(estado)

            Libros.limpiarLibro(self)

            if (var.estado == 'DISPONIBLE'):
                var.ui.spinBoxEstado.setValue(0)
            elif (var.estado == 'NO DISPONIBLE/PRESTADO'):
                var.ui.spinBoxEstado.setValue(1)
        else:
            eventos.Aviso.mensajeVentanaAviso('NO HAY LIBROS ' + var.estadoLibro + 'S EN LA BIBLIOTECA')
            eventos.Aviso.abrirVentanaAviso(self)
            print('NO HAY LIBROS ' + var.estadoLibro + 'S ')
            Libros.limpiarLibro(self)
            if (var.estadoLibro == 'DISPONIBLE'):
                var.ui.spinBoxEstado.setValue(0)
            elif (var.estadoLibro == 'NO DISPONIBLE/PRESTADO'):
                var.ui.spinBoxEstado.setValue(1)
            conexion.Libros.mostrarLibros(self)
