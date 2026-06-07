from src.modelo.dao.MazoDAO import MazoDAO
from src.modelo.dao.TorneoDaoJBDC import TorneoDaoJBDC
from src.modelo.dao.ModeradoDaoJBDC import ModeraDAO
from src.modelo.vo.TorneoVo import TorneoVO


class LogicaModerador:

    # ------------------------------------------------------------------ #
    # Mazos                                                                #
    # ------------------------------------------------------------------ #

    def obtener_todos_los_mazos(self):
        return MazoDAO().obtener_todos_los_mazos()

    def ocultar_mazo(self, id_mazo, id_moderador):
        exito = MazoDAO().ocultar_mazo(id_mazo)
        if exito:
            ModeraDAO().registrar_log(id_moderador, id_mazo, "oculto", "Ocultado por moderador")
        return exito

    # ------------------------------------------------------------------ #
    # Torneos                                                              #
    # ------------------------------------------------------------------ #

    def obtener_torneos(self):
        return TorneoDaoJBDC().obtener_todos_los_torneos()

    def crear_torneo(self, nombre, ubicacion, descripcion, reglas):
        return TorneoDaoJBDC().insertar_nuevo_torneo(
            TorneoVO(None, nombre, ubicacion, descripcion, reglas)
        )

    def eliminar_torneo(self, id_torneo):
        return TorneoDaoJBDC().eliminar_torneo_por_id(id_torneo)

    def obtener_participantes(self, id_torneo):
        return TorneoDaoJBDC().obtener_participantes_torneo(id_torneo)

    def expulsar_participante(self, id_usuario, id_torneo):
        return TorneoDaoJBDC().eliminar_participante_torneo(id_usuario, id_torneo)