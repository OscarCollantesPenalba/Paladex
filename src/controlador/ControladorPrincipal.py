from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.UsuarioVo import UsuarioVO
from src.modelo.vo.MazoVo import MazoVO
from src.modelo.vo.TorneoVo import TorneoVO
from src.vista.VistaHome import VistaHome
from src.vista.VistaMazo import VistaMazo
from src.vista.VistaMenu import VistaMenu
from src.vista.VistaTorneos import VistaTorneos
from src.vista.VistaPerfil import VistaPerfil
from src.vista.VistaMisMazos import VistaMisMazos
from src.vista.VistaModerador import VistaModerador
from src.vista.VistaAdmin import VistaAdmin
from src.controlador.ControladorHome import ControladorHome
from src.controlador.ControladorModerador import ControladorModerador
from src.controlador.ControladorAdmin import ControladorAdmin


class ControladorPrincipal:
    def __init__(self, ref_vista, ref_modelo):
        self.__vista = ref_vista
        self.__modelo = ref_modelo
        self.usuario_actual = None
        self.usuario_actual_id = None

    # ------------------------------------------------------------------ #
    # Login / Registro                                                     #
    # ------------------------------------------------------------------ #

    def abrirIniciarSesion(self):
        self.__vista.show()

    def comprobarLogin(self, usuario, contrasena):
        loginVO = LoginVO(usuario, contrasena)
        resultado = self.__modelo.HacerLogin(loginVO)

        if not usuario or not contrasena:
            self.__vista.login_vacio()
            return

        if resultado is None:
            self.__vista.login_incorrecto()
            return

        self.usuario_actual = resultado
        self.usuario_actual_id = resultado.id_usuario
        id_rol = getattr(resultado, 'id_rol', 3)
        self.__vista.close()

        if id_rol == 0:
            self.mostrar_menu_admin()
        elif id_rol == 1:
            self.mostrar_menu_moderador()
        else:
            self.__abrirHome(resultado)

    def comprobarRegistro(self, nombre_completo, nombre_usuario, correo, contrasena, confirm_contrasena, puntos_experiencia=0, id_rol=3):
        if not nombre_completo or not nombre_usuario or not correo or not contrasena or not confirm_contrasena:
            self.__vista.sign_vacio()
            return

        if "@" not in correo or "." not in correo:
            self.__vista.email_correcto()
            return

        if contrasena != confirm_contrasena:
            self.__vista.contrasenas_diferentes()
            return

        if len(contrasena) < 8:
            self.__vista.contrasena_pequena()
            return

        usuarioVO = UsuarioVO(None, nombre_completo, nombre_usuario, correo, contrasena, puntos_experiencia, id_rol)
        resultado = self.__modelo.ComprobarSign(usuarioVO)

        if resultado:
            self.__vista.usuario_email_existentes()
        else:
            self.__modelo.Insert(usuarioVO)
            self.__vista.volver_login()

    # ------------------------------------------------------------------ #
    # Home                                                                 #
    # ------------------------------------------------------------------ #

    def __abrirHome(self, usuario):
        self.__vista_home = VistaHome()
        self.__ctrl_home  = ControladorHome(self.__vista_home, usuario)
        self.__vista_home.controlador = self.__ctrl_home

        # Conectar botones del sidebar al ControladorHome
        if hasattr(self.__vista_home, 'btnPerfil'):
            self.__vista_home.btnPerfil.clicked.connect(self.__ctrl_home.abrirPerfil)
        if hasattr(self.__vista_home, 'btnMazos'):
            self.__vista_home.btnMazos.clicked.connect(self.__ctrl_home.abrirCreadorMazos)
        if hasattr(self.__vista_home, 'btnMisMazos'):
            self.__vista_home.btnMisMazos.clicked.connect(self.__ctrl_home.abrirMisMazos)
        if hasattr(self.__vista_home, 'btnTorneos'):
            self.__vista_home.btnTorneos.clicked.connect(self.__ctrl_home.abrirTorneos)
        if hasattr(self.__vista_home, 'btnCerrarSesion'):
            self.__vista_home.btnCerrarSesion.clicked.connect(self.__cerrarSesionHome)

        self.__vista_home.closeEvent = lambda event: self.__on_home_cerrada(event)
        self.__vista_home.show()
        self.__ctrl_home.inicializar()

    def __on_home_cerrada(self, event):
        self.__ctrl_home.cerrar_todo()
        event.accept()

    def __cerrarSesionHome(self):
        self.__ctrl_home.cerrar_todo()
        self.__vista_home.close()
        self.usuario_actual = None
        self.usuario_actual_id = None
        self.abrirIniciarSesion()

    # ------------------------------------------------------------------ #
    # Menú principal                                                       #
    # ------------------------------------------------------------------ #

    def mostrar_menu_principal(self):
        self.__menu = VistaMenu()

        if hasattr(self.__menu, 'btnPerfil'):
            self.__menu.btnPerfil.clicked.connect(self.abrirPerfilUsuario)
        if hasattr(self.__menu, 'btnMazos'):
            self.__menu.btnMazos.clicked.connect(self.abrirCreadorMazos)
        if hasattr(self.__menu, 'btnMisMazos'):
            self.__menu.btnMisMazos.clicked.connect(self.abrirMisMazos)
        if hasattr(self.__menu, 'btnTorneos'):
            self.__menu.btnTorneos.clicked.connect(self.abrirGestionTorneos)
        if hasattr(self.__menu, 'btnCerrarSesion'):
            self.__menu.btnCerrarSesion.clicked.connect(self.cerrar_sesion)

        self.__menu.show()

    def cerrar_sesion(self):
        self.__menu.close()
        self.usuario_actual = None
        self.usuario_actual_id = None
        self.abrirIniciarSesion()

    # ------------------------------------------------------------------ #
    # Mazos                                                                #
    # ------------------------------------------------------------------ #

    def abrirCreadorMazos(self):
        id_rol_actual = getattr(self.usuario_actual, 'id_rol', 3)

        if id_rol_actual not in (0, 2):
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                self.__vista_home,
                "Acceso Restringido",
                "No tienes el rol de 'Creador de Mazos'. Requieres al menos Nivel 2 (100 XP) para desbloquear esta función."
            )
            return

        self.__nueva_vista = VistaMazo()
        self.cargar_datos_iniciales()
        self.__nueva_vista.btnGuardarMazo.clicked.connect(self.guardarMazoDesdeInterfaz)
        self.__nueva_vista.cbCampeon.currentIndexChanged.connect(self.actualizar_cartas_interfaz)
        self.__nueva_vista.show()

    def cargar_datos_iniciales(self):
        campeones = self.__modelo.obtener_campeones()
        self.__nueva_vista.cbCampeon.clear()
        for id_camp, nombre in campeones:
            self.__nueva_vista.cbCampeon.addItem(nombre, id_camp)

    def guardarMazoDesdeInterfaz(self):
        nombre = self.__nueva_vista.txtNombreMazo.text()
        id_campeon = self.__nueva_vista.cbCampeon.currentData()
        id_usuario = self.usuario_actual_id

        if not nombre:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self.__nueva_vista, "Error", "El mazo debe tener un nombre.")
            return

        lista_cartas = [
            (self.__nueva_vista.cbCarta1.currentData(), self.__nueva_vista.spinNivel1.value()),
            (self.__nueva_vista.cbCarta2.currentData(), self.__nueva_vista.spinNivel2.value()),
            (self.__nueva_vista.cbCarta3.currentData(), self.__nueva_vista.spinNivel3.value()),
            (self.__nueva_vista.cbCarta4.currentData(), self.__nueva_vista.spinNivel4.value()),
            (self.__nueva_vista.cbCarta5.currentData(), self.__nueva_vista.spinNivel5.value()),
        ]

        nuevo_mazo = MazoVO(None, nombre, id_usuario, id_campeon, lista_cartas)
        exito = self.__modelo.guardar_mazo_en_db(nuevo_mazo)

        from PyQt5.QtWidgets import QMessageBox
        if exito:
            QMessageBox.information(self.__nueva_vista, "Éxito", "¡Mazo guardado correctamente!")
            self.__nueva_vista.close()
        else:
            QMessageBox.critical(self.__nueva_vista, "Error", "Error al guardar el mazo en la base de datos.")

    def actualizar_cartas_interfaz(self):
        id_c = self.__nueva_vista.cbCampeon.currentData()
        cartas = self.__modelo.obtener_cartas_por_campeon(id_c)

        combos = [
            self.__nueva_vista.cbCarta1, self.__nueva_vista.cbCarta2,
            self.__nueva_vista.cbCarta3, self.__nueva_vista.cbCarta4,
            self.__nueva_vista.cbCarta5
        ]
        for cb in combos:
            cb.clear()
            for id_car, nombre, desc, cat in cartas:
                cb.addItem(nombre, id_car)

    def abrirMisMazos(self):
        self.__vista_mis_mazos = VistaMisMazos()
        self.__datos_mazos = self.__modelo.obtener_mazos_usuario(self.usuario_actual_id)

        self.__vista_mis_mazos.listMazos.clear()
        for mazo in self.__datos_mazos:
            self.__vista_mis_mazos.listMazos.addItem(mazo[1])

        self.__vista_mis_mazos.listMazos.currentRowChanged.connect(self.mostrar_detalles_mazo)
        self.__vista_mis_mazos.btnEliminarMazo.clicked.connect(self.procesar_eliminacion_mazo)
        self.__vista_mis_mazos.show()

    def mostrar_detalles_mazo(self, fila):
        if fila < 0:
            return
        mazo = self.__datos_mazos[fila]
        id_mazo = mazo[0]
        self.__vista_mis_mazos.lblCampeon.setText(f"Campeón: {mazo[2]}")

        cartas = self.__modelo.obtener_detalles_mazo(id_mazo)
        texto = ""
        for nom_carta, nivel in cartas:
            texto += f"• {nom_carta} (Nivel {nivel})\n"
        self.__vista_mis_mazos.txtDetalleCartas.setText(texto)

    def procesar_eliminacion_mazo(self):
        fila = self.__vista_mis_mazos.listMazos.currentRow()
        if fila < 0:
            return
        id_mazo = self.__datos_mazos[fila][0]
        exito = self.__modelo.eliminar_mazo_db(id_mazo)

        from PyQt5.QtWidgets import QMessageBox
        if exito:
            QMessageBox.information(self.__vista_mis_mazos, "Éxito", "Mazo eliminado correctamente.")
            self.__vista_mis_mazos.close()
            self.abrirMisMazos()
        else:
            QMessageBox.critical(self.__vista_mis_mazos, "Error", "Error al eliminar el mazo.")

    # ------------------------------------------------------------------ #
    # Torneos                                                              #
    # ------------------------------------------------------------------ #

    def abrirGestionTorneos(self):
        self.__vista_torneos = VistaTorneos()
        self.__datos_torneos = self.__modelo.obtener_torneos()

        self.__vista_torneos.listTorneos.clear()
        for torneo in self.__datos_torneos:
            self.__vista_torneos.listTorneos.addItem(torneo.nombre)

        self.__vista_torneos.listTorneos.currentRowChanged.connect(self.mostrar_detalles_torneo)
        self.__vista_torneos.btnInscribirse.clicked.connect(self.procesar_inscripcion)
        self.__vista_torneos.show()

    def mostrar_detalles_torneo(self, fila):
        if fila < 0:
            return
        torneo = self.__datos_torneos[fila]
        self.__vista_torneos.lblUbicacion.setText(f"Ubicación: {torneo.ubicacion}")
        self.__vista_torneos.lblDescripcion.setText(f"Descripción: {torneo.descripcion}")
        self.__vista_torneos.lblReglas.setText(f"Reglas: {torneo.reglas}")

    def procesar_inscripcion(self):
        fila = self.__vista_torneos.listTorneos.currentRow()
        if fila < 0:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self.__vista_torneos, "Aviso", "Selecciona un torneo primero.")
            return

        id_torneo = self.__datos_torneos[fila].id_torneo
        id_usuario = self.usuario_actual_id
        alias = self.usuario_actual.nombre_usuario
        equipo = "Ninguno"

        exito = self.__modelo.inscribir_usuario_torneo(id_usuario, id_torneo, alias, equipo)

        from PyQt5.QtWidgets import QMessageBox
        if exito:
            QMessageBox.information(self.__vista_torneos, "Éxito", "¡Inscrito correctamente en el torneo!")
        else:
            QMessageBox.critical(self.__vista_torneos, "Error", "Ya estás inscrito o hubo un error.")

    # ------------------------------------------------------------------ #
    # Perfil                                                               #
    # ------------------------------------------------------------------ #

    def abrirPerfilUsuario(self):
        self.__vista_perfil = VistaPerfil()
        self.actualizar_datos_pantalla_perfil()
        self.__vista_perfil.btnSumarVictoria.clicked.connect(lambda: self.procesar_cambio_stats(True))
        self.__vista_perfil.btnSumarDerrota.clicked.connect(lambda: self.procesar_cambio_stats(False))
        self.__vista_perfil.show()

    def actualizar_datos_pantalla_perfil(self):
        usuario_vo = self.__modelo.obtener_datos_perfil_vo(self.usuario_actual_id)
        stats_torneo = self.__modelo.obtener_estadisticas_torneo(self.usuario_actual_id)

        if usuario_vo:
            xp = usuario_vo.puntos_experiencia or 0
            nivel = (xp // 100) + 1
            self.__vista_perfil.lblUsuario.setText(f"Usuario: {usuario_vo.nombre_usuario}")
            self.__vista_perfil.lblXP.setText(f"Puntos de Experiencia: {xp} XP")
            self.__vista_perfil.lblNivel.setText(f"Nivel: {nivel}")

        if stats_torneo:
            victorias = stats_torneo[0] or 0
            derrotas  = stats_torneo[1] or 0
            self.__vista_perfil.lblVictorias.setText(f"Victorias totales: {victorias}")
            self.__vista_perfil.lblDerrotas.setText(f"Derrotas totales: {derrotas}")

    def procesar_cambio_stats(self, es_victoria):
        exito = self.__modelo.registrar_resultado_combate(self.usuario_actual_id, es_victoria)
        if exito:
            self.actualizar_datos_pantalla_perfil()

    # ------------------------------------------------------------------ #
    # Panel Administrador                                                  #
    # ------------------------------------------------------------------ #

    def mostrar_menu_admin(self):
        from src.vista.VistaAdmin import VistaAdmin
        self.__vista_admin = VistaAdmin()
        self.__ctrl_admin  = ControladorAdmin(self.__vista_admin, self.usuario_actual, self)
        self.__vista_admin.controlador = self.__ctrl_admin
        self.__vista_admin.show()
        self.__ctrl_admin.inicializar()

    # ------------------------------------------------------------------ #
    # Panel Moderador                                                      #
    # ------------------------------------------------------------------ #

    def mostrar_menu_moderador(self):
        from src.vista.VistaModerador import VistaModerador
        self.__vista_mod = VistaModerador()
        self.__ctrl_mod  = ControladorModerador(self.__vista_mod, self.usuario_actual, self)
        self.__vista_mod.controlador = self.__ctrl_mod
        self.__vista_mod.show()
        self.__ctrl_mod.inicializar()