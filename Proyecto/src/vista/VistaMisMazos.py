from PyQt5 import QtWidgets, uic

class VistaMisMazos(QtWidgets.QMainWindow):
    def __init__(self):
        super(VistaMisMazos, self).__init__()
        uic.loadUi('src/vista/Ui/mis_mazos.ui', self)