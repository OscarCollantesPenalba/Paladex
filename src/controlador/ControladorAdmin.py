from src.modelo.LogicaAdmin import LogicaAdmin


class ControladorAdmin:

    def __init__(self, ref_vista, usuario_actual, ref_controlador_principal):
        self.__vista     = ref_vista
        self.__usuario   = usuario_actual
        self.__logica    = LogicaAdmin()
        self.__ctrl_ppal = ref_controlador_principal
        self.__mods      = []
        self.__creadores = []
        self.__users     = []

    def inicializar(self):
        self.__vista.lblAdmin.setText(f"👑  {self.__usuario.nombre_usuario}")
        self._cargar_datos()

    def _cargar_datos(self):
        self.__mods      = self.__logica.obtener_usuarios_por_rol(1)
        self.__creadores = self.__logica.obtener_usuarios_por_rol(2)
        self.__users     = self.__logica.obtener_usuarios_por_rol(3)
        self.__vista.cargar_lista(self.__vista.listModeradores,    self.__mods)
        self.__vista.cargar_lista(self.__vista.listCreadoresMazos, self.__creadores)
        self.__vista.cargar_lista(self.__vista.listUsuariosBase,   self.__users)

    def cambiar_tab(self, indice):
        if indice == 1:  # pestaña logs
            logs = self.__logica.obtener_logs_moderacion()
            self.__vista.cargar_logs(logs)

    # ------------------------------------------------------------------ #
    # Acciones usuarios                                                    #
    # ------------------------------------------------------------------ #

    def eliminar_moderador(self, fila):
        if fila < 0:
            self.__vista.mostrar_error("Selecciona un moderador primero.")
            return
        exito = self.__logica.eliminar_usuario(self.__mods[fila].id_usuario)
        if exito:
            self.__vista.mostrar_info("Cuenta eliminada correctamente.")
            self._cargar_datos()
        else:
            self.__vista.mostrar_error("Error al eliminar la cuenta.")

    def degradar_creador(self, fila):
        if fila < 0:
            self.__vista.mostrar_error("Selecciona un creador primero.")
            return
        usuario = self.__creadores[fila]
        exito = self.__logica.cambiar_rol(usuario.id_usuario, 3)
        if exito:
            self.__vista.mostrar_info(f"'{usuario.nombre_usuario}' degradado a Lector.")
            self._cargar_datos()
        else:
            self.__vista.mostrar_error("Error al cambiar el rol.")

    def ascender_a_moderador(self, fila):
        if fila < 0:
            self.__vista.mostrar_error("Selecciona un usuario primero.")
            return
        usuario = self.__users[fila]
        exito = self.__logica.cambiar_rol(usuario.id_usuario, 1)
        if exito:
            self.__vista.mostrar_info(f"'{usuario.nombre_usuario}' ascendido a Moderador.")
            self._cargar_datos()
        else:
            self.__vista.mostrar_error("Error al cambiar el rol.")

    def cerrar_sesion(self):
        self.__vista.close()
        self.__ctrl_ppal.abrirIniciarSesion()