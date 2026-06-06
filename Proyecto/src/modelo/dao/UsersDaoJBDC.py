from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuarioVo import UsuarioVO
from src.modelo.vo.LoginVO import LoginVO

class UsersDaoJBDC (Conexion):
    SQL_SELECT = "SELECT id_usuario, nombre_completo, nombre_usuario, correo, contrasena, puntos_experiencia, id_rol FROM Usuario"
    SQL_INSERT = "INSERT INTO Usuario(nombre_completo, nombre_usuario, correo, contrasena, puntos_experiencia, id_rol) VALUES (?, ?, ?, ?, ?, ?)" 
    SQL_CHECK_LOGIN = "SELECT id_usuario, nombre_completo, nombre_usuario, correo, contrasena, puntos_experiencia, id_rol FROM Usuario WHERE nombre_usuario = ? AND contrasena = ?"
    SQL_CHEK_SIGN = "SELECT * FROM Usuario WHERE nombre_usuario = ? OR correo = ?"
    
    def __init__ (self):
        super().__init__()

    def select (self):
        cursor = self.getCursor()
        usuarios = []

        try:
            cursor.execute(self.SQL_SELECT)
            rows = cursor.fetchall()

            for row in rows:
                usuario = UsuarioVO(row[0], row[1], row[2], row[3], row[4], row[5], row[6])   
                usuarios.append(usuario)

        except Exception as e:
            print(e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

        return usuarios
    
    def insert(self, usuario: UsuarioVO):
        cursor = self.getCursor() 
        rows = 0
        try:
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
                return UsuarioVO(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            else: 
                return None

        except Exception as e:
            print(e)
        
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

    def chek_sign (self, usuario: UsuarioVO):
        cursor = self.getCursor()

        try:
            cursor.execute(self.SQL_CHEK_SIGN,(usuario.nombre_usuario, usuario.correo))
            row = cursor.fetchone()
            
            if row:
                return row
            else: 
                return None

        except Exception as e:
            print(e)

        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
    
    def obtener_perfil_por_id(self, id_usuario):
        cursor = self.getCursor()
        try:
            cursor.execute("SELECT id_usuario, nombre_completo, nombre_usuario, correo, contrasena, puntos_experiencia, id_rol FROM Usuario WHERE id_usuario = ?", (id_usuario,))
            row = cursor.fetchone()
            if row:
                return UsuarioVO(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            return None
        except Exception as e:
            print(f"Error UsersDaoJBDC Perfil: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

    def obtener_totales_participante(self, id_usuario):
        cursor = self.getCursor()
        try:
            cursor.execute("SELECT SUM(win), SUM(loss) FROM Participantes WHERE id_usuario = ?", (id_usuario,))
            row = cursor.fetchone()
            if row:
                return (row[0] if row[0] is not None else 0, row[1] if row[1] is not None else 0)
            return (0, 0)
        except Exception as e:
            print(f"Error UsersDaoJBDC Stats: {e}")
            return (0, 0)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

    def obtener_usuarios_por_rol(self, id_rol):
        cursor = self.getCursor()
        if not cursor:
            return []
        try:
            cursor.execute("SELECT id_usuario, nombre_completo, nombre_usuario, correo, contrasena, puntos_experiencia, id_rol FROM Usuario WHERE id_rol = ?", (id_rol,))
            rows = cursor.fetchall()
            usuarios = []
            for row in rows:
                usuarios.append(UsuarioVO(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
            return usuarios
        except Exception as e:
            print(f"Error UsersDaoJBDC Obtener por Rol: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

    def eliminar_usuario_por_id(self, id_usuario):
        cursor = self.getCursor()
        if not cursor:
            return False
        try:
            cursor.execute("DELETE FROM Usuario WHERE id_usuario = ?", (id_usuario,))
            self.conexion.commit()
            return True
        except Exception as e:
            if self.conexion:
                self.conexion.rollback()
            print(f"Error UsersDaoJBDC Eliminar Usuario: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

    def actualizar_progreso_usuario(self, id_usuario, nuevas_victorias, nuevas_derrotas, nueva_xp, nuevo_rol):
        cursor = self.getCursor()
        if not cursor:
            return False
        try:
            sql = """
                UPDATE Usuario 
                SET puntos_experiencia = ?, id_rol = ? 
                WHERE id_usuario = ?
            """
            cursor.execute(sql, (nueva_xp, nuevo_rol, id_usuario))
            
            sql_participante = """
                UPDATE Participantes 
                SET win = ?, loss = ? 
                WHERE id_usuario = ?
            """
            cursor.execute(sql_participante, (nuevas_victorias, nuevas_derrotas, id_usuario))
            
            self.conexion.commit()
            return True
        except Exception as e:
            if self.conexion:
                self.conexion.rollback()
            print(f"Error UsersDaoJBDC actualizar progreso: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()