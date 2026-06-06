import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi


class VistaHome(QMainWindow):

    UI_PATH = os.path.join(os.path.dirname(__file__), "ui", "Home.ui")

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
        if hasattr(self, "BtnBuscar"):
            self.BtnBuscar.clicked.connect(self._on_buscar)
        self.BarraBusqueda_2.returnPressed.connect(self._on_buscar)
        self.FiltrosBusqueda.currentTextChanged.connect(self._on_buscar)
        self.Resultados.currentRowChanged.connect(self._on_seleccionar)

        self.BtnNovedad1.clicked.connect(lambda: self.__controlador.clic_novedad(0))
        self.BtnNovedad2.clicked.connect(lambda: self.__controlador.clic_novedad(1))
        self.BtnNovedad3.clicked.connect(lambda: self.__controlador.clic_novedad(2))

        self.BtnMapa1.clicked.connect(lambda: self.__controlador.clic_mapa(0))
        self.BtnMapa2.clicked.connect(lambda: self.__controlador.clic_mapa(1))
        self.BtnMapa3.clicked.connect(lambda: self.__controlador.clic_mapa(2))

        self.BtnModo1.clicked.connect(lambda: self.__controlador.clic_modo(0))
        self.BtnModo2.clicked.connect(lambda: self.__controlador.clic_modo(1))
        self.BtnModo3.clicked.connect(lambda: self.__controlador.clic_modo(2))

    def _on_buscar(self):
        if self.__controlador:
            self.__controlador.buscar(
                self.BarraBusqueda_2.text(),
                self.FiltrosBusqueda.currentText()
            )

    def _on_seleccionar(self, indice):
        if self.__controlador and indice >= 0:
            self.__controlador.seleccionar_item(indice)

    # ------------------------------------------------------------------ #
    # API pública                                                          #
    # ------------------------------------------------------------------ #

    def cargarUsuario(self, usuario_vo):
        self.LabelUsuario.setText(f"👤  {usuario_vo.nombre_usuario}")

    def mostrar_resultados(self, etiquetas):
        self.Resultados.clear()
        for texto in etiquetas:
            self.Resultados.addItem(texto)

    def seleccionar_primero(self):
        if self.Resultados.count() > 0:
            self.Resultados.setCurrentRow(0)

    def limpiar_resultados(self):
        self.Resultados.clear()

    # ------------------------------------------------------------------ #
    # Panel Info (GroupBox superior)                                       #
    # ------------------------------------------------------------------ #

    def mostrar_info(self, datos):
        self.InfoTitulo.setText(datos.get("titulo", ""))
        self.InfoSubtitulo.setText(datos.get("subtitulo", ""))
        self.InfoDescripcion.setPlainText(datos.get("descripcion", ""))

    # ------------------------------------------------------------------ #
    # Panel Detalle (lista derecha)                                        #
    # ------------------------------------------------------------------ #

    def limpiar_detalle(self):
        self.DetalleTitulo.setText("")
        self.DetalleSubtitulo.setText("")
        self.DetalleKey1.setText(""); self.DetalleVal1.setText("")
        self.DetalleKey2.setText(""); self.DetalleVal2.setText("")
        self.DetalleKey3.setText(""); self.DetalleVal3.setText("")
        self.DetalleKey4.setText(""); self.DetalleVal4.setText("")
        self.DetalleExtra.setPlainText("")

    def mostrar_detalle_campeon(self, vo):
        self.limpiar_detalle()
        if not vo:
            return
        self.DetalleTitulo.setText(f"⚔  {vo.nombre}")
        self.DetalleSubtitulo.setText(vo.titulo or "")
        self.DetalleKey1.setText("Clase:");       self.DetalleVal1.setText(vo.nombre_clase or "—")
        self.DetalleKey2.setText("❤ Salud:");    self.DetalleVal2.setText(str(vo.salud))
        self.DetalleKey3.setText("⚡ Daño:");     self.DetalleVal3.setText(str(vo.daño))
        self.DetalleKey4.setText("💨 Velocidad:"); self.DetalleVal4.setText(str(vo.velocidad))
        lineas = []
        if hasattr(vo, "habilidades") and vo.habilidades:
            lineas.append("── Habilidades ──")
            for h in vo.habilidades:
                lineas.append(f"• {h.nombre} [{h.tipo}]: {h.descripcion or ''}")
        if hasattr(vo, "cartas") and vo.cartas:
            lineas.append("\n── Cartas ──")
            for c in vo.cartas:
                lineas.append(f"• {c.nombre}  ({c.categoria or '—'})")
        self.DetalleExtra.setPlainText("\n".join(lineas))

    def mostrar_detalle_carta(self, vo):
        self.limpiar_detalle()
        if not vo:
            return
        self.DetalleTitulo.setText(f"🃏  {vo.nombre}")
        self.DetalleKey1.setText("Categoría:"); self.DetalleVal1.setText(vo.categoria or "—")
        self.DetalleKey2.setText("Campeón:");   self.DetalleVal2.setText(vo.nombre_campeon or "—")
        lineas = []
        if vo.descripcion:
            lineas.append("── Descripción ──")
            lineas.append(vo.descripcion)
        if hasattr(vo, "cartas_campeon") and vo.cartas_campeon:
            lineas.append(f"\n── Otras cartas de {vo.nombre_campeon} ──")
            for c in vo.cartas_campeon:
                if c.id_carta != vo.id_carta:
                    lineas.append(f"• {c.nombre}  ({c.categoria or '—'})")
        self.DetalleExtra.setPlainText("\n".join(lineas))

    def mostrar_detalle_mazo(self, vo):
        self.limpiar_detalle()
        if not vo:
            return
        self.DetalleTitulo.setText(f"📦  {vo.nombre_mazo}")
        self.DetalleKey1.setText("Campeón:"); self.DetalleVal1.setText(vo.nombre_campeon or "—")
        self.DetalleKey2.setText("Estado:");  self.DetalleVal2.setText(vo.estado or "—")
        self.DetalleKey3.setText("Creador:"); self.DetalleVal3.setText(vo.nombre_usuario or "—")
        self.DetalleKey4.setText("Oficial:"); self.DetalleVal4.setText("Sí" if vo.es_oficial else "No")
        lineas = []
        if vo.descripcion:
            lineas.append("── Descripción ──")
            lineas.append(vo.descripcion)
        if hasattr(vo, "cartas") and vo.cartas:
            lineas.append(f"\n── Cartas del mazo ({len(vo.cartas)}) ──")
            for c in vo.cartas:
                nivel = f"  [Nivel {c.nivel}]" if hasattr(c, "nivel") and c.nivel else ""
                lineas.append(f"• {c.nombre}  ({c.categoria or '—'}){nivel}")
        self.DetalleExtra.setPlainText("\n".join(lineas))

    def mostrar_detalle_torneo(self, vo):
        self.limpiar_detalle()
        if not vo:
            return
        self.DetalleTitulo.setText(f"🏆  {vo.nombre}")
        self.DetalleKey1.setText("📍 Ubicación:"); self.DetalleVal1.setText(vo.ubicacion or "—")
        lineas = []
        if vo.descripcion:
            lineas.append("── Descripción ──")
            lineas.append(vo.descripcion)
        if vo.reglas:
            lineas.append("\n── Reglas ──")
            lineas.append(vo.reglas)
        self.DetalleExtra.setPlainText("\n".join(lineas))

    # ------------------------------------------------------------------ #
    # Feedback                                                             #
    # ------------------------------------------------------------------ #

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)

    def mostrar_info_msg(self, mensaje):
        QMessageBox.information(self, "Info", mensaje)