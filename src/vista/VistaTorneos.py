from PyQt5 import QtWidgets, uic

class VistaTorneos(QtWidgets.QMainWindow):
    def __init__(self):
        super(VistaTorneos, self).__init__()
        uic.loadUi('src/vista/Ui/torneos.ui', self)