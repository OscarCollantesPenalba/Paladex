from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from src.modelo.Logica import Logica

# Cargar la interfaz generada desde el archivo .ui
Form, Window = uic.loadUiType("./src/vista/Ui/VistaLogReg.ui")

class MiVentana(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa los widgets
        self.setWindowTitle("Paladex")
        self.controlador = None
        # Boton Inicio Sesión
        self.BotonInicioSesion.clicked.connect(self.log_in)
        #Boton acceder registrase
        self.BotonRegister.clicked.connect(self.go_register)
        #boton Registrarse
        self.BotonRegister_2.clicked.connect(self.sign_up)
        #Boton volver inicio sesion
        self.LabelCancelar.mousePressEvent = self.back_login
    

    def go_register (self):
        self.QStackedWidget.setCurrentIndex(1)

    def volver_login(self):
        self.QStackedWidget.setCurrentIndex(0)
        
    def back_login(self, event):
        self.QStackedWidget.setCurrentIndex(0)

    def log_in(self):
        self.controlador.comprobarLogin(self.Usuario.text(), self.Contrasena.text())
        
    def login_incorrecto(self):
        QMessageBox.information(self, "Info", "Login incorrecto")

    def login_vacio(self):
        QMessageBox.critical(self,"Error", "Rellena todos los campos")
    
    def sign_up (self):
        self.controlador.comprobarRegistro(
                                self.NombreCompleto.text(),
                                self.Usuario_2.text(),
                                self.Correo.text(),
                                self.Contrasena_2.text(),
                                self.ConfirmContrasena.text())
    def sign_vacio(self):
        QMessageBox.critical(self,"Error","Rellena todos los campos")

    def contrasenas_diferentes(self):
        QMessageBox.critical(self,"Error","Las contraseñas deben coincidir")

    def contrasena_pequena(self):
        QMessageBox.critical(self, "Error", "La contraseña debe tener al menos 8 caracteres")

    def usuario_email_existentes(self):
        QMessageBox.information(self, "Error", "El usuario o email ya existen")
        
    def email_correcto(self):
        QMessageBox.critical(self, "Error", "El email no tiene el formato correcto")
        
    @property
    def controlador(self):
        return self._controlador
    
    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador