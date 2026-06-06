from src.modelo.dao.CampeonDaoJBDC import CampeonDaoJBDC
from src.modelo.dao.CartaDaoJBDC import CartaDaoJBDC
from src.modelo.dao.MazoDaoJBDC import MazoDaoJBDC
from src.modelo.dao.TorneoDaoJBDC import TorneoDaoJBDC


class LogicaHome:

    FILTRO_TODOS     = "Todos"
    FILTRO_CAMPEONES = "Campeones"
    FILTRO_CARTAS    = "Cartas"
    FILTRO_MAZOS     = "Mazos"
    FILTRO_TORNEOS   = "Torneos"

    # ------------------------------------------------------------------ #
    # Datos estáticos                                                      #
    # ------------------------------------------------------------------ #

    NOVEDADES = [
        {
            "titulo":      "Nuevo campeón: Lillith",
            "subtitulo":   "Clase: Daño  |  Disponible desde el parche 3.4",
            "descripcion": (
                "Lillith llega al campo de batalla con un estilo de juego agresivo "
                "y habilidades centradas en el control de área.\n\n"
                "Su ultimate, Tormenta de Sombras, inflige daño masivo en una zona "
                "amplia y reduce la curación de los enemigos afectados durante 3 segundos.\n\n"
                "Cartas destacadas:\n"
                "• Manto Oscuro: aumenta el daño de su habilidad pasiva un 10%.\n"
                "• Sombra Veloz: reduce el cooldown de su dash en 0.5s."
            ),
        },
        {
            "titulo":      "Parche 3.4 lanzado",
            "subtitulo":   "Balanceo general · Nuevas cartas · Corrección de errores",
            "descripcion": (
                "Cambios destacados del parche 3.4:\n\n"
                "• Fernando: reducción del 8% en el daño de su escudo.\n"
                "• Maeve: aumento del 5% en la velocidad de movimiento base.\n"
                "• Androxus: Reversal ahora puede reflejar habilidades de área.\n"
                "• Koga: el tiempo de recarga de Shadow Step se reduce en 0.3s.\n\n"
                "Correcciones:\n"
                "• El marcador de torneos ya muestra resultados en tiempo real.\n"
                "• Solucionado bug visual en el mapa Frozen Guard."
            ),
        },
        {
            "titulo":      "Evento: Semana del Dragón",
            "subtitulo":   "Del 1 al 7 de junio · Recompensas exclusivas",
            "descripcion": (
                "Durante la Semana del Dragón ganarás el doble de puntos de "
                "experiencia en cada partida clasificatoria.\n\n"
                "Desafíos diarios:\n"
                "• Día 1-2: Gana 3 partidas en modo Asalto.\n"
                "• Día 3-4: Consigue 20 eliminaciones con cualquier campeón.\n"
                "• Día 5-7: Juega 5 partidas en Jaguar Falls.\n\n"
                "Recompensa final: skin 'Dragón de Jade' para Koga."
            ),
        },
    ]

    MAPAS = [
        {
            "titulo":      "Stone Keep",
            "subtitulo":   "Modo: Asalto  |  5v5  |  Dificultad: Media",
            "descripcion": (
                "Stone Keep es el mapa más veterano de Paladex. Su diseño "
                "simétrico favorece tanto a los tanques de primera línea "
                "como a los tiradores de largo alcance.\n\n"
                "Características:\n"
                "• Pasillo central: el choke point principal del mapa.\n"
                "• Flancos laterales: rutas alternativas para asesinos.\n"
                "• Zona de objetivo: en el centro, fuertemente disputada.\n\n"
                "Campeones recomendados:\n"
                "Fernando (tanque), Viktor (tirador), Ying (soporte)."
            ),
        },
        {
            "titulo":      "Jaguar Falls",
            "subtitulo":   "Modo: Escolta  |  5v5  |  Dificultad: Alta",
            "descripcion": (
                "Jaguar Falls destaca por su vegetación densa y múltiples "
                "niveles de altura, perfecto para campeones con movilidad "
                "vertical y flanqueo agresivo.\n\n"
                "Características:\n"
                "• Cascadas: bloquean visión en el carril oeste.\n"
                "• Plataformas elevadas: ventaja para francotiradores.\n"
                "• Carga: avanza más rápido en el tramo final.\n\n"
                "Campeones recomendados:\n"
                "Maeve (flanco), Sha Lin (tirador), Jenos (soporte)."
            ),
        },
        {
            "titulo":      "Frozen Guard",
            "subtitulo":   "Modo: Sitio  |  5v5  |  Dificultad: Baja",
            "descripcion": (
                "Frozen Guard es un escenario invernal donde el ritmo "
                "más lento premia la coordinación de equipo y el control "
                "de zona sobre el duelo individual.\n\n"
                "Características:\n"
                "• Suelo helado: afecta a la velocidad de ciertos campeones.\n"
                "• Tres puntos de captura simultáneos.\n"
                "• Rutas de flanco muy expuestas, poco recomendadas.\n\n"
                "Campeones recomendados:\n"
                "Fernando (tanque), Cassie (daño), Grover (soporte)."
            ),
        },
    ]

    MODOS = [
        {
            "titulo":      "Asalto",
            "subtitulo":   "5v5  |  Objetivo: capturar y mantener el punto central",
            "descripcion": (
                "El modo más popular de Paladex. Dos equipos de 5 jugadores "
                "compiten por capturar y mantener el punto central del mapa.\n\n"
                "Reglas:\n"
                "• El equipo que acumule 100 puntos de captura gana la ronda.\n"
                "• Se juegan al mejor de 3 rondas.\n"
                "• Las eliminaciones otorgan créditos para comprar mejoras.\n\n"
                "Consejos:\n"
                "• Prioriza siempre el objetivo sobre las kills.\n"
                "• Un buen soporte puede cambiar el resultado del partido.\n"
                "• Coordina el uso de ultimates con tu equipo."
            ),
        },
        {
            "titulo":      "Escolta",
            "subtitulo":   "5v5  |  Objetivo: escoltar o detener la carga",
            "descripcion": (
                "Un equipo debe escoltar una carga hasta la meta mientras "
                "el equipo contrario intenta detenerla antes de que se agote "
                "el tiempo.\n\n"
                "Reglas:\n"
                "• La carga avanza mientras haya aliados cerca.\n"
                "• El equipo defensor gana si detiene la carga antes de la meta.\n"
                "• Los equipos intercambian roles al final de la primera ronda.\n\n"
                "Consejos:\n"
                "• Los tanques deben pegarse a la carga en todo momento.\n"
                "• Los flancos enemigos son la mayor amenaza para el soporte."
            ),
        },
        {
            "titulo":      "Sitio",
            "subtitulo":   "5v5  |  Objetivo: controlar múltiples puntos",
            "descripcion": (
                "El modo más estratégico de Paladex. Los equipos compiten "
                "por el control de tres puntos repartidos por el mapa.\n\n"
                "Reglas:\n"
                "• Cada punto controlado genera puntos cada segundo.\n"
                "• El primer equipo en llegar a 500 puntos gana.\n"
                "• Los puntos pueden ser capturados y reconquistados.\n\n"
                "Consejos:\n"
                "• Divide el equipo eficientemente entre los tres puntos.\n"
                "• No abandones un punto capturado sin dejar a alguien.\n"
                "• El punto central suele ser el más valioso y disputado."
            ),
        },
    ]

    # ------------------------------------------------------------------ #
    # Búsqueda                                                             #
    # ------------------------------------------------------------------ #

    def buscar(self, termino, filtro):
        termino = termino.strip()
        if filtro == self.FILTRO_CAMPEONES:
            return self._buscar_campeones(termino)
        elif filtro == self.FILTRO_CARTAS:
            return self._buscar_cartas(termino)
        elif filtro == self.FILTRO_MAZOS:
            return self._buscar_mazos(termino)
        elif filtro == self.FILTRO_TORNEOS:
            return self._buscar_torneos(termino)
        else:
            return (
                self._buscar_campeones(termino)
                + self._buscar_cartas(termino)
                + self._buscar_mazos(termino)
                + self._buscar_torneos(termino)
            )

    def _buscar_campeones(self, termino):
        dao = CampeonDaoJBDC()
        resultados = dao.search(termino) if termino else dao.select_all()
        return [("campeon", vo) for vo in resultados]

    def _buscar_cartas(self, termino):
        dao = CartaDaoJBDC()
        resultados = dao.search(termino) if termino else dao.select_all()
        return [("carta", vo) for vo in resultados]

    def _buscar_mazos(self, termino):
        dao = MazoDaoJBDC()
        resultados = dao.search(termino) if termino else dao.select_all()
        return [("mazo", vo) for vo in resultados]

    def _buscar_torneos(self, termino):
        dao = TorneoDaoJBDC()
        resultados = dao.search(termino) if termino else dao.select_all()
        return [("torneo", vo) for vo in resultados]

    # ------------------------------------------------------------------ #
    # Detalle                                                              #
    # ------------------------------------------------------------------ #

    def obtener_campeon(self, id_campeon):
        dao_campeon = CampeonDaoJBDC()
        campeon = dao_campeon.select_by_id(id_campeon)
        if campeon:
            campeon.cartas = CartaDaoJBDC().select_by_campeon(id_campeon)
        return campeon

    def obtener_carta(self, id_carta):
        dao = CartaDaoJBDC()
        carta = dao.select_by_id(id_carta)
        if carta and carta.id_campeon:
            carta.cartas_campeon = dao.select_by_campeon(carta.id_campeon)
        else:
            carta.cartas_campeon = []
        return carta

    def obtener_mazo(self, id_mazo):
        return MazoDaoJBDC().select_by_id(id_mazo)

    def obtener_torneo(self, id_torneo):
        return TorneoDaoJBDC().select_by_id(id_torneo)

    # ------------------------------------------------------------------ #
    # Acceso a datos estáticos                                             #
    # ------------------------------------------------------------------ #

    def obtener_novedad(self, indice):
        return self.NOVEDADES[indice] if 0 <= indice < len(self.NOVEDADES) else None

    def obtener_mapa(self, indice):
        return self.MAPAS[indice] if 0 <= indice < len(self.MAPAS) else None

    def obtener_modo(self, indice):
        return self.MODOS[indice] if 0 <= indice < len(self.MODOS) else None