
import eventos
import libros
import var
import conexion
import prestamos
import socios
import imprimir
import ventanaSalir
from ventanaBiblioteca import *
import ventanaCalendarioPrestamo
import ventanaCalendarioDevolucion
import ventanaCalendarioSancion
import ventanaAviso
import sys
from datetime import datetime


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_MainWindow()
        var.ui.setupUi(self)

        #****************************ACCIONES DE LA TOOLBAR***********************************
        var.ui.actionactualizar.triggered.connect(libros.Libros.limpiarLibro)
        var.ui.actionactualizar.triggered.connect(conexion.Libros.mostrarLibros)
        var.ui.actionactualizar.triggered.connect(prestamos.Prestamos.limpiarPrestamos)
        var.ui.actionactualizar.triggered.connect(conexion.Prestamos.mostrarPrestamos)
        var.ui.actionactualizar.triggered.connect(socios.Socios.limpiarSocio)
        var.ui.actionactualizar.triggered.connect(conexion.Socios.mostrarSocios)

        var.ui.actionSalir.triggered.connect(eventos.Salir.preguntaSalir)
        var.ui.actionImprimir_lista_pr_stamos_PDF.triggered.connect(imprimir.Imprimir.informePrestamos)
        var.ui.actionImprimir_lista_Libros_PDF.triggered.connect(imprimir.Imprimir.informeLibros)
        var.ui.actionImprimir_lista_socios_PDF.triggered.connect(imprimir.Imprimir.informeSocios)
        var.ui.actioncomprimir.triggered.connect(eventos.Comprimir.BackupBaseDatos)
        var.ui.actionAbrir.triggered.connect(eventos.Abrir.abrirExplorador)


        #************************************+CONEXIÓN BD***********************************************
        var.filedb = 'biblioteca.db'
        conexion.Conexion.db_connect(var.filedb)
        conexion.Socios.actualizarSocios(self)
        conexion.Libros.mostrarLibros(self)
        conexion.Prestamos.mostrarPrestamos(self)
        conexion.Socios.mostrarSocios(self)
        #**************************************************************************************************+



        #***************************************PRÉSTAMOS******************************************
        #Seleccionar fechas préstamo y devolución
        var.ui.pushButtonCalendario.clicked.connect(eventos.Calendario.abrirCalendarioPrestamo)
        var.ui.pushButtonCalendarioDevolucion.clicked.connect(eventos.Calendario.abrirCalendarioDevolucion)
        # Botones guardar, modificar, limpiar
        var.ui.pushButtonGuardarPrestamo.clicked.connect(prestamos.Prestamos.guardarPrestamo)
        var.ui.pushButtonGuardarDevolucion.clicked.connect(prestamos.Prestamos.modificarPrestamo)
        var.ui.pushButtonLimpiarPrestamos.clicked.connect(prestamos.Prestamos.limpiarPrestamos)
        #****************************************************************************************************



        #*****************************************LIBROS****************************************
        var.ui.pushButtonModificarLibro.setHidden(True)
        var.ui.pushButtonEliminarLibro.setHidden(True)
        #Seleccionar género
        var.generoLibro='' #Género predeterminado
        libros.Libros.cargarGenero(self)
        var.ui.comboBoxGenero.currentIndexChanged[str].connect(libros.Libros.seleccionarGenero)
        # Seleccionar estado
        var.estadoLibro = 'DISPONIBLE'  # Estado predeterminado
        var.ui.spinBoxEstado.valueChanged.connect(libros.Libros.seleccionarEstado)
        #Seleccionar etiquetas
        var.etiquetas = []#Sin etiquetas de forma predeterminada
        libros.Libros.marcarEtiquetas(self)
        #Botones guardar, elimninar, modificar, limpiar
        var.ui.pushButtonGuardarLibro.clicked.connect(libros.Libros.guardarLibro)
        var.ui.pushButtonLimpiarLibros.clicked.connect(libros.Libros.limpiarLibro)
        var.ui.pushButtonLimpiarLibros.clicked.connect(conexion.Libros.mostrarLibros)
        var.ui.pushButtonEliminarLibro.clicked.connect(libros.Libros.eliminarLibro)
        var.ui.pushButtonModificarLibro.clicked.connect(libros.Libros.modificarLibro)
        #Búsquedas
        var.ui.pushButtonBuscarCodigo.clicked.connect(libros.Libros.buscarLibroCodigo)
        var.ui.pushButtonBuscarTitulo.clicked.connect(libros.Libros.buscarLibroTitulo)
        var.ui.pushButtonBuscarAutor.clicked.connect(libros.Libros.buscarLibroAutor)
        var.ui.pushButtonBuscarGenero.clicked.connect(libros.Libros.buscarLibroGenero)
        var.ui.pushButtonBuscarEstado.clicked.connect(libros.Libros.buscarLibroEstado)
        # ****************************************************************************************************



        # ***************************************SOCIOS******************************************
        var.ui.pushButtonModificarSocio.setHidden(True)
        var.ui.pushButtonEliminarSocio.setHidden(True)
        # Seleccionar fecha sanción
        var.ui.pushButtonSancionHasta.clicked.connect(eventos.Calendario.abrirCalendarioSancion)
        # Seleccionar Multa y visibilidad Sanción Hasta
        socios.Socios.seleccionarMulta(self)
        socios.Socios.visibilidadFechaSancion(self)
        var.ui.buttonGroupMulta.buttonToggled.connect(socios.Socios.seleccionarMulta)
        var.ui.buttonGroupMulta.buttonToggled.connect(socios.Socios.visibilidadFechaSancion)
        #Seleccionar sexo
        var.sexoSocio = 'Mujer'#Sexo predeterminado
        var.ui.buttonGroupSexo.buttonClicked.connect(socios.Socios.seleccionarSexo)
        #Seleccionar numero libros prestados
        var.numLibrosSocio=0 #Valor por defecto
        var.ui.spinBoxNumLibros.valueChanged.connect(socios.Socios.seleccionarNumLibros)
        #Validar DNI
        var.ui.lineEditDni.editingFinished.connect(socios.Socios.validarDNI)
        # Botones guardar, elimninar, modificar, limpiar
        var.ui.pushButtonGuardarSocio.clicked.connect(socios.Socios.guardarSocio)
        var.ui.pushButtonLimpiarSocios.clicked.connect(socios.Socios.limpiarSocio)
        var.ui.pushButtonLimpiarSocios.clicked.connect(conexion.Socios.mostrarSocios)
        var.ui.pushButtonEliminarSocio.clicked.connect(socios.Socios.eliminarSocio)
        var.ui.pushButtonModificarSocio.clicked.connect(socios.Socios.modificarSocio)
        # Búsquedas
        var.ui.pushButtonBuscarDni.clicked.connect(socios.Socios.buscarSocioDni)
        var.ui.pushButtonBuscarNumSocio.clicked.connect(socios.Socios.buscarSocioNum)
        # ****************************************************************************************************

class CalendarioPrestamo(QtWidgets.QDialog):

    def __init__(self):
        super(CalendarioPrestamo,self).__init__()
        var.uiCalendarioPrestamo = ventanaCalendarioPrestamo.Ui_Dialog()
        var.uiCalendarioPrestamo.setupUi(self)
        diaActual=datetime.now().day
        mesActual=datetime.now().month
        anoActual=datetime.now().year

        #PRÉSTAMOS
        var.uiCalendarioPrestamo.calendarioPrestamo.setSelectedDate(QtCore.QDate(anoActual,mesActual,diaActual))
        var.uiCalendarioPrestamo.calendarioPrestamo.clicked.connect(eventos.Calendario.cargarFechaDesde)
        var.uiCalendarioPrestamo.calendarioPrestamo.clicked.connect(eventos.Calendario.cargarFechaHasta)

class CalendarioDevolucion(QtWidgets.QDialog):

    def __init__(self):
        super(CalendarioDevolucion,self).__init__()
        var.uiCalendarioDevolucion = ventanaCalendarioDevolucion.Ui_Dialog()
        var.uiCalendarioDevolucion.setupUi(self)
        diaActual=datetime.now().day
        mesActual=datetime.now().month
        anoActual=datetime.now().year

        #DEVOLUCIÓN
        var.uiCalendarioDevolucion.calendarioDevolucion.setSelectedDate(QtCore.QDate(anoActual,mesActual,diaActual))
        var.uiCalendarioDevolucion.calendarioDevolucion.clicked.connect(eventos.Calendario.cargarFechaDevolucion)

class CalendarioSancion(QtWidgets.QDialog):

    def __init__(self):
        super(CalendarioSancion,self).__init__()
        var.uiCalendarioSancion = ventanaCalendarioSancion.Ui_Dialog()
        var.uiCalendarioSancion.setupUi(self)
        diaActual=datetime.now().day
        mesActual=datetime.now().month
        anoActual=datetime.now().year

        #SANCIÓN
        var.uiCalendarioSancion.calendarioSancion.setSelectedDate(QtCore.QDate(anoActual,mesActual,diaActual))
        var.uiCalendarioSancion.calendarioSancion.clicked.connect(eventos.Calendario.cargarFechaSancion)


class Aviso(QtWidgets.QMessageBox):
    def __init__(self):
        super(Aviso,self).__init__()
        var.uiAviso = ventanaAviso.Ui_DialogAviso()
        var.uiAviso.setupUi(self)


class DialogoAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(DialogoAbrir,self).__init__()
        self.setWindowTitle('Abrir')

class Salir(QtWidgets.QDialog):

    def __init__(self):
        super(Salir,self).__init__()
        var.uiSalir = ventanaSalir.Ui_Dialog()
        var.uiSalir.setupUi(self)



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    var.uiCalendarioPrestamo = CalendarioPrestamo()
    var.uiCalendarioDevolucion = CalendarioDevolucion()
    var.uiCalendarioSancion = CalendarioSancion()
    var.uiAviso = Aviso()
    var.uiAbrir = DialogoAbrir()
    var.uiSalir = Salir()
    window.show()
    sys.exit(app.exec())
