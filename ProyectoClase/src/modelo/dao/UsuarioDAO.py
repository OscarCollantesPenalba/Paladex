from modelo.conexion.Conexion import Conexion
from modelo.vo.UsuarioVO import UsuarioVO

class UsuarioDAO(Conexion):
    def __init__(self):
        super().__init__()
        self.SQL_INSERT = "INSERT INTO Usuario (id_usuario, nombre_Usuario, correo, contrasena, id_rol) VALUES (%s, %s, %s, %s, %s)"

    def registrar_usuario(self, usuario: UsuarioVO):
        cursor = self.getCursor()
        try:
            datos = (usuario.nombre, usuario.correo, usuario.contrasena)
            cursor.execute(self.SQL_INSERT, datos)
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en DAO: {e}")
            return False
        finally:
            self.closeConnection()