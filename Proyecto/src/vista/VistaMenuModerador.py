from PyQt5 import QtWidgets, uic

class VistaMenuModerador(QtWidgets.QMainWindow):
    def __init__(self):
        super(VistaMenuModerador, self).__init__()
        uic.loadUi('src/vista/Ui/menu_moderador.ui', self)