from src.modelo.LogicaHome import LogicaHome


class ControladorHome:

    def __init__(self, ref_vista, usuario_actual):
        self.__vista   = ref_vista
        self.__usuario = usuario_actual
        self.__logica  = LogicaHome()
        self.__resultados_actuales = []

    def inicializar(self):
        self.__vista.cargarUsuario(self.__usuario)
        self.buscar("", "Todos")

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
    # Clics GroupBox → PanelInfo                                           #
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