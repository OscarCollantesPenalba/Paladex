from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.TorneoVo import TorneoVO


class TorneoDaoJBDC(Conexion):

    SQL_SELECT_ALL = """
        SELECT id_torneo, nombre, ubicacion, descripcion, reglas
        FROM torneos
    """

    SQL_SEARCH = """
        SELECT id_torneo, nombre, ubicacion, descripcion, reglas
        FROM torneos
        WHERE nombre LIKE ? OR ubicacion LIKE ? OR descripcion LIKE ?
    """

    SQL_SELECT_BY_ID = """
        SELECT id_torneo, nombre, ubicacion, descripcion, reglas
        FROM torneos
        WHERE id_torneo = ?
    """

    def __init__(self):
        super().__init__()

    def _fila_a_torneo(self, row):
        id_torneo, nombre, ubicacion, descripcion, reglas = row
        return TorneoVO(id_torneo, nombre, ubicacion, descripcion, reglas)

    def select_all(self):
        cursor = self.getCursor()
        torneos = []

        try:
            cursor.execute(self.SQL_SELECT_ALL)
            rows = cursor.fetchall()
            for row in rows:
                torneos.append(self._fila_a_torneo(row))

        except Exception as e:
            print("Error al obtener torneos:", e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

        return torneos

    def search(self, termino):
        cursor = self.getCursor()
        torneos = []
        like = f"%{termino}%"

        try:
            cursor.execute(self.SQL_SEARCH, (like, like, like))
            rows = cursor.fetchall()
            for row in rows:
                torneos.append(self._fila_a_torneo(row))

        except Exception as e:
            print("Error al buscar torneos:", e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

        return torneos

    def select_by_id(self, id_torneo):
        cursor = self.getCursor()
        torneo = None

        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_torneo,))
            row = cursor.fetchone()
            if row:
                torneo = self._fila_a_torneo(row)

        except Exception as e:
            print("Error al obtener torneo por ID:", e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

        return torneo