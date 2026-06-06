import os
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi


class DialogNovedades(QDialog):

    UI_PATH = os.path.join(os.path.dirname(__file__), "ui", "DialogNovedades.ui")

    def __init__(self, datos, parent=None):
        super().__init__(parent)
        loadUi(self.UI_PATH, self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.DlgTitulo.setText(datos.get("titulo", ""))
        self.DlgSubtitulo.setText(datos.get("subtitulo", ""))
        self.DlgDescripcion.setPlainText(datos.get("descripcion", ""))
        self.BtnCerrar.clicked.connect(self.close)

    def mostrar_arriba_derecha(self, ventana_padre):
        geo = ventana_padre.frameGeometry()
        x = geo.x() + geo.width() - self.width() - 10
        y = geo.y() + 40
        self.move(x, y)
        self.exec_()