from modelo.conexion.Conexion import Conexion

class RolDAO(Conexion):
    def __init__(self):
        super().__init__()

    def insertar_roles_iniciales(self):
        cursor = self.getCursor()
        if not cursor: return
        
        try:
            sql = "INSERT INTO Rol (id_rol, nombre_rol) VALUES (%s, %s)"
            roles = [
                (1, 'Jugador'),
                (2, 'Moderador'),
                (3, 'Administrador')
            ]
            cursor.executemany(sql, roles)
            self.conexion.commit()
            print("Roles iniciales verificados/insertados.")
        except Exception as e:
            print(f"Error al insertar roles: {e}")
        finally:
            self.closeConnection()