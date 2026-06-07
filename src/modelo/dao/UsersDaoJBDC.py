from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuarioVo import UsuarioVO
from src.modelo.vo.LoginVO import LoginVO


class UsersDaoJBDC(Conexion):

    SQL_SELECT      = "SELECT id_usuario, nombre_completo, nombre_usuario, correo, contrasena, puntos_experiencia, id_rol FROM Usuario"
    SQL_INSERT      = "INSERT INTO Usuario(nombre_completo, nombre_usuario, correo, contrasena, puntos_experiencia, id_rol) VALUES (?, ?, ?, ?, ?, ?)"
    SQL_CHECK_LOGIN = "SELECT id_usuario, nombre_completo, nombre_usuario, correo, contrasena, puntos_experiencia, id_rol FROM Usuario WHERE nombre_usuario = ? AND contrasena = ?"
    SQL_CHEK_SIGN   = "SELECT * FROM Usuario WHERE nombre_usuario = ? OR correo = ?"

    def __init__(self):
        super().__init__()

    def select(self):
        cursor = self.getCursor()
        usuarios = []
        try:
            cursor.execute(self.SQL_SELECT)
            rows = cursor.fetchall()
            for row in rows:
                usuarios.append(UsuarioVO(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
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
            cursor.execute(self.SQL_INSERT, (
                usuario.nombre_completo,
                usuario.nombre_usuario,
                usuario.correo,
                usuario.contrasena,
                usuario.puntos_experiencia,
                usuario.id_rol
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar usuario:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return rows

    def check_login(self, login: LoginVO):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CHECK_LOGIN, (login.usuario, login.contrasena))
            row = cursor.fetchone()
            if row:
                return UsuarioVO(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            return None
        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

    def chek_sign(self, usuario: UsuarioVO):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CHEK_SIGN, (usuario.nombre_usuario, usuario.correo))
            row = cursor.fetchone()
            return row if row else None
        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

    def obtener_perfil_por_id(self, id_usuario):
        cursor = self.getCursor()
        try:
            cursor.execute(
                "SELECT id_usuario, nombre_completo, nombre_usuario, correo, contrasena, puntos_experiencia, id_rol FROM Usuario WHERE id_usuario = ?",
                (id_usuario,)
            )
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
            cursor.execute(
                "SELECT SUM(win), SUM(loss) FROM Participantes WHERE id_usuario = ?",
                (id_usuario,)
            )
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
            cursor.execute(
                "SELECT id_usuario, nombre_completo, nombre_usuario, correo, contrasena, puntos_experiencia, id_rol FROM Usuario WHERE id_rol = ?",
                (id_rol,)
            )
            return [UsuarioVO(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in cursor.fetchall()]
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
            # Borrar cartas de los mazos del usuario
            cursor.execute("""
                DELETE FROM mazo_carta WHERE id_mazo IN (
                    SELECT id_mazo FROM mazos WHERE id_usuario = ?
                )
            """, (id_usuario,))
            # Borrar logs de moderación de sus mazos
            cursor.execute("""
                DELETE FROM modera_mazo WHERE id_mazo IN (
                    SELECT id_mazo FROM mazos WHERE id_usuario = ?
                )
            """, (id_usuario,))
            # Borrar participaciones en torneos
            cursor.execute("DELETE FROM participantes WHERE id_usuario = ?", (id_usuario,))
            # Borrar mazos
            cursor.execute("DELETE FROM mazos WHERE id_usuario = ?", (id_usuario,))
            # Borrar usuario
            cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
            return True
        except Exception as e:
            print(f"Error UsersDaoJBDC Eliminar: {e}")
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
            cursor.execute(
                "UPDATE Usuario SET puntos_experiencia = ?, id_rol = ? WHERE id_usuario = ?",
                (nueva_xp, nuevo_rol, id_usuario)
            )
            cursor.execute(
                "UPDATE Participantes SET win = ?, loss = ? WHERE id_usuario = ?",
                (nuevas_victorias, nuevas_derrotas, id_usuario)
            )
            return True
        except Exception as e:
            print(f"Error UsersDaoJBDC actualizar progreso: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()

    def cambiar_rol_usuario(self, id_usuario, nuevo_rol):
        cursor = self.getCursor()
        if not cursor:
            return False
        try:
            cursor.execute(
                "UPDATE Usuario SET id_rol = ? WHERE id_usuario = ?",
                (nuevo_rol, id_usuario)
            )
            return True
        except Exception as e:
            print(f"Error UsersDaoJBDC cambiar rol: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()