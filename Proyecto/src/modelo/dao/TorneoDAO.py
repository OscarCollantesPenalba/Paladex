from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.TorneoVO import TorneoVO

class TorneoDAO(Conexion):
    def __init__(self):
        super().__init__()

    def obtener_todos_los_torneos(self):
        cursor = self.getCursor()
        if not cursor:
            return []
        torneos = []
        try:
            cursor.execute("SELECT id_torneo, nombre, ubicacion, descripcion, reglas FROM Torneo")
            rows = cursor.fetchall()
            for row in rows:
                id_torneo, nombre, ubicacion, descripcion, reglas = row
                torneos.append(TorneoVO(id_torneo, nombre, ubicacion, descripcion, reglas))
            return torneos
        except Exception as e:
            print(f"Error TorneoDAO: {e}")
            return []
        finally:
            self.closeConnection()

    def inscribir_participante(self, id_usuario, id_torneo, alias, equipo):
        cursor = self.getCursor()
        if not cursor:
            return False
        try:
            sql = "INSERT INTO Participantes (id_usuario, id_torneo, alias, equipo, win, loss) VALUES (?, ?, ?, ?, 0, 0)"
            cursor.execute(sql, (id_usuario, id_torneo, alias, equipo))
            self.conexion.commit()
            return True
        except Exception as e:
            if self.conexion:
                self.conexion.rollback()
            print(f"Error TorneoDAO Inscripcion: {e}")
            return False
        finally:
            self.closeConnection()