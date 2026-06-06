import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from src.modelo.vo.UsuarioVo import UsuarioVO
from src.modelo.Logica import Logica
from src.vista.Login import MiVentana
from src.controlador.ControladorPrincipal import ControladorPrincipal





if __name__ == "__main__":
    app = QApplication([])
    ventana = MiVentana()
    ventana.show()
    modelo = Logica()
    controlador = ControladorPrincipal(ventana, modelo)
    ventana.controlador = controlador
    controlador.abrirIniciarSesion()
    
    app.exec_()

