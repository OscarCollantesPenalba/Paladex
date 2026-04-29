from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from src.modelo.vo.LoginVo import LoginVo

# Cargar la interfaz generada desde el archivo .ui
Form, Window = uic.loadUiType("./src/vista/Ui/Login.ui")

class MiVentana(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa los widgets

        # Conectar el botón a la función
        self.Boton.clicked.connect(self.on_button_click)


    def on_button_click(self):
        print("Botón presionado")
        texto_correo = self.correo.text() #Obtenet el texto del campo nombre
        texto_contrasena = self.contrasenha.text() #falta poner el nombre, mirar lo de lucas

        print("El texto es: ")
        print(texto_correo)

        login = LoginVo(texto_correo, texto_contrasena)
        print("correcto")
        return login


if __name__ == "__main__":
    app = QApplication([])
    ventana = MiVentana()
    ventana.show()
    app.exec_()