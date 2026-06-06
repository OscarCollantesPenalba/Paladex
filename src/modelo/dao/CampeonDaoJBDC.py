from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.CampeonVo import CampeonVO
from src.modelo.vo.HabilidadVo import HabilidadVO


class CampeonDaoJBDC(Conexion):

    SQL_SELECT_ALL = """
        SELECT c.id_campeon, c.nombre, c.titulo, c.salud, c.daño, c.velocidad,
               c.id_clase, cc.nombre_clase
        FROM campeon c
        LEFT JOIN clase_campeon cc ON c.id_clase = cc.id_clase
    """

    SQL_SEARCH = """
        SELECT c.id_campeon, c.nombre, c.titulo, c.salud, c.daño, c.velocidad,
               c.id_clase, cc.nombre_clase
        FROM campeon c
        LEFT JOIN clase_campeon cc ON c.id_clase = cc.id_clase
        WHERE c.nombre LIKE ? OR c.titulo LIKE ? OR cc.nombre_clase LIKE ?
    """

    SQL_SELECT_BY_ID = """
        SELECT c.id_campeon, c.nombre, c.titulo, c.salud, c.daño, c.velocidad,
               c.id_clase, cc.nombre_clase
        FROM campeon c
        LEFT JOIN clase_campeon cc ON c.id_clase = cc.id_clase
        WHERE c.id_campeon = ?
    """

    SQL_HABILIDADES_BY_CAMPEON = """
        SELECT id_habilidad, nombre, tipo, descripcion, id_campeon
        FROM habilidades
        WHERE id_campeon = ?
    """

    def __init__(self):
        super().__init__()

    def _fila_a_campeon(self, row):
        id_campeon, nombre, titulo, salud, daño, velocidad, id_clase, nombre_clase = row
        return CampeonVO(id_campeon, nombre, titulo, salud, daño, velocidad, id_clase, nombre_clase)

    def select_all(self):
        cursor = self.getCursor()
        campeones = []

        try:
            cursor.execute(self.SQL_SELECT_ALL)
            rows = cursor.fetchall()
            for row in rows:
                campeones.append(self._fila_a_campeon(row))

        except Exception as e:
            print("Error al obtener campeones:", e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

        return campeones

    def search(self, termino):
        cursor = self.getCursor()
        campeones = []
        like = f"%{termino}%"

        try:
            cursor.execute(self.SQL_SEARCH, (like, like, like))
            rows = cursor.fetchall()
            for row in rows:
                campeones.append(self._fila_a_campeon(row))

        except Exception as e:
            print("Error al buscar campeones:", e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

        return campeones

    def select_by_id(self, id_campeon):
        cursor = self.getCursor()
        campeon = None

        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_campeon,))
            row = cursor.fetchone()
            if row:
                campeon = self._fila_a_campeon(row)
                campeon.habilidades = self._get_habilidades(campeon.id_campeon)

        except Exception as e:
            print("Error al obtener campeon por ID:", e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

        return campeon

    def _get_habilidades(self, id_campeon):
        """Carga las habilidades de un campeon. Usa su propia conexion."""
        dao = CampeonDaoJBDC()
        cursor = dao.getCursor()
        habilidades = []

        try:
            cursor.execute(self.SQL_HABILIDADES_BY_CAMPEON, (id_campeon,))
            rows = cursor.fetchall()
            for row in rows:
                id_hab, nombre, tipo, descripcion, id_camp = row
                habilidades.append(HabilidadVO(id_hab, nombre, tipo, descripcion, id_camp))

        except Exception as e:
            print("Error al obtener habilidades:", e)

        finally:
            if cursor:
                cursor.close()
            dao.closeConnection()

        return habilidades