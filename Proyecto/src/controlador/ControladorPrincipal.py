from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.UsuarioVo import UsuarioVO
from src.vista.VistaMazo import VistaMazo
from src.modelo.vo.MazoVO import MazoVO
from src.vista.VistaMenu import VistaMenu
from src.vista.VistaTorneos import VistaTorneos
from src.vista.VistaPerfil import VistaPerfil
from src.vista.VistaMisMazos import VistaMisMazos
from src.vista.VistaMenuModerador import VistaMenuModerador
from src.vista.VistaMenuAdmin import VistaMenuAdmin
from src.modelo.vo.TorneoVO import TorneoVO

class ControladorPrincipal:
    def __init__(self, ref_vista, ref_modelo):
        self.__vista = ref_vista
        self.__modelo = ref_modelo
        self.usuario_actual = None
        self.usuario_actual_id = None
        
        if hasattr(self.__vista, 'btnIrAMazos'):
            self.__vista.btnIrAMazos.clicked.connect(self.abrirCreadorMazos)

    def cargar_datos_iniciales(self):
        campeones = self.__modelo.obtener_campeones()
        self.__nueva_vista.cbCampeon.clear()
        for id_amp, nombre in campeones:
            self.__nueva_vista.cbCampeon.addItem(nombre, id_amp)

    def abrirIniciarSesion(self):
        self.__vista.show()

    def comprobarLogin(self, usuario, contrasena):
        loginVO = LoginVO(usuario, contrasena)
        resultado = self.__modelo.HacerLogin(loginVO)

        if resultado:
            self.usuario_actual = resultado 
            self.usuario_actual_id = resultado.id_usuario
            
            id_rol = getattr(resultado, 'id_rol', 3)
            self.__vista.close()
            
            if id_rol == 1:
                self.mostrar_menu_admin()
            elif id_rol == 2:
                self.mostrar_menu_moderador()
            else:
                self.mostrar_menu_principal()
        else:
            self.__vista.login_incorrecto()

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

    def abrirCreadorMazos(self):
        id_rol_actual = getattr(self.usuario_actual, 'id_rol', 3)
        
        if id_rol_actual != 4 and id_rol_actual != 1:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                self.__menu, 
                "Acceso Restringido", 
                "No tienes el rol de 'Creador de Mazos'. Requieres al menos Nivel 2 (100 XP) para desbloquear esta función."
            )
            return
            
        self.__nueva_vista = VistaMazo()
        self.cargar_datos_iniciales()
        self.__nueva_vista.btnGuardarMazo.clicked.connect(self.guardarMazoDesdeInterfaz)
        self.__nueva_vista.cbCampeon.currentIndexChanged.connect(self.actualizar_cartas_interfaz)
        self.__nueva_vista.show()

    def guardarMazoDesdeInterfaz(self):
        nombre = self.__nueva_vista.txtNombreMazo.text()
        id_campeon = self.__nueva_vista.cbCampeon.currentData()
        id_usuario = getattr(self, 'usuario_actual_id', 1) 

        if not nombre:
            print("El mazo debe tener un nombre")
            return

        lista_cartas = [
            (self.__nueva_vista.cbCarta1.currentData(), self.__nueva_vista.spinNivel1.value()),
            (self.__nueva_vista.cbCarta2.currentData(), self.__nueva_vista.spinNivel2.value()),
            (self.__nueva_vista.cbCarta3.currentData(), self.__nueva_vista.spinNivel3.value()),
            (self.__nueva_vista.cbCarta4.currentData(), self.__nueva_vista.spinNivel4.value()),
            (self.__nueva_vista.cbCarta5.currentData(), self.__nueva_vista.spinNivel5.value())
        ]

        nuevo_mazo = MazoVO(None, nombre, id_usuario, id_campeon, lista_cartas)
        exito = self.__modelo.guardar_mazo_en_db(nuevo_mazo)

        if exito:
            print("¡Mazo guardado con éxito!")
        else:
            print("Error al guardar el mazo en la base de datos")

    def actualizar_cartas_interfaz(self):
        id_c = self.__nueva_vista.cbCampeon.currentData()
        cartas = self.__modelo.obtener_cartas_por_campeon(id_c)

        combos = [self.__nueva_vista.cbCarta1, self.__nueva_vista.cbCarta2, 
                  self.__nueva_vista.cbCarta3, self.__nueva_vista.cbCarta4, 
                  self.__nueva_vista.cbCarta5]

        for cb in combos:
            cb.clear()
            for id_car, nombre, desc, cat in cartas:
                cb.addItem(nombre, id_car)

    def abrirGestionTorneos(self):
        self.__vista_torneos = VistaTorneos()
        self.__datos_torneos = self.__modelo.obtener_torneos()
        
        self.__vista_torneos.listTorneos.clear()
        for torneo in self.__datos_torneos:
            self.__vista_torneos.listTorneos.addItem(torneo.nombre)
            
        self.__vista_torneos.listTorneos.currentRowChanged.connect(self.mostrar_detalles_torneo)
        self.__vista_torneos.btnInscribirse.clicked.connect(self.procesar_inscripcion)
        self.__vista_torneos.show()

    def mostrar_detalles_torneo(self, fila_seleccionada):
        if fila_seleccionada < 0:
            return
            
        torneo = self.__datos_torneos[fila_seleccionada]
        self.__vista_torneos.lblUbicacion.setText(f"Ubicación: {torneo.ubicacion}")
        self.__vista_torneos.lblDescripcion.setText(f"Descripción: {torneo.descripcion}")
        self.__vista_torneos.lblReglas.setText(f"Reglas: {torneo.reglas}")

    def procesar_inscripcion(self):
        fila = self.__vista_torneos.listTorneos.currentRow()
        if fila < 0:
            print("Por favor, selecciona un torneo primero.")
            return
            
        id_torneo = self.__datos_torneos[fila].id_torneo
        id_usuario = getattr(self, 'usuario_actual_id', 1)
        
        alias_usuario = "Player_Pro"
        equipo_usuario = "Ninguno"
        
        exito = self.__modelo.inscribir_usuario_torneo(id_usuario, id_torneo, alias_usuario, equipo_usuario)
        
        if exito:
            print("¡Inscrito correctamente en el torneo!")
        else:
            print("Error: Ya estás inscrito o falló la BD.")

    def abrirPerfilUsuario(self):
        self.__vista_perfil = VistaPerfil()
        self.actualizar_datos_pantalla_perfil()
        
        self.__vista_perfil.btnSumarVictoria.clicked.connect(lambda: self.procesar_cambio_stats(True))
        self.__vista_perfil.btnSumarDerrota.clicked.connect(lambda: self.procesar_cambio_stats(False))
        self.__vista_perfil.show()

    def actualizar_datos_pantalla_perfil(self):
        id_usuario = self.usuario_actual_id
        usuario_vo = self.__modelo.obtener_datos_perfil_vo(id_usuario) 
        stats_torneo = self.__modelo.obtener_estadisticas_torneo(id_usuario)
        
        if usuario_vo:
            xp = usuario_vo.puntos_experiencia if usuario_vo.puntos_experiencia is not None else 0
            nivel = (xp // 100) + 1
            
            self.__vista_perfil.lblUsuario.setText(f"Usuario: {usuario_vo.nombre_usuario}")
            self.__vista_perfil.lblXP.setText(f"Puntos de Experiencia: {xp} XP")
            self.__vista_perfil.lblNivel.setText(f"Nivel: {nivel}")
            
        if stats_torneo:
            self.__vista_perfil.lblVictorias.setText(str(stats_torneo[0]))
            self.__vista_perfil.lblDerrotas.setText(str(stats_torneo[1]))

    def procesar_cambio_stats(self, es_victoria):
        id_usuario = self.usuario_actual_id
        exito = self.__modelo.registrar_resultado_combate(id_usuario, es_victoria)
        if exito:
            usuario_vo = self.__modelo.obtener_datos_perfil_vo(id_usuario)
            if usuario_vo:
                self.usuario_actual = usuario_vo
            self.actualizar_datos_pantalla_perfil()

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
            self.__vista.close()
            self.abrirIniciarSesion()

    def abrirMisMazos(self):
        self.__vista_mis_mazos = VistaMisMazos()
        id_usuario = getattr(self, 'usuario_actual_id', 1)
        self.__datos_mazos = self.__modelo.obtener_mazos_usuario(id_usuario)
        
        self.__vista_mis_mazos.listMazos.clear()
        for mazo in self.__datos_mazos:
            self.__vista_mis_mazos.listMazos.addItem(str(mazo[1]))
            
        self.__vista_mis_mazos.listMazos.currentRowChanged.connect(self.mostrar_detalles_mazo)
        self.__vista_mis_mazos.btnEliminarMazo.clicked.connect(self.procesar_eliminacion_mazo)
        self.__vista_mis_mazos.show()

    def mostrar_detalles_mazo(self, fila_seleccionada):
        if fila_seleccionada < 0:
            return
            
        mazo = self.__datos_mazos[fila_seleccionada]
        id_mazo = mazo[0]
        nombre_campeon = mazo[2]
        
        self.__vista_mis_mazos.lblCampeon.setText(f"Campeón: {nombre_campeon}")
        
        cartas = self.__modelo.obtener_detalles_mazo(id_mazo)
        texto_detalles = ""
        for nom_carta, nivel in cartas:
            texto_detalles += f"• {nom_carta} (Nivel {nivel})\n"
            
        self.__vista_mis_mazos.txtDetalleCartas.setText(texto_detalles)

    def procesar_eliminacion_mazo(self):
        fila = self.__vista_mis_mazos.listMazos.currentRow()
        if fila < 0:
            return
            
        id_mazo = self.__datos_mazos[fila][0]
        exito = self.__modelo.eliminar_mazo_db(id_mazo)
        
        if exito:
            print("Mazo eliminado correctamente")
            self.__vista_mis_mazos.close()
            self.abrirMisMazos()
        else:
            print("Error al eliminar el mazo")

    # ================= PANEL DE ADMINISTRADOR =================
    def mostrar_admin_listas(self):
        self.__mods = self.__modelo.obtener_usuarios_por_rol(2)
        self.__users = self.__modelo.obtener_usuarios_por_rol(3)
        
        self.__admin.listModeradores.clear()
        for m in self.__mods:
            self.__admin.listModeradores.addItem(f"{m.nombre_usuario} ({m.correo})")
            
        self.__admin.listUsuariosBase.clear()
        for u in self.__users:
            self.__admin.listUsuariosBase.addItem(f"{u.nombre_usuario} ({u.correo})")

    def mostrar_menu_admin(self):
        self.__admin = VistaMenuAdmin()
        self.mostrar_admin_listas()
        
        self.__admin.btnEliminarMod.clicked.connect(self.eliminar_moderador_admin)
        self.__admin.btnEliminarUserBase.clicked.connect(self.eliminar_usuario_admin)
        self.__admin.btnRegistrarMod.clicked.connect(self.dar_alta_moderador)
        self.__admin.btnCerrarSesionAdmin.clicked.connect(self.cerrar_sesion_admin)
        self.__admin.show()

    def eliminar_moderador_admin(self):
        fila = self.__admin.listModeradores.currentRow()
        if fila >= 0:
            self.__modelo.eliminar_usuario_db(self.__mods[fila].id_usuario)
            self.mostrar_admin_listas()

    def eliminar_usuario_admin(self):
        fila = self.__admin.listUsuariosBase.currentRow()
        if fila >= 0:
            self.__modelo.eliminar_usuario_db(self.__users[fila].id_usuario)
            self.mostrar_admin_listas()

    def dar_alta_moderador(self):
        nom = self.__admin.txtAltaNombre.text()
        usr = self.__admin.txtAltaUser.text()
        corr = self.__admin.txtAltaCorreo.text()
        pas = self.__admin.txtAltaPass.text()
        
        if nom and usr and corr and pas:
            nuevo_mod = UsuarioVO(None, nom, usr, corr, pas, 0, 2)
            self.__modelo.Insert(nuevo_mod)
            self.mostrar_admin_listas()
            self.__admin.txtAltaNombre.clear()
            self.__admin.txtAltaUser.clear()
            self.__admin.txtAltaCorreo.clear()
            self.__admin.txtAltaPass.clear()

    def cerrar_sesion_admin(self):
        self.__admin.close()
        self.usuario_actual = None
        self.usuario_actual_id = None
        self.abrirIniciarSesion()

    # ================= PANEL DE MODERADOR =================
    def mostrar_moderador_datos(self):
        self.__mazos_globales = self.__modelo.obtener_todos_los_mazos_global()
        self.__torneos_globales = self.__modelo.obtener_torneos()
        
        self.__mod_view.listMazosGlobal.clear()
        for m in self.__mazos_globales:
            self.__mod_view.listMazosGlobal.addItem(f"Mazo: {m[1]} | Creador: {m[2]}")
            
        self.__mod_view.listTorneosMod.clear()
        for t in self.__torneos_globales:
            if hasattr(t, 'nombre'):
                self.__mod_view.listTorneosMod.addItem(t.nombre)
            else:
                self.__mod_view.listTorneosMod.addItem(str(t[1]))

    def mostrar_menu_moderador(self):
        self.__mod_view = VistaMenuModerador()
        self.mostrar_moderador_datos()
        
        self.__mod_view.listTorneosMod.currentRowChanged.connect(self.cargar_participantes_moderacion)
        self.__mod_view.btnEliminarMazoGlobal.clicked.connect(self.eliminar_mazo_moderador)
        self.__mod_view.btnEliminarTorneo.clicked.connect(self.eliminar_torneo_moderador)
        self.__mod_view.btnEliminarParticipante.clicked.connect(self.expulsar_participante_moderador)
        self.__mod_view.btnGuardarTorneo.clicked.connect(self.crear_torneo_moderador)
        self.__mod_view.btnCerrarSesionMod.clicked.connect(self.cerrar_sesion_moderador)
        self.__mod_view.show()

    def cargar_participantes_moderacion(self, fila):
        self.__mod_view.listParticipantes.clear()
        if fila < 0:
            return
        id_torneo = self.__torneos_globales[fila].id_torneo
        self.__participantes_actuales = self.__modelo.obtener_participantes_torneo(id_torneo)
        for p in self.__participantes_actuales:
            self.__mod_view.listParticipantes.addItem(f"User ID: {p[0]} - {p[1]} ({p[2]})")

    def eliminar_mazo_moderador(self):
        fila = self.__mod_view.listMazosGlobal.currentRow()
        if fila >= 0:
            id_mazo = self.__mazos_globales[fila][0]
            self.__modelo.eliminar_mazo_db(id_mazo)
            self.mostrar_moderador_datos()

    def eliminar_torneo_moderador(self):
        fila = self.__mod_view.listTorneosMod.currentRow()
        if fila >= 0:
            id_torneo = self.__torneos_globales[fila].id_torneo
            self.__modelo.eliminar_torneo_db(id_torneo)
            self.mostrar_moderador_datos()
            self.__mod_view.listParticipantes.clear()

    def expulsar_participante_moderador(self):
        fila_t = self.__mod_view.listTorneosMod.currentRow()
        fila_p = self.__mod_view.listParticipantes.currentRow()
        if fila_t >= 0 and fila_p >= 0:
            id_torneo = self.__torneos_globales[fila_t].id_torneo
            id_usuario = self.__participantes_actuales[fila_p][0]
            self.__modelo.eliminar_participante_torneo(id_usuario, id_torneo)
            self.cargar_participantes_moderacion(fila_t)

    def crear_torneo_moderador(self):
        nom = self.__mod_view.txtNombreTorneo.text()
        ub = self.__mod_view.txtUbicacionTorneo.text()
        desc = self.__mod_view.txtDescTorneo.text()
        reg = self.__mod_view.txtReglasTorneo.text()
        
        if nom and ub:
            nuevo_torneo = TorneoVO(None, nom, ub, desc, reg)
            self.__modelo.añadir_torneo_db(nuevo_torneo)
            self.mostrar_moderador_datos()
            self.__mod_view.txtNombreTorneo.clear()
            self.__mod_view.txtUbicacionTorneo.clear()
            self.__mod_view.txtDescTorneo.clear()
            self.__mod_view.txtReglasTorneo.clear()

    def cerrar_sesion_moderador(self):
        self.__mod_view.close()
        self.usuario_actual = None
        self.usuario_actual_id = None
        self.abrirIniciarSesion()