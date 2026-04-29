from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuarioVo import UsuarioVO
from src.modelo.vo.LoginVO import LoginVO
class UsersDaoJBDC (Conexion):
    # Un DAO para cada tabla de la base de datos
    SQL_SELECT = "SELECT id_usuario, nombre_completo,nombre_usuario, correo, contrasena,puntos_experiencia FROM usuario"
    SQL_INSERT = "INSERT INTO Usuario(nombre_completo,nombre_usuario, correo, contrasena,puntos_experiencia, id_rol) VALUES (?, ?, ?, ?,?,?)" 
    SQL_CHECK_LOGIN = "SELECT * FROM Usuario WHERE nombre_usuario = ? AND contrasena = ? "
    SQL_CHEK_SIGN = "SELECT * FROM Usuario WHERE nombre_usuario = ? OR correo = ?"
    
    def __init__ (self):
        super().__init__()

    def select (self):
        cursor = self.getCursor()
        usuarios = []

        try :
            cursor.execute(self.SQL_SELECT)
            rows = cursor.fetchall()

            for row in rows:
                id_usuario, nombre_completo,nombre_usuario, correo, contrasena,puntos_experiencia = row     
                usuario = UsuarioVO (id_usuario, nombre_completo,nombre_usuario, correo, contrasena,puntos_experiencia)   
                usuarios.append(usuario)

        except Exception as e:
            print (e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()


        return usuarios
    
    def insert(self, usuario: UsuarioVO):
        cursor = self.getCursor() 
        rows = 0
        try :
            cursor.execute(self.SQL_INSERT,(
                        usuario.nombre_completo, 
                        usuario.nombre_usuario, 
                        usuario.correo, 
                        usuario.contrasena, 
                        usuario.puntos_experiencia,
                        usuario.id_rol))
            
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar usuario:", e)
        
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

        return rows


    def check_login (self, login: LoginVO):
        cursor = self.getCursor()

        try:
            cursor.execute(self.SQL_CHECK_LOGIN,(login.usuario, login.contrasena))
            row = cursor.fetchone()

            if row:
                id_usuario, nombre_completo,nombre_usuario, correo, contrasena,puntos_experiencia, id_rol  = row
                usuario = UsuarioVO (id_usuario, nombre_completo,nombre_usuario, correo, contrasena,puntos_experiencia, id_rol) 
                return usuario
            else: 
                return None

        except Exception as e:
            print(e)
        
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

    def chek_sign (self, usuario: UsuarioVO ):
        cursor = self.getCursor()

        try :
            cursor.execute(self.SQL_CHEK_SIGN,(usuario.nombre_usuario, usuario.correo))
            row = cursor.fetchone()
            
            if row :
                return row
            else: 
                return None

        except Exception as e:
            print(e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        