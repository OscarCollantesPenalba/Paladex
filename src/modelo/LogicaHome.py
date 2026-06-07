from src.modelo.dao.CampeonDaoJBDC import CampeonDaoJBDC
from src.modelo.dao.CartaDaoJBDC import CartaDaoJBDC
from src.modelo.dao.MazoDaoJBDC import MazoDaoJBDC
from src.modelo.dao.MazoDAO import MazoDAO
from src.modelo.dao.TorneoDaoJBDC import TorneoDaoJBDC
from src.modelo.dao.UsersDaoJBDC import UsersDaoJBDC
from src.modelo.dao.SeccionDaoJBDC import SeccionDAO
from src.modelo.dao.ModeradoDaoJBDC import ModeraDAO
from src.modelo.conexion.Conexion import Conexion


class LogicaHome:

    FILTRO_TODOS     = "Todos"
    FILTRO_CAMPEONES = "Campeones"
    FILTRO_CARTAS    = "Cartas"
    FILTRO_MAZOS     = "Mazos"
    FILTRO_TORNEOS   = "Torneos"

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
    # Detalle búsqueda                                                     #
    # ------------------------------------------------------------------ #

    def obtener_campeon(self, id_campeon):
        campeon = CampeonDaoJBDC().select_by_id(id_campeon)
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
    # Secciones (novedades, mapas, modos) desde BD                        #
    # ------------------------------------------------------------------ #

    def obtener_novedad(self, indice):
        secciones = SeccionDAO().obtener_por_rango(1, 3)
        return secciones[indice] if 0 <= indice < len(secciones) else None

    def obtener_mapa(self, indice):
        secciones = SeccionDAO().obtener_por_rango(4, 6)
        return secciones[indice] if 0 <= indice < len(secciones) else None

    def obtener_modo(self, indice):
        secciones = SeccionDAO().obtener_por_rango(7, 9)
        return secciones[indice] if 0 <= indice < len(secciones) else None

    # ------------------------------------------------------------------ #
    # Perfil                                                               #
    # ------------------------------------------------------------------ #

    def obtener_perfil(self, id_usuario):
        return UsersDaoJBDC().obtener_perfil_por_id(id_usuario)

    def obtener_estadisticas(self, id_usuario):
        return UsersDaoJBDC().obtener_totales_participante(id_usuario)

    def registrar_resultado_combate(self, id_usuario, es_victoria):
        try:
            dao = UsersDaoJBDC()
            usuario_vo = dao.obtener_perfil_por_id(id_usuario)
            stats = dao.obtener_totales_participante(id_usuario)
            if not usuario_vo:
                return False
            victorias, derrotas = stats[0], stats[1]
            if es_victoria:
                victorias += 1
                usuario_vo.puntos_experiencia += 25
            else:
                derrotas += 1
                usuario_vo.puntos_experiencia = max(0, usuario_vo.puntos_experiencia - 10)
            if usuario_vo.id_rol == 3 and usuario_vo.puntos_experiencia >= 100:
                usuario_vo.id_rol = 2
            elif usuario_vo.id_rol == 2 and usuario_vo.puntos_experiencia < 100:
                usuario_vo.id_rol = 3
            return dao.actualizar_progreso_usuario(
                id_usuario, victorias, derrotas,
                usuario_vo.puntos_experiencia, usuario_vo.id_rol
            )
        except Exception as e:
            print(f"Error registrar_resultado_combate: {e}")
            return False

    # ------------------------------------------------------------------ #
    # Mazos                                                                #
    # ------------------------------------------------------------------ #

    def obtener_campeones(self):
        conexion_obj = Conexion()
        conexion = conexion_obj.createConnection()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_campeon, nombre FROM campeon")
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultados

    def obtener_cartas_por_campeon(self, id_campeon):
        return MazoDAO().obtener_cartas_por_campeon(id_campeon)

    def guardar_mazo(self, mazo_vo):
        id_nuevo = MazoDAO().guardar_mazo_completo(mazo_vo)
        if id_nuevo:
            ModeraDAO().registrar_log(mazo_vo.id_usuario, id_nuevo, "publicado", "Mazo publicado por el creador")
        return id_nuevo is not None

    def obtener_mazos_usuario(self, id_usuario):
        return MazoDAO().obtener_mazos_por_usuario(id_usuario)

    def obtener_detalles_mazo(self, id_mazo):
        return MazoDAO().obtener_detalles_cartas_mazo(id_mazo)

    def eliminar_mazo(self, id_mazo):
        return MazoDAO().eliminar_mazo_por_id(id_mazo)

    # ------------------------------------------------------------------ #
    # Torneos                                                              #
    # ------------------------------------------------------------------ #

    def obtener_torneos(self):
        return TorneoDaoJBDC().obtener_todos_los_torneos()

    def inscribir_usuario_torneo(self, id_usuario, id_torneo, alias, equipo):
        return TorneoDaoJBDC().inscribir_participante(id_usuario, id_torneo, alias, equipo)