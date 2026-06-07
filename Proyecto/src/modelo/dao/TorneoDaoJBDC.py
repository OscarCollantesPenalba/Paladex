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

    def obtener_todos_los_torneos(self):
        return self.select_all()

    def inscribir_participante(self, id_usuario, id_torneo, alias, equipo):
        cursor = self.getCursor()
        if not cursor:
            return False
        try:
            sql = "INSERT INTO Participantes (id_usuario, id_torneo, alias, equipo, win, loss) VALUES (?, ?, ?, ?, 0, 0)"
            cursor.execute(sql, (id_usuario, id_torneo, alias, equipo))
            return True
        except Exception as e:
            print(f"Error TorneoDaoJBDC Inscripcion: {e}")
            return False
        finally:
            self.closeConnection()

    def insertar_nuevo_torneo(self, torneo_vo):
        cursor = self.getCursor()
        if not cursor:
            return False
        try:
            sql = "INSERT INTO Torneos (nombre, ubicacion, descripcion, reglas) VALUES (?, ?, ?, ?)"
            cursor.execute(sql, (torneo_vo.nombre, torneo_vo.ubicacion, torneo_vo.descripcion, torneo_vo.reglas))
            return True
        except Exception as e:
            print(f"Error TorneoDaoJBDC Insertar: {e}")
            return False
        finally:
            self.closeConnection()

    def eliminar_torneo_por_id(self, id_torneo):
        cursor = self.getCursor()
        if not cursor:
            return False
        try:
            cursor.execute("DELETE FROM Participantes WHERE id_torneo = ?", (id_torneo,))
            cursor.execute("DELETE FROM Torneos WHERE id_torneo = ?", (id_torneo,))
            return True
        except Exception as e:
            print(f"Error TorneoDaoJBDC Eliminar: {e}")
            return False
        finally:
            self.closeConnection()

    def obtener_participantes_torneo(self, id_torneo):
        cursor = self.getCursor()
        if not cursor:
            return []
        try:
            sql = "SELECT id_usuario, alias, equipo FROM Participantes WHERE id_torneo = ?"
            cursor.execute(sql, (id_torneo,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error TorneoDaoJBDC Participantes: {e}")
            return []
        finally:
            self.closeConnection()

    def eliminar_participante_torneo(self, id_usuario, id_torneo):
        cursor = self.getCursor()
        if not cursor:
            return False
        try:
            cursor.execute(
                "DELETE FROM Participantes WHERE id_usuario = ? AND id_torneo = ?",
                (id_usuario, id_torneo)
            )
            return True
        except Exception as e:
            print(f"Error TorneoDaoJBDC Borrar Participante: {e}")
            return False
        finally:
            self.closeConnection()