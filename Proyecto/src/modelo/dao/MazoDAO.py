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
            
            cursor.execute("SELECT LAST_INSERT_ID()")
            resultado = cursor.fetchone()
            id_nuevo_mazo = resultado[0]
            
            sql_cartas = "INSERT INTO Mazo_Carta (id_mazo, id_carta, nivel_carta) VALUES (?, ?, ?)"
            
            datos_para_insertar = []
            for id_carta, nivel in mazo_vo.lista_cartas:
                datos_para_insertar.append((id_nuevo_mazo, id_carta, nivel))
            
            cursor.executemany(sql_cartas, datos_para_insertar)
            
            self.conexion.commit()
            return True
            
        except Exception as e:
            if self.conexion:
                self.conexion.rollback()
            print(f"Error: {e}")
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