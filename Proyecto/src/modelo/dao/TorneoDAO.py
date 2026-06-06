from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.TorneoVO import TorneoVO

class TorneoDAO(Conexion):
    def __init__(self):
        super().__init__()

    def obtener_todos_los_torneos(self):
        cursor = self.getCursor()
        if not cursor:
            return []
        try:
            cursor.execute("SELECT id_torneo, nombre, ubicacion, descripcion, reglas FROM Torneos")
            filas = cursor.fetchall()
            cursor.close()
            
            torneos = []
            for f in filas:
                torneos.append(TorneoVO(f[0], f[1], f[2], f[3], f[4]))
            return torneos
        except Exception as e:
            print(f"Error crítico en TorneoDAO.obtener_todos_los_torneos: {e}")
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

    def insertar_nuevo_torneo(self, torneo_vo):
        cursor = self.getCursor()
        if not cursor:
            return False
        try:
            sql = "INSERT INTO Torneos (nombre, ubicacion, descripcion, reglas) VALUES (?, ?, ?, ?)"
            cursor.execute(sql, (torneo_vo.nombre, torneo_vo.ubicacion, torneo_vo.descripcion, torneo_vo.reglas))
            self.conexion.commit()
            return True
        except Exception as e:
            if self.conexion:
                self.conexion.rollback()
            print(f"Error TorneoDAO Insertar: {e}")
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
            self.conexion.commit()
            return True
        except Exception as e:
            if self.conexion:
                self.conexion.rollback()
            print(f"Error TorneoDAO Eliminar: {e}")
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
            print(f"Error TorneoDAO Participantes: {e}")
            return []
        finally:
            self.closeConnection()

    def eliminar_participante_torneo(self, id_usuario, id_torneo):
        cursor = self.getCursor()
        if not cursor:
            return False
        try:
            cursor.execute("DELETE FROM Participantes WHERE id_usuario = ? AND id_torneo = ?", (id_usuario, id_torneo))
            self.conexion.commit()
            return True
        except Exception as e:
            if self.conexion:
                self.conexion.rollback()
            print(f"Error TorneoDAO Borrar Participante: {e}")
            return False
        finally:
            self.closeConnection()