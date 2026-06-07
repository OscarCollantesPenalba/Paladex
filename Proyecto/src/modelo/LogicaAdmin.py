from src.modelo.dao.UsersDaoJBDC import UsersDaoJBDC
from src.modelo.dao.ModeradoDaoJBDC import ModeraDAO
from src.modelo.dao.AdminDaoJBDC import AdminDaoJBDC


class LogicaAdmin:

    def obtener_usuarios_por_rol(self, id_rol):
        return UsersDaoJBDC().obtener_usuarios_por_rol(id_rol)

    def eliminar_usuario(self, id_usuario):
        return UsersDaoJBDC().eliminar_usuario_por_id(id_usuario)

    def cambiar_rol(self, id_usuario, nuevo_rol):
        return UsersDaoJBDC().cambiar_rol_usuario(id_usuario, nuevo_rol)

    def obtener_logs_moderacion(self):
        return ModeraDAO().obtener_todos_los_logs()

    def hacer_backup(self, ruta_destino):
        return AdminDaoJBDC().hacer_backup(ruta_destino)