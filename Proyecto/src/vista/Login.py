from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

import os
print(os.getcwd())

# Cargar la interfaz generada desde el archivo .ui
Form, Window = uic.loadUiType("./src/vista/Ui/VistaLogReg.ui")

class MiVentana(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa los widgets

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
    
    def back_login(self,event):
        self.QStackedWidget.setCurrentIndex(0)

    def log_in(self):
        pass#hacer el log_in        

    def sign_up (self):
        pass #hacer el sign up


if __name__ == "__main__":
    app = QApplication([])
    ventana = MiVentana()
    ventana.show()
    app.exec_()