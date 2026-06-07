import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi


class VistaModerador(QMainWindow):

    UI_PATH = os.path.join(os.path.dirname(__file__), "ui", "menu_moderador.ui")

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

    # ------------------------------------------------------------------ #
    # Señales                                                              #
    # ------------------------------------------------------------------ #

    def _conectar_senales(self):
        self.btnEliminarMazoGlobal.clicked.connect(self._on_eliminar_mazo)
        self.btnEliminarTorneo.clicked.connect(self._on_eliminar_torneo)
        self.btnEliminarParticipante.clicked.connect(self._on_expulsar_participante)
        self.btnGuardarTorneo.clicked.connect(self._on_crear_torneo)
        self.btnCerrarSesionMod.clicked.connect(self._on_cerrar_sesion)
        self.listTorneosMod.currentRowChanged.connect(self._on_seleccionar_torneo)

    def _on_eliminar_mazo(self):
        if self.__controlador:
            self.__controlador.eliminar_mazo(self.listMazosGlobal.currentRow())

    def _on_eliminar_torneo(self):
        if self.__controlador:
            self.__controlador.eliminar_torneo(self.listTorneosMod.currentRow())

    def _on_expulsar_participante(self):
        if self.__controlador:
            self.__controlador.expulsar_participante(
                self.listTorneosMod.currentRow(),
                self.listParticipantes.currentRow()
            )

    def _on_crear_torneo(self):
        if self.__controlador:
            self.__controlador.crear_torneo(
                self.txtNombreTorneo.text(),
                self.txtUbicacionTorneo.text(),
                self.txtDescTorneo.text(),
                self.txtReglasTorneo.text()
            )

    def _on_cerrar_sesion(self):
        if self.__controlador:
            self.__controlador.cerrar_sesion()

    def _on_seleccionar_torneo(self, fila):
        if self.__controlador:
            self.__controlador.cargar_participantes(fila)

    # ------------------------------------------------------------------ #
    # API pública                                                          #
    # ------------------------------------------------------------------ #

    def cargar_mazos(self, mazos):
        self.listMazosGlobal.clear()
        for m in mazos:
            self.listMazosGlobal.addItem(f"Mazo: {m[1]}  |  Creador: {m[2]}")

    def cargar_torneos(self, torneos):
        self.listTorneosMod.clear()
        for t in torneos:
            self.listTorneosMod.addItem(t.nombre)

    def cargar_participantes(self, participantes):
        self.listParticipantes.clear()
        for p in participantes:
            self.listParticipantes.addItem(f"{p[1]}  ({p[2]})")

    def limpiar_formulario_torneo(self):
        self.txtNombreTorneo.clear()
        self.txtUbicacionTorneo.clear()
        self.txtDescTorneo.clear()
        self.txtReglasTorneo.clear()

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)

    def mostrar_info(self, mensaje):
        QMessageBox.information(self, "Info", mensaje)