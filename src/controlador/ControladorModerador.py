from src.modelo.LogicaModerador import LogicaModerador


class ControladorModerador:

    def __init__(self, ref_vista, usuario_actual, ref_controlador_principal):
        self.__vista      = ref_vista
        self.__usuario    = usuario_actual
        self.__logica     = LogicaModerador()
        self.__ctrl_ppal  = ref_controlador_principal
        self.__mazos      = []
        self.__torneos    = []
        self.__participantes_actuales = []

    # ------------------------------------------------------------------ #
    # Arranque                                                             #
    # ------------------------------------------------------------------ #

    def inicializar(self):
        self.__vista.lblModerador.setText(f"🛡  {self.__usuario.nombre_usuario}")
        self._cargar_datos()

    def _cargar_datos(self):
        self.__mazos   = self.__logica.obtener_todos_los_mazos()
        self.__torneos = self.__logica.obtener_torneos()
        self.__vista.cargar_mazos(self.__mazos)
        self.__vista.cargar_torneos(self.__torneos)
        self.__vista.cargar_participantes([])

    # ------------------------------------------------------------------ #
    # Mazos                                                                #
    # ------------------------------------------------------------------ #

    def eliminar_mazo(self, fila):
        if fila < 0:
            self.__vista.mostrar_error("Selecciona un mazo primero.")
            return
        exito = self.__logica.ocultar_mazo(self.__mazos[fila][0], self.__usuario.id_usuario)
        if exito:
            self.__vista.mostrar_info("Mazo ocultado correctamente.")
            self._cargar_datos()
        else:
            self.__vista.mostrar_error("Error al ocultar el mazo.")

    # ------------------------------------------------------------------ #
    # Torneos                                                              #
    # ------------------------------------------------------------------ #

    def eliminar_torneo(self, fila):
        if fila < 0:
            self.__vista.mostrar_error("Selecciona un torneo primero.")
            return
        exito = self.__logica.eliminar_torneo(self.__torneos[fila].id_torneo)
        if exito:
            self.__vista.mostrar_info("Torneo eliminado correctamente.")
            self._cargar_datos()
        else:
            self.__vista.mostrar_error("Error al eliminar el torneo.")

    def cargar_participantes(self, fila):
        if fila < 0:
            return
        self.__participantes_actuales = self.__logica.obtener_participantes(
            self.__torneos[fila].id_torneo
        )
        self.__vista.cargar_participantes(self.__participantes_actuales)

    def expulsar_participante(self, fila_torneo, fila_participante):
        if fila_torneo < 0 or fila_participante < 0:
            self.__vista.mostrar_error("Selecciona un torneo y un participante.")
            return
        id_torneo  = self.__torneos[fila_torneo].id_torneo
        id_usuario = self.__participantes_actuales[fila_participante][0]
        exito = self.__logica.expulsar_participante(id_usuario, id_torneo)
        if exito:
            self.__vista.mostrar_info("Participante expulsado correctamente.")
            self.cargar_participantes(fila_torneo)
        else:
            self.__vista.mostrar_error("Error al expulsar el participante.")

    def crear_torneo(self, nombre, ubicacion, descripcion, reglas):
        if not nombre or not ubicacion:
            self.__vista.mostrar_error("El nombre y la ubicación son obligatorios.")
            return
        exito = self.__logica.crear_torneo(nombre, ubicacion, descripcion, reglas)
        if exito:
            self.__vista.mostrar_info("Torneo creado correctamente.")
            self.__vista.limpiar_formulario_torneo()
            self._cargar_datos()
        else:
            self.__vista.mostrar_error("Error al crear el torneo.")

    # ------------------------------------------------------------------ #
    # Sesión                                                               #
    # ------------------------------------------------------------------ #

    def cerrar_sesion(self):
        self.__vista.close()
        self.__ctrl_ppal.abrirIniciarSesion()