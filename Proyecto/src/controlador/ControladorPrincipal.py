from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.UsuarioVo import UsuarioVO
from src.vista.VistaMazo import VistaMazo
from src.modelo.vo.MazoVO import MazoVO
from src.vista.VistaMenu import VistaMenu
from src.vista.VistaTorneos import VistaTorneos
from src.vista.VistaPerfil import VistaPerfil
from src.vista.VistaMisMazos import VistaMisMazos

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
            if hasattr(resultado, 'id_usuario'):
                self.usuario_actual_id = resultado.id_usuario
            elif isinstance(resultado, (list, tuple)) and len(resultado) > 0:
                self.usuario_actual_id = resultado[0]
            else:
                self.usuario_actual_id = 1
                
            self.__vista.close()
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
        id_usuario = getattr(self, 'usuario_actual_id', 1)
        
        usuario_vo = self.__modelo.obtener_datos_perfil(id_usuario)
        stats_torneo = self.__modelo.obtener_estadisticas_torneo(id_usuario)
        
        if usuario_vo:
            nombre_usuario = usuario_vo.nombre_usuario
            xp = usuario_vo.puntos_experiencia if usuario_vo.puntos_experiencia is not None else 0
            nivel = (xp // 100) + 1
            
            self.__vista_perfil.lblUsuario.setText(f"Usuario: {nombre_usuario}")
            self.__vista_perfil.lblXP.setText(f"Puntos de Experiencia: {xp}")
            self.__vista_perfil.lblNivel.setText(f"Nivel: {nivel}")
            
        vistas = stats_torneo[0]
        derrotas = stats_torneo[1]
        
        self.__vista_perfil.lblVictorias.setText(str(vistas))
        self.__vista_perfil.lblDerrotas.setText(str(derrotas))
        
        self.__vista_perfil.show()

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
    