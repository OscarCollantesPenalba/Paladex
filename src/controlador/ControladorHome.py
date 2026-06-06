from src.modelo.LogicaHome import LogicaHome
from src.modelo.vo.MazoVo import MazoVO
from src.modelo.vo.TorneoVo import TorneoVO
from src.vista.VistaMazo import VistaMazo
from src.vista.VistaPerfil import VistaPerfil
from src.vista.VistaMisMazos import VistaMisMazos
from src.vista.VistaTorneos import VistaTorneos
from PyQt5.QtWidgets import QMessageBox


class ControladorHome:

    def __init__(self, ref_vista, usuario_actual):
        self.__vista   = ref_vista
        self.__usuario = usuario_actual
        self.__logica  = LogicaHome()
        self.__resultados_actuales = []

    # ------------------------------------------------------------------ #
    # Arranque                                                             #
    # ------------------------------------------------------------------ #

    def inicializar(self):
        self.__vista.cargarUsuario(self.__usuario)
        self.buscar("", "Todos")

    # ------------------------------------------------------------------ #
    # Búsqueda                                                             #
    # ------------------------------------------------------------------ #

    def buscar(self, termino, filtro):
        try:
            resultados = self.__logica.buscar(termino, filtro)
            self.__resultados_actuales = resultados
            self.__vista.mostrar_resultados(self._construir_etiquetas(resultados))
            if resultados:
                self.__vista.seleccionar_primero()
            else:
                self.__vista.limpiar_detalle()
        except Exception as e:
            self.__vista.mostrar_error(f"Error al buscar: {e}")

    def _construir_etiquetas(self, resultados):
        etiquetas = []
        for tipo, vo in resultados:
            if tipo == "campeon":
                etiquetas.append(f"[Campeón]  {vo.nombre}  —  {vo.titulo}")
            elif tipo == "carta":
                etiquetas.append(f"[Carta]    {vo.nombre}  ({vo.categoria})")
            elif tipo == "mazo":
                etiquetas.append(f"[Mazo]     {vo.nombre_mazo}")
            elif tipo == "torneo":
                etiquetas.append(f"[Torneo]   {vo.nombre}")
        return etiquetas

    def seleccionar_item(self, indice):
        if indice < 0 or indice >= len(self.__resultados_actuales):
            return
        tipo, vo = self.__resultados_actuales[indice]
        try:
            if tipo == "campeon":
                self.__vista.mostrar_detalle_campeon(self.__logica.obtener_campeon(vo.id_campeon))
            elif tipo == "carta":
                self.__vista.mostrar_detalle_carta(self.__logica.obtener_carta(vo.id_carta))
            elif tipo == "mazo":
                self.__vista.mostrar_detalle_mazo(self.__logica.obtener_mazo(vo.id_mazo))
            elif tipo == "torneo":
                self.__vista.mostrar_detalle_torneo(self.__logica.obtener_torneo(vo.id_torneo))
        except Exception as e:
            self.__vista.mostrar_error(f"Error al cargar detalle: {e}")

    # ------------------------------------------------------------------ #
    # Panel Info (Novedades / Mapas / Modos)                              #
    # ------------------------------------------------------------------ #

    def clic_novedad(self, indice):
        datos = self.__logica.obtener_novedad(indice)
        if datos:
            self.__vista.mostrar_info(datos)

    def clic_mapa(self, indice):
        datos = self.__logica.obtener_mapa(indice)
        if datos:
            self.__vista.mostrar_info(datos)

    def clic_modo(self, indice):
        datos = self.__logica.obtener_modo(indice)
        if datos:
            self.__vista.mostrar_info(datos)

    # ------------------------------------------------------------------ #
    # Perfil                                                               #
    # ------------------------------------------------------------------ #

    def abrirPerfil(self):
        self.__vista_perfil = VistaPerfil()
        self._actualizar_perfil()
        self.__vista_perfil.btnSumarVictoria.clicked.connect(lambda: self._procesar_combate(True))
        self.__vista_perfil.btnSumarDerrota.clicked.connect(lambda: self._procesar_combate(False))
        self.__vista_perfil.show()

    def _actualizar_perfil(self):
        id_usuario = self.__usuario.id_usuario
        usuario_vo = self.__logica.obtener_perfil(id_usuario)
        stats      = self.__logica.obtener_estadisticas(id_usuario)

        if usuario_vo:
            xp    = usuario_vo.puntos_experiencia or 0
            nivel = (xp // 100) + 1
            self.__vista_perfil.lblUsuario.setText(f"Usuario: {usuario_vo.nombre_usuario}")
            self.__vista_perfil.lblXP.setText(f"Puntos de Experiencia: {xp} XP")
            self.__vista_perfil.lblNivel.setText(f"Nivel: {nivel}")

        if stats:
            self.__vista_perfil.lblVictorias.setText(f"Victorias totales: {stats[0] or 0}")
            self.__vista_perfil.lblDerrotas.setText(f"Derrotas totales: {stats[1] or 0}")

    def _procesar_combate(self, es_victoria):
        exito = self.__logica.registrar_resultado_combate(self.__usuario.id_usuario, es_victoria)
        if exito:
            # Recargar usuario desde BD para que el rol esté actualizado en memoria
            usuario_actualizado = self.__logica.obtener_perfil(self.__usuario.id_usuario)
            if usuario_actualizado:
                self.__usuario = usuario_actualizado
            self._actualizar_perfil()

    # ------------------------------------------------------------------ #
    # Mazos                                                                #
    # ------------------------------------------------------------------ #

    def abrirCreadorMazos(self):
        id_rol = getattr(self.__usuario, 'id_rol', 3)
        if id_rol not in (0, 2):
            QMessageBox.warning(
                self.__vista,
                "Acceso Restringido",
                "Necesitas al menos Nivel 2 (100 XP) para crear mazos."
            )
            return

        self.__vista_mazo = VistaMazo()
        self._cargar_campeones_mazo()
        self.__vista_mazo.btnGuardarMazo.clicked.connect(self._guardar_mazo)
        self.__vista_mazo.cbCampeon.currentIndexChanged.connect(self._actualizar_cartas_mazo)
        self.__vista_mazo.show()

    def _cargar_campeones_mazo(self):
        campeones = self.__logica.obtener_campeones()
        self.__vista_mazo.cbCampeon.clear()
        for id_camp, nombre in campeones:
            self.__vista_mazo.cbCampeon.addItem(nombre, id_camp)
        # Cargar cartas del primer campeón seleccionado
        if campeones:
            self._actualizar_cartas_mazo()

    def _actualizar_cartas_mazo(self):
        id_campeon = self.__vista_mazo.cbCampeon.currentData()
        cartas = self.__logica.obtener_cartas_por_campeon(id_campeon)
        combos = [
            self.__vista_mazo.cbCarta1, self.__vista_mazo.cbCarta2,
            self.__vista_mazo.cbCarta3, self.__vista_mazo.cbCarta4,
            self.__vista_mazo.cbCarta5
        ]
        for cb in combos:
            cb.clear()
            for id_car, nombre, desc, cat in cartas:
                cb.addItem(nombre, id_car)

    def _guardar_mazo(self):
        nombre     = self.__vista_mazo.txtNombreMazo.text()
        id_campeon = self.__vista_mazo.cbCampeon.currentData()

        if not nombre:
            QMessageBox.warning(self.__vista_mazo, "Error", "El mazo debe tener un nombre.")
            return

        lista_cartas = [
            (self.__vista_mazo.cbCarta1.currentData(), self.__vista_mazo.spinNivel1.value()),
            (self.__vista_mazo.cbCarta2.currentData(), self.__vista_mazo.spinNivel2.value()),
            (self.__vista_mazo.cbCarta3.currentData(), self.__vista_mazo.spinNivel3.value()),
            (self.__vista_mazo.cbCarta4.currentData(), self.__vista_mazo.spinNivel4.value()),
            (self.__vista_mazo.cbCarta5.currentData(), self.__vista_mazo.spinNivel5.value()),
        ]

        # Validar que ninguna carta supere nivel 5
        for id_carta, nivel in lista_cartas:
            if nivel > 5:
                QMessageBox.warning(
                    self.__vista_mazo, "Nivel inválido",
                    f"Cada carta puede tener un nivel máximo de 5."
                )
                return

        # Validar nivel total == 15
        nivel_total = sum(nivel for _, nivel in lista_cartas)
        if nivel_total != 15:
            QMessageBox.warning(
                self.__vista_mazo, "Nivel inválido",
                f"La suma de niveles de las cartas debe ser exactamente 15.Actualmente es: {nivel_total}")
            return

        # Validar que no haya cartas repetidas
        ids_cartas = [id_carta for id_carta, _ in lista_cartas]
        if len(ids_cartas) != len(set(ids_cartas)):
            QMessageBox.warning(
                self.__vista_mazo, "Cartas repetidas",
                "No puede haber cartas repetidas en el mismo mazo."
            )
            return

        mazo_vo = MazoVO(None, nombre, "Sin descripción", "Activo", self.__usuario.id_usuario, id_campeon, 0)
        mazo_vo.lista_cartas = lista_cartas
        exito   = self.__logica.guardar_mazo(mazo_vo)

        if exito:
            QMessageBox.information(self.__vista_mazo, "Éxito", "¡Mazo guardado correctamente!")
            self.__vista_mazo.close()
        else:
            QMessageBox.critical(self.__vista_mazo, "Error", "Error al guardar el mazo.")

    def abrirMisMazos(self):
        id_rol = getattr(self.__usuario, 'id_rol', 3)
        if id_rol not in (0, 2):
            QMessageBox.warning(
                self.__vista,
                "Acceso Restringido",
                "Necesitas al menos Nivel 2 (100 XP) para acceder a tus mazos."
            )
            return

        self.__vista_mis_mazos = VistaMisMazos()
        self.__datos_mazos = self.__logica.obtener_mazos_usuario(self.__usuario.id_usuario)

        self.__vista_mis_mazos.listMazos.clear()
        for mazo in self.__datos_mazos:
            self.__vista_mis_mazos.listMazos.addItem(mazo[1])

        self.__vista_mis_mazos.listMazos.currentRowChanged.connect(self._mostrar_detalle_mazo)
        self.__vista_mis_mazos.btnEliminarMazo.clicked.connect(self._eliminar_mazo)
        self.__vista_mis_mazos.show()

    def _mostrar_detalle_mazo(self, fila):
        if fila < 0:
            return
        mazo = self.__datos_mazos[fila]
        self.__vista_mis_mazos.lblCampeon.setText(f"Campeón: {mazo[2]}")
        cartas = self.__logica.obtener_detalles_mazo(mazo[0])
        texto  = "\n".join(f"• {nom} (Nivel {nivel})" for nom, nivel in cartas)
        self.__vista_mis_mazos.txtDetalleCartas.setText(texto)

    def _eliminar_mazo(self):
        fila = self.__vista_mis_mazos.listMazos.currentRow()
        if fila < 0:
            return
        exito = self.__logica.eliminar_mazo(self.__datos_mazos[fila][0])
        if exito:
            QMessageBox.information(self.__vista_mis_mazos, "Éxito", "Mazo eliminado.")
            self.__vista_mis_mazos.close()
            self.abrirMisMazos()
        else:
            QMessageBox.critical(self.__vista_mis_mazos, "Error", "Error al eliminar el mazo.")

    # ------------------------------------------------------------------ #
    # Torneos                                                              #
    # ------------------------------------------------------------------ #

    def abrirTorneos(self):
        self.__vista_torneos = VistaTorneos()
        self.__datos_torneos = self.__logica.obtener_torneos()

        self.__vista_torneos.listTorneos.clear()
        for torneo in self.__datos_torneos:
            self.__vista_torneos.listTorneos.addItem(torneo.nombre)

        self.__vista_torneos.listTorneos.currentRowChanged.connect(self._mostrar_detalle_torneo)
        self.__vista_torneos.btnInscribirse.clicked.connect(self._inscribir_torneo)
        self.__vista_torneos.show()

    def _mostrar_detalle_torneo(self, fila):
        if fila < 0:
            return
        t = self.__datos_torneos[fila]
        self.__vista_torneos.lblUbicacion.setText(f"Ubicación: {t.ubicacion}")
        self.__vista_torneos.lblDescripcion.setText(f"Descripción: {t.descripcion}")
        self.__vista_torneos.lblReglas.setText(f"Reglas: {t.reglas}")

    def _inscribir_torneo(self):
        fila = self.__vista_torneos.listTorneos.currentRow()
        if fila < 0:
            QMessageBox.warning(self.__vista_torneos, "Aviso", "Selecciona un torneo primero.")
            return
        exito = self.__logica.inscribir_usuario_torneo(
            self.__usuario.id_usuario,
            self.__datos_torneos[fila].id_torneo,
            self.__usuario.nombre_usuario,
            "Ninguno"
        )
        if exito:
            QMessageBox.information(self.__vista_torneos, "Éxito", "¡Inscrito en el torneo!")
        else:
            QMessageBox.critical(self.__vista_torneos, "Error", "Ya estás inscrito o hubo un error.")