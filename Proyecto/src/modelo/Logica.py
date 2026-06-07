import hashlib
from src.modelo.dao.UsersDaoJBDC import UsersDaoJBDC
from src.modelo.vo.UsuarioVo import UsuarioVO


def cifrar_contrasena(contrasena):
    """Devuelve el hash SHA-256 de la contraseña en hexadecimal."""
    return hashlib.sha256(contrasena.encode('utf-8')).hexdigest()


class Logica:

    def Select(self):
        user_dao = UsersDaoJBDC()
        users = user_dao.select()
        for usuario in users:
            print(usuario.nombre_usuario)

    def Insert(self, usuarioVO):
        """Cifra la contraseña antes de guardarla en la BD."""
        usuarioVO.contrasena = cifrar_contrasena(usuarioVO.contrasena)
        user_dao = UsersDaoJBDC()
        user_dao.insert(usuarioVO)

    def HacerLogin(self, loginVO):
        """Cifra la contraseña introducida antes de compararla con la BD."""
        loginVO.contrasena = cifrar_contrasena(loginVO.contrasena)
        login_dao = UsersDaoJBDC()
        return login_dao.check_login(loginVO)

    def ComprobarSign(self, usuarioVO):
        user_dao = UsersDaoJBDC()
        return user_dao.chek_sign(usuarioVO)