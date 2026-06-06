from PyQt5 import QtWidgets, uic

class VistaPerfil(QtWidgets.QMainWindow):
    def __init__(self):
        super(VistaPerfil, self).__init__()
        uic.loadUi('src/vista/Ui/perfil.ui', self)