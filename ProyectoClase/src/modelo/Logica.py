
from modelo.dao.UsuarioDAO import UsuarioDAO

class Logica:
    def __init__(self):
        self.usuario_dao = UsuarioDAO()

    def validar_registro(self, usuario_vo):

        if not usuario_vo.nombre or not usuario_vo.correo:
            return "Error: Campos vacíos"
        
        resultado = self.usuario_dao.registrar_usuario(usuario_vo)
        if resultado:
            return "Registro exitoso"
        else:
            return "Error en la base de datos"