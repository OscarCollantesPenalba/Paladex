from src.modelo.dao.UsersDaoJBDC import UsersDaoJBDC
from src.modelo.vo.UsuarioVo import UsuarioVO 

class Logica:
    def Select(self):
        user_dao = UsersDaoJBDC()
        users = user_dao.select()

        for usuario in users:  
            print(usuario)
            print(usuario.nombre_usuario)
        
    def Insert(self, usuarioVO):
        user_dao = UsersDaoJBDC()
        user_dao.insert(usuarioVO) 

    def HacerLogin(self, loginVO):
        login_dao = UsersDaoJBDC()
        resultado = login_dao.check_login(loginVO)

        return resultado

    def ComprobarSign(self,usuarioVO):
        user_dao = UsersDaoJBDC()
        resultado = user_dao.chek_sign(usuarioVO)

        return resultado
    
class LogicaHome:
    pass