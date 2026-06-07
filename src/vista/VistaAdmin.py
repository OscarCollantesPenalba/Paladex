import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi


class VistaAdmin(QMainWindow):

    UI_PATH = os.path.join(os.path.dirname(__file__), "ui", "menu_admin.ui")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__controlador = None
        loadUi(self.UI_PATH, self)
        self._conectar_senales()

    @property
    def controlador(self):
        return self.__controlador

    @controlador.setter
    def controlador(self, ctrl):
        self.__controlador = ctrl

    def _conectar_senales(self):
        self.btnEliminarMod.clicked.connect(
            lambda: self.__controlador.eliminar_moderador(self.listModeradores.currentRow()))
        self.btnEliminarCreador.clicked.connect(
            lambda: self.__controlador.degradar_creador(self.listCreadoresMazos.currentRow()))
        self.btnAscenderModerador.clicked.connect(
            lambda: self.__controlador.ascender_a_moderador(self.listUsuariosBase.currentRow()))
        self.btnCerrarSesionAdmin.clicked.connect(
            lambda: self.__controlador.cerrar_sesion())
        self.tabWidget.currentChanged.connect(self._on_cambiar_tab)

    def _on_cambiar_tab(self, indice):
        if self.__controlador:
            self.__controlador.cambiar_tab(indice)

    # ------------------------------------------------------------------ #
    # API pública                                                          #
    # ------------------------------------------------------------------ #

    def cargar_lista(self, lista_widget, usuarios):
        lista_widget.clear()
        for u in usuarios:
            lista_widget.addItem(f"{u.nombre_usuario}  —  {u.correo}")

    def cargar_logs(self, logs):
        self.listLogs.clear()
        for log in logs:
            id_mod, accion, comentario, fecha, usuario, mazo = log
            icono = "✅" if accion == "publicado" else "🚫"
            self.listLogs.addItem(
                f"{icono}  [{fecha}]  {accion.upper()}  —  Mazo: {mazo}  |  Usuario: {usuario}  |  {comentario}"
            )

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)

    def mostrar_info(self, mensaje):
        QMessageBox.information(self, "Info", mensaje)