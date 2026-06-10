from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.MazoVo import MazoVO
from src.modelo.vo.CartaVo import CartaVO


class MazoDaoJBDC(Conexion):

    SQL_SELECT_ALL = """
        SELECT m.id_mazo, m.nombre_mazo, m.descripcion, m.estado,
               m.id_usuario, m.id_campeon, m.es_oficial,
               c.nombre, u.nombre_usuario
        FROM mazos m
        LEFT JOIN campeon c ON m.id_campeon = c.id_campeon
        LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
    """

    SQL_SEARCH = """
        SELECT m.id_mazo, m.nombre_mazo, m.descripcion, m.estado,
               m.id_usuario, m.id_campeon, m.es_oficial,
               c.nombre, u.nombre_usuario
        FROM mazos m
        LEFT JOIN campeon c ON m.id_campeon = c.id_campeon
        LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
        WHERE m.nombre_mazo LIKE ? OR m.descripcion LIKE ? OR c.nombre LIKE ? OR u.nombre_usuario LIKE ?
    """

    SQL_SELECT_BY_ID = """
        SELECT m.id_mazo, m.nombre_mazo, m.descripcion, m.estado,
               m.id_usuario, m.id_campeon, m.es_oficial,
               c.nombre, u.nombre_usuario
        FROM mazos m
        LEFT JOIN campeon c ON m.id_campeon = c.id_campeon
        LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
        WHERE m.id_mazo = ?
    """

    SQL_CARTAS_BY_MAZO = """
        SELECT ca.id_carta, ca.nombre, ca.descripcion, ca.categoria,
               ca.id_campeon, c.nombre, mc.nivel_carta
        FROM mazo_carta mc
        JOIN cartas ca ON mc.id_carta = ca.id_carta
        LEFT JOIN campeon c ON ca.id_campeon = c.id_campeon
        WHERE mc.id_mazo = ?
    """

    SQL_SELECT_BY_USUARIO = """
        SELECT m.id_mazo, m.nombre_mazo, m.descripcion, m.estado,
               m.id_usuario, m.id_campeon, m.es_oficial,
               c.nombre, u.nombre_usuario
        FROM mazos m
        LEFT JOIN campeon c ON m.id_campeon = c.id_campeon
        LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
        WHERE m.id_usuario = ?
    """

    def __init__(self):
        super().__init__()

    def _fila_a_mazo(self, row):
        id_mazo, nombre_mazo, descripcion, estado, id_usuario, id_campeon, es_oficial, nombre_campeon, nombre_usuario = row
        return MazoVO(id_mazo, nombre_mazo, descripcion, estado, id_usuario, id_campeon, es_oficial, nombre_campeon, nombre_usuario)

    def select_all(self):
        cursor = self.getCursor()
        mazos = []

        try:
            cursor.execute(self.SQL_SELECT_ALL)
            rows = cursor.fetchall()
            for row in rows:
                mazos.append(self._fila_a_mazo(row))

        except Exception as e:
            print("Error al obtener mazos:", e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

        return mazos

    def search(self, termino):
        cursor = self.getCursor()
        mazos = []
        like = f"%{termino}%"

        try:
            cursor.execute(self.SQL_SEARCH, (like, like, like, like))
            rows = cursor.fetchall()
            for row in rows:
                mazos.append(self._fila_a_mazo(row))

        except Exception as e:
            print("Error al buscar mazos:", e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

        return mazos

    def select_by_id(self, id_mazo):
        cursor = self.getCursor()
        mazo = None

        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_mazo,))
            row = cursor.fetchone()
            if row:
                mazo = self._fila_a_mazo(row)
                mazo.cartas = self._get_cartas(mazo.id_mazo)

        except Exception as e:
            print("Error al obtener mazo por ID:", e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

        return mazo

    def select_by_usuario(self, id_usuario):
        cursor = self.getCursor()
        mazos = []

        try:
            cursor.execute(self.SQL_SELECT_BY_USUARIO, (id_usuario,))
            rows = cursor.fetchall()
            for row in rows:
                mazos.append(self._fila_a_mazo(row))

        except Exception as e:
            print("Error al obtener mazos por usuario:", e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

        return mazos

    def _get_cartas(self, id_mazo):
        """Carga las cartas de un mazo con su nivel. Usa su propia conexion."""
        dao = MazoDaoJBDC()
        cursor = dao.getCursor()
        cartas = []

        try:
            cursor.execute(self.SQL_CARTAS_BY_MAZO, (id_mazo,))
            rows = cursor.fetchall()
            for row in rows:
                id_carta, nombre, descripcion, categoria, id_campeon, nombre_campeon, nivel_carta = row
                carta = CartaVO(id_carta, nombre, descripcion, categoria, id_campeon, nombre_campeon)
                carta.nivel = nivel_carta  # nivel especifico dentro del mazo
                cartas.append(carta)

        except Exception as e:
            print("Error al obtener cartas del mazo:", e)

        finally:
            if cursor:
                cursor.close()
            dao.closeConnection()

        return cartas