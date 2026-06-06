from PyQt5 import QtWidgets, uic

class VistaMenuAdmin(QtWidgets.QMainWindow):
    def __init__(self):
        super(VistaMenuAdmin, self).__init__()
        uic.loadUi('src/vista/Ui/menu_admin.ui', self)