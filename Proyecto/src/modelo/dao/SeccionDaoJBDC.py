from src.modelo.conexion.Conexion import Conexion


class SeccionDAO(Conexion):

    def __init__(self):
        super().__init__()

    def obtener_por_rango(self, id_inicio, id_fin):
        cursor = self.getCursor()
        if not cursor:
            return []
        try:
            cursor.execute(
                "SELECT id_seccion, titulo, contenido, url FROM secciones WHERE id_seccion BETWEEN ? AND ? ORDER BY id_seccion",
                (id_inicio, id_fin)
            )
            rows = cursor.fetchall()
            return [
                {
                    "titulo":      r[1],
                    "subtitulo":   "",
                    "descripcion": r[2],
                    "url":         r[3] if r[3] else ""
                }
                for r in rows
            ]
        except Exception as e:
            print(f"Error SeccionDAO: {e}")
            return []
        finally:
            self.closeConnection()