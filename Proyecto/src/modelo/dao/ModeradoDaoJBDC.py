from src.modelo.conexion.Conexion import Conexion
from datetime import date


class ModeraDAO(Conexion):

    def __init__(self):
        super().__init__()

    def registrar_log(self, id_usuario, id_mazo, accion, comentario=""):
        cursor = self.getCursor()
        if not cursor:
            return False
        try:
            sql = """
                INSERT INTO modera_mazo (accion, comentario, fecha, id_usuario, id_mazo)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(sql, (accion, comentario, str(date.today()), id_usuario, id_mazo))
            return True
        except Exception as e:
            print(f"Error ModeraDAO registrar_log: {e}")
            return False
        finally:
            self.closeConnection()

    def obtener_todos_los_logs(self):
        cursor = self.getCursor()
        if not cursor:
            return []
        try:
            sql = """
                SELECT mm.id_moderacion, mm.accion, mm.comentario, mm.fecha,
                       u.nombre_usuario, m.nombre_mazo
                FROM modera_mazo mm
                JOIN usuario u ON mm.id_usuario = u.id_usuario
                JOIN mazos m   ON mm.id_mazo    = m.id_mazo
                ORDER BY mm.fecha DESC, mm.id_moderacion DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error ModeraDAO obtener_logs: {e}")
            return []
        finally:
            self.closeConnection()