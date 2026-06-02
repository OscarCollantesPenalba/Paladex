from PyQt5 import QtWidgets, uic

class VistaMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super(VistaMenu, self).__init__()
        uic.loadUi('src/vista/Ui/menu_principal.ui', self)