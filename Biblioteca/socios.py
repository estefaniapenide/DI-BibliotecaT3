import eventos
import var
from dni import Dni
from PyQt5.QtGui import QFont
import conexion

#GESTIÓN DE SOCIOS
class Socios:

    def visibilidadFechaSancion(self):
        '''Muestra o oculta el campo de fecha de sanción de la interfaz gráfica en función de si se le quiere añadir
        una multa al socio o no'''

        if var.multaSocio==True:
            Socios.mostrarFechaSancion(self)
        if var.multaSocio==False:
            Socios.esconderFechaSancion(self)

    def esconderFechaSancion(self):
        '''Esconde el campo y la eqiqueta de fecha de sanción, así como el botón de selección de fecha
        de sanción de la interfaz gráfica'''

        var.ui.textBrowserSancionHasta.setText('')
        var.ui.labelSancionHasta.setHidden(True)
        var.ui.textBrowserSancionHasta.setHidden(True)
        var.ui.pushButtonSancionHasta.setHidden(True)

    def mostrarFechaSancion(self):
        '''Muestra el campo y la eqiqueta de fecha de sanción, así como el botón de selección de fecha
        de sanción de la interfaz gráfica'''

        var.ui.labelSancionHasta.setHidden(False)
        var.ui.textBrowserSancionHasta.setHidden(False)
        var.ui.pushButtonSancionHasta.setHidden(False)

    def seleccionarMulta(self):
        '''Selecciona si un socio tiene multa o no en función de lo marcado en la interfaz gráfica por el ususario'''

        try:
            if var.ui.radioButtonMultaSi.isChecked():
                var.multaSocio=True
            if var.ui.radioButtonMultaNo.isChecked():
                var.multaSocio=False
        except Exception as error:
            print('Error en módulo seleccionar multa:',error)

    def seleccionarSexo(self):
        '''Selecciona el sewxo del socio en función de lo marcado en la interfaz gráfica por el ususario'''

        try:
            if var.ui.radioButtonMujer.isChecked():
                var.sexoSocio='Mujer'
            if var.ui.radioButtonHombre.isChecked():
                var.sexoSocio='Hombre'
        except Exception as error:
            print('Error en módulo seleccionar sexo:',error)

    def seleccionarNumLibros(self):
        '''Selecciona el número de libros que un socio tiene prestados en función
        de lo marcado en la interfaz gráfica por el ususario'''

        try:
            var.numLibrosSocio = var.ui.spinBoxNumLibros.value()
        except Exception as error:
            print('Error seleccionar numero de libros prestados: %s' % str(error))

    def validarDNI():
        '''Comprueba la validez de un DNI introducido por el usuario en la interfaz gráfica'''

        try:
            dni=var.ui.lineEditDni.text()
            var.ui.lineEditDni.setText(dni.upper())
            if (len(dni) == 9):
                numero = ""
                i = 0
                while (i < 8):
                    numero = numero + dni[i]
                    i += 1
                letra = dni[8]
                letra=letra.upper()
                dniCorrecto = Dni(numero)
                if (dniCorrecto.letra == letra):
                    print("DNI CORRECTO")
                    var.ui.labelValidarDni.setStyleSheet('QLabel {color:green;font-size:14pt;font-weight:bold}')
                    var.ui.labelValidarDni.setFont(QFont("Forte"))
                    var.ui.labelValidarDni.setText('V')
                    return True
                else:
                    print("DNI INCORRECTO")
                    var.ui.labelValidarDni.setStyleSheet('QLabel {color:red;font-size:14pt;font-weight:bold}')
                    var.ui.labelValidarDni.setFont(QFont("Forte"))
                    var.ui.labelValidarDni.setText('X')
                    return False
            else:
                print("DNI INCORRECTO")
                var.ui.labelValidarDni.setStyleSheet('QLabel {color:red;font-size:14pt;font-weight:bold}')
                var.ui.labelValidarDni.setFont(QFont("Forte"))
                var.ui.labelValidarDni.setText('X')
                return False
        except Exception as error:
            print("Error validar dni: %s " % str(error))

    def guardarSocio(self):
        '''Recoge los datos que ha introducido el usuario para guardar el socio y guarda el socio'''

        if Socios.validarDNI():
            try:
                socio = [var.ui.lineEditDni.text(), var.ui.lineEditNombre.text().upper(), var.ui.lineEditApellidos.text().upper(), var.ui.lineEditDireccion.text().upper(), var.sexoSocio, str(var.multaSocio),var.ui.textBrowserSancionHasta.toPlainText(),str(var.numLibrosSocio)]

                conexion.Socios.guardarSocio(socio)
                Socios.buscarSocioDni(self)
                conexion.Socios.mostrarSocios(self)

            except Exception as error:
                print('Error guardar socio (socios): %s ' % str(error))
        else:
            eventos.Aviso.mensajeVentanaAviso("EL DNI INTRODUCIDO NO ES VÁLIDO")
            eventos.Aviso.abrirVentanaAviso(self)

    def modificarSocio(self):
        '''Recoge los datos que ha introducido el usuario para modificar el socio y modifica el socio'''

        if Socios.validarDNI():
            try:
                socio = [var.ui.labelNumSocioGenerado.text(), var.ui.lineEditDni.text(), var.ui.lineEditNombre.text().upper(), var.ui.lineEditApellidos.text().upper(), var.ui.lineEditDireccion.text().upper(), var.sexoSocio, str(var.multaSocio),var.ui.textBrowserSancionHasta.toPlainText(),str(var.numLibrosSocio)]
                if (conexion.Socios.existeSocioNumero(socio[0])):
                    conexion.Socios.modificarSocio(socio)
                    eventos.Aviso.mensajeVentanaAviso('SOCIO MODIFICADO')
                    eventos.Aviso.abrirVentanaAviso(self)
                    conexion.Socios.mostrarSocios(self)
                else:
                    print('NO EXISTE EL SOCIO')
                    if var.ui.labelNumSocioGenerado.text() == '':
                        print("NO HA INTRODUCIDO NINGÚN NÚMERO DE SOCIO")
                        eventos.Aviso.mensajeVentanaAviso("NO HA INTRODUCIDO NINGÚN NÚMERO DE SOCIO\nEN LA BARRA DE BÚSQUEDA")
                        eventos.Aviso.abrirVentanaAviso(self)
                    else:
                        eventos.Aviso.mensajeVentanaAviso("NO EXISTE EL SOCIO '" + socio[0].text()+ "' EN LA BIBLIOTECA")
                        eventos.Aviso.abrirVentanaAviso(self)
                        print("NO EXISTE EL SOCIO " + socio[0].text()+ " EN LA BD")
            except Exception as error:
                print('Error modificando socio: %s' % str(error))
        else:
            eventos.Aviso.mensajeVentanaAviso("EL DNI INTRODUCIDO NO ES VÁLIDO")
            eventos.Aviso.abrirVentanaAviso(self)

    def eliminarSocio(self):
        '''Recoge el dato de número de socio indicado por el usuario para eliminar el socio y elimina el socio'''

        try:
            numSocio = var.ui.labelNumSocioGenerado.text()
            if (conexion.Socios.existeSocioNumero(numSocio)):
                conexion.Socios.bajaSocio(numSocio)
                eventos.Aviso.mensajeVentanaAviso("SOCIO ELIMINADO")
                eventos.Aviso.abrirVentanaAviso(self)
                conexion.Socios.mostrarSocios(self)
                Socios.limpiarSocio(self)
            else:
                print('NO EXISTE EL SOCIO')
                if var.ui.labelNumSocioGenerado.text()=='':
                    print("NO HA INTRODUCIDO NINGÚN NÚMERO DE SOCIO")
                    eventos.Aviso.mensajeVentanaAviso("NO HA INTRODUCIDO NINGÚN NÚMERO DE SOCIO\nEN LA BARRA DE BÚSQUEDA")
                    eventos.Aviso.abrirVentanaAviso(self)
                else:
                    print("SOCIO CON NÚMERO '" + numSocio + "' NO EXISTE EN LA BD")
                    eventos.Aviso.mensajeVentanaAviso("NO EXISTE EL SOCIO '" + numSocio + "' EN LA BIBLIOTECA")
                    eventos.Aviso.abrirVentanaAviso(self)
        except Exception as error:
            print('Error eliminar socio: %s' % str(error))

    def buscarSocioNum(self):
        '''Recoge el número de socio introducido por el ususario y devuelve los valores del socio en los
            distintos campos del formulario y en la tabla de la interfaz gráfica'''

        id = var.ui.lineEditNumeroSocio.text()
        if conexion.Socios.existeSocioNumero(id):
            conexion.Socios.buscarSocioNumero(id)

            Socios.limpiarSocio(self)

            var.ui.lineEditDni.setText(var.dni)
            var.ui.lineEditNumeroSocio.setText(str(var.numSocio))
            var.ui.labelNumSocioGenerado.setText(str(var.numSocio))
            var.ui.lineEditNombre.setText(var.nombre)
            var.ui.lineEditApellidos.setText(var.apellidos)
            var.ui.lineEditDireccion.setText(var.direccion)
            var.ui.spinBoxNumLibros.setValue(var.numLibros)
            var.ui.textBrowserSancionHasta.setText(var.fmulta)

            if (var.sexo == 'Mujer'):
                var.ui.radioButtonMujer.click()
            elif (var.sexo == 'Hombre'):
                var.ui.radioButtonHombre.click()

            if(var.multa=='True'):
                var.ui.radioButtonMultaSi.click()
            if(var.multa=='False'):
                var.ui.radioButtonMultaNo.click()


            var.ui.pushButtonModificarSocio.setHidden(False)
            var.ui.pushButtonEliminarSocio.setHidden(False)

        else:
            Socios.limpiarSocio(self)
            var.ui.lineEditNumeroSocio.setText(id)
            conexion.Socios.mostrarSocios(self)
            eventos.Aviso.mensajeVentanaAviso("NO EXISTE EL SOCIO '" + id + "' EN LA BIBLIOTECA")
            eventos.Aviso.abrirVentanaAviso(self)

    def buscarSocioDni(self):
        '''Recoge el DNI introducido por el ususario y devuelve los valores del socio en los
        distintos campos del formulario y en la tabla de la interfaz gráfica'''

        if Socios.validarDNI():
            dni = var.ui.lineEditDni.text()
            if conexion.Socios.existeSocioDni(dni):
                conexion.Socios.buscarSocioDni(dni)

                Socios.limpiarSocio(self)

                var.ui.lineEditDni.setText(var.dni)
                var.ui.labelNumSocioGenerado.setText(str(var.numSocio))
                var.ui.lineEditNombre.setText(var.nombre)
                var.ui.lineEditApellidos.setText(var.apellidos)
                var.ui.lineEditDireccion.setText(var.direccion)
                var.ui.spinBoxNumLibros.setValue(var.numLibros)
                var.ui.textBrowserSancionHasta.setText(var.fmulta)

                if (var.sexo == 'Mujer'):
                    var.ui.radioButtonMujer.click()
                elif (var.sexo == 'Hombre'):
                    var.ui.radioButtonHombre.click()

                if (var.multa == 'True'):
                    var.ui.radioButtonMultaSi.click()
                if (var.multa == 'False'):
                    var.ui.radioButtonMultaNo.click()

                var.ui.pushButtonModificarSocio.setHidden(False)
                var.ui.pushButtonEliminarSocio.setHidden(False)

            else:
                Socios.limpiarSocio(self)
                var.ui.lineEditDni.setText(dni)
                conexion.Socios.mostrarSocios(self)


    def limpiarSocio(self):
        '''Vacía todos los campos del formulario socio de la interfaz gráfica'''

        var.ui.lineEditNumeroSocio.setText("")
        var.ui.labelNumSocioGenerado.setText("")
        var.ui.lineEditDni.setText("")
        var.ui.labelValidarDni.setText("")
        var.ui.lineEditNombre.setText("")
        var.ui.lineEditApellidos.setText("")
        var.ui.lineEditDireccion.setText("")
        Socios.esconderFechaSancion(self)

        var.ui.buttonGroupMulta.setExclusive(False)
        var.ui.radioButtonMultaNo.setChecked(True)
        var.ui.radioButtonMultaSi.setChecked(False)
        var.ui.buttonGroupMulta.setExclusive(True)

        var.ui.buttonGroupSexo.setExclusive(False)
        var.ui.radioButtonHombre.setChecked(False)
        var.ui.radioButtonMujer.setChecked(False)
        var.ui.buttonGroupSexo.setExclusive(True)

        var.ui.spinBoxNumLibros.setValue(0)

        var.ui.pushButtonModificarSocio.setHidden(True)
        var.ui.pushButtonEliminarSocio.setHidden(True)
