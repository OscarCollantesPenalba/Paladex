
from modelo.dao.UsuarioDAO import UsuarioDAO
from modelo.vo.UsuarioVO import UsuarioVO
from modelo.dao.RolDAO import RolDAO


#nuevo_usuario = UsuarioVO(None, "AndroxusPlayer", "gay@ule.com", "1234")
#dao = UsuarioDAO()
#
#if dao.registrar_usuario(nuevo_usuario):
#    print("¡Usuario registrado con éxito!")
#else:
#    print("Error al registrar")


dao_rol = RolDAO()
dao_rol.insertar_roles_iniciales()

nuevo_usuario = UsuarioVO(10, "Grefurius", "grefu@gmail.com", "password", 2)
dao_usuario = UsuarioDAO()

if dao_usuario.registrar_usuario(nuevo_usuario):
    print("¡Usuario registrado con éxito!")
else:
    print("Error al registrar")