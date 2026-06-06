from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.CartaVo import CartaVO


class CartaDaoJBDC(Conexion):

    SQL_SELECT_ALL = """
        SELECT ca.id_carta, ca.nombre, ca.descripcion, ca.categoria,
               ca.id_campeon, c.nombre
        FROM cartas ca
        LEFT JOIN campeon c ON ca.id_campeon = c.id_campeon
    """

    SQL_SEARCH = """
        SELECT ca.id_carta, ca.nombre, ca.descripcion, ca.categoria,
               ca.id_campeon, c.nombre
        FROM cartas ca
        LEFT JOIN campeon c ON ca.id_campeon = c.id_campeon
        WHERE ca.nombre LIKE ? OR ca.descripcion LIKE ? OR ca.categoria LIKE ? OR c.nombre LIKE ?
    """

    SQL_SELECT_BY_ID = """
        SELECT ca.id_carta, ca.nombre, ca.descripcion, ca.categoria,
               ca.id_campeon, c.nombre
        FROM cartas ca
        LEFT JOIN campeon c ON ca.id_campeon = c.id_campeon
        WHERE ca.id_carta = ?
    """

    SQL_SELECT_BY_CAMPEON = """
        SELECT ca.id_carta, ca.nombre, ca.descripcion, ca.categoria,
               ca.id_campeon, c.nombre
        FROM cartas ca
        LEFT JOIN campeon c ON ca.id_campeon = c.id_campeon
        WHERE ca.id_campeon = ?
    """

    def __init__(self):
        super().__init__()

    def _fila_a_carta(self, row):
        id_carta, nombre, descripcion, categoria, id_campeon, nombre_campeon = row
        return CartaVO(id_carta, nombre, descripcion, categoria, id_campeon, nombre_campeon)

    def select_all(self):
        cursor = self.getCursor()
        cartas = []

        try:
            cursor.execute(self.SQL_SELECT_ALL)
            rows = cursor.fetchall()
            for row in rows:
                cartas.append(self._fila_a_carta(row))

        except Exception as e:
            print("Error al obtener cartas:", e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

        return cartas

    def search(self, termino):
        cursor = self.getCursor()
        cartas = []
        like = f"%{termino}%"

        try:
            cursor.execute(self.SQL_SEARCH, (like, like, like, like))
            rows = cursor.fetchall()
            for row in rows:
                cartas.append(self._fila_a_carta(row))

        except Exception as e:
            print("Error al buscar cartas:", e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

        return cartas

    def select_by_id(self, id_carta):
        cursor = self.getCursor()
        carta = None

        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_carta,))
            row = cursor.fetchone()
            if row:
                carta = self._fila_a_carta(row)

        except Exception as e:
            print("Error al obtener carta por ID:", e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

        return carta

    def select_by_campeon(self, id_campeon):
        cursor = self.getCursor()
        cartas = []

        try:
            cursor.execute(self.SQL_SELECT_BY_CAMPEON, (id_campeon,))
            rows = cursor.fetchall()
            for row in rows:
                cartas.append(self._fila_a_carta(row))

        except Exception as e:
            print("Error al obtener cartas por campeon:", e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

        return cartas