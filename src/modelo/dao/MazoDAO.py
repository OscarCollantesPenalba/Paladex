from src.modelo.conexion.Conexion import Conexion


class MazoDAO(Conexion):
    def __init__(self):
        super().__init__()

    def guardar_mazo_completo(self, mazo_vo):
        cursor = self.getCursor()
        if not cursor:
            return False
        try:
            sql_mazo = "INSERT INTO Mazos (nombre_mazo, descripcion, estado, id_usuario, id_campeon) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(sql_mazo, (mazo_vo.nombre_mazo, "Descripción mazo", "Activo", mazo_vo.id_usuario, mazo_vo.id_campeon))

            cursor.execute(
                "SELECT MAX(id_mazo) FROM Mazos WHERE id_usuario = ? AND nombre_mazo = ?",
                (mazo_vo.id_usuario, mazo_vo.nombre_mazo)
            )
            id_nuevo_mazo = cursor.fetchone()[0]

            sql_cartas = "INSERT INTO Mazo_Carta (id_mazo, id_carta, nivel_carta) VALUES (?, ?, ?)"
            datos = [(id_nuevo_mazo, id_carta, nivel) for id_carta, nivel in mazo_vo.lista_cartas]
            cursor.executemany(sql_cartas, datos)
            return True

        except Exception as e:
            print(f"Error MazoDAO guardar: {e}")
            return False
        finally:
            self.closeConnection()

    def obtener_cartas_por_campeon(self, id_campeon):
        cursor = self.getCursor()
        try:
            sql = "SELECT id_carta, nombre, descripcion, categoria FROM Cartas WHERE id_campeon = ?"
            cursor.execute(sql, (id_campeon,))
            return cursor.fetchall()
        except Exception as e:
            print(e)
            return []
        finally:
            self.closeConnection()

    def obtener_mazos_por_usuario(self, id_usuario):
        cursor = self.getCursor()
        if not cursor:
            return []
        try:
            sql = """
                SELECT m.id_mazo, m.nombre_mazo, c.nombre 
                FROM Mazos m 
                JOIN Campeon c ON m.id_campeon = c.id_campeon 
                WHERE m.id_usuario = ?
            """
            cursor.execute(sql, (id_usuario,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error MazoDAO Obtener: {e}")
            return []
        finally:
            self.closeConnection()

    def obtener_detalles_cartas_mazo(self, id_mazo):
        cursor = self.getCursor()
        if not cursor:
            return []
        try:
            sql = """
                SELECT c.nombre, mc.nivel_carta 
                FROM Mazo_Carta mc 
                JOIN Cartas c ON mc.id_carta = c.id_carta 
                WHERE mc.id_mazo = ?
            """
            cursor.execute(sql, (id_mazo,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error MazoDAO Detalles: {e}")
            return []
        finally:
            self.closeConnection()

    def eliminar_mazo_por_id(self, id_mazo):
        cursor = self.getCursor()
        if not cursor:
            return False
        try:
            cursor.execute("DELETE FROM Mazo_Carta WHERE id_mazo = ?", (id_mazo,))
            cursor.execute("DELETE FROM Mazos WHERE id_mazo = ?", (id_mazo,))
            return True
        except Exception as e:
            print(f"Error MazoDAO Eliminar: {e}")
            return False
        finally:
            self.closeConnection()

    def obtener_todos_los_mazos(self):
        cursor = self.getCursor()
        if not cursor:
            return []
        try:
            sql = """
                SELECT m.id_mazo, m.nombre_mazo, u.nombre_usuario 
                FROM Mazos m 
                JOIN Usuario u ON m.id_usuario = u.id_usuario
            """
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error MazoDAO Global: {e}")
            return []
        finally:
            self.closeConnection()