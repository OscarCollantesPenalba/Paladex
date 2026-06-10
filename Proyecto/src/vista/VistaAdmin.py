import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PyQt5.uic import loadUi


class VistaAdmin(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__controlador = None
        loadUi('src/vista/Ui/menu_admin.ui', self)
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
        self.btnBackup.clicked.connect(self._on_backup)
        self.btnCerrarSesionAdmin.clicked.connect(
            lambda: self.__controlador.cerrar_sesion())

        # Conexión de la señal del tabWidget para cargar los logs al cambiar de pestaña
        self.tabWidget.currentChanged.connect(
            lambda indice: self.__controlador.cambiar_tab(indice))

    def _on_backup(self):
        """Abre un diálogo para elegir dónde guardar el backup."""
        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar backup de la base de datos",
            "Paladex_backup.sql",
            "Ficheros SQL (*.sql)"
        )
        if ruta and self.__controlador:
            self.__controlador.hacer_backup(ruta)

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