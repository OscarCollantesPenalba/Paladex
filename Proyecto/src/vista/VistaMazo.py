from PyQt5 import QtWidgets, uic

class VistaMazo(QtWidgets.QMainWindow):
    def __init__(self):
        super(VistaMazo, self).__init__()
        uic.loadUi('src/vista/Ui/crear_mazo.ui', self)