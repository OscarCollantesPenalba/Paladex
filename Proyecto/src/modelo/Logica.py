from src.modelo.dao.UsersDaoJBDC import UsersDaoJBDC
from src.modelo.vo.UsuarioVo import UsuarioVO 
from src.modelo.dao.MazoDAO import MazoDAO
from src.modelo.conexion.Conexion import Conexion

class Logica:
    def __init__(self):
        self.conexion_obj = Conexion() 
        self.conexion = self.conexion_obj.createConnection()

    def obtener_cartas_por_campeon(self, id_campeon):
        try:
            from src.modelo.dao.MazoDAO import MazoDAO
            dao = MazoDAO()
            return dao.obtener_cartas_por_campeon(id_campeon)
        except Exception as e:
            print(f"Error al obtener cartas: {e}")
            return []

    def guardar_mazo_en_db(self, mazo_vo):
        try:
            from src.modelo.dao.MazoDAO import MazoDAO
            dao = MazoDAO()
            return dao.guardar_mazo_completo(mazo_vo)
        except Exception as e:
            print(f"Error en Logica: {e}")
            return False
    
    def obtener_campeones(self):
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT id_campeon, nombre FROM Campeon")
            resultados = cursor.fetchall()
            cursor.close()
            return resultados
        except Exception as e:
            print(f"Error en Logica.obtener_campeones: {e}")
            return []


    def cargar_combo_campeones(self):
        campeones = self.__modelo.obtener_campeones()
        self.__nueva_vista.cbCampeon.clear()
        for fila in campeones:
            self.__nueva_vista.cbCampeon.addItem(str(fila[1]), fila[0])
    
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
    
    def obtener_torneos(self):
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT id_torneo, nombre, ubicacion, descripcion, reglas FROM Torneos")
            resultados = cursor.fetchall()
            cursor.close()
            return resultados
        except Exception as e:
            print(f"Error al obtener torneos: {e}")
            return []

    def inscribir_usuario_torneo(self, id_usuario, id_torneo, alias, equipo):
        try:
            cursor = self.conexion.cursor()
            sql = """
                INSERT INTO Participantes (id_usuario, id_torneo, alias, equipo, win, loss) 
                VALUES (%s, %s, %s, %s, 0, 0)
            """
            cursor.execute(sql, (id_usuario, id_torneo, alias, equipo))
            self.conexion.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error en la inscripción: {e}")
            return False
        
    def obtener_datos_perfil(self, id_usuario):
        try:
            cursor = self.conexion.cursor()
            sql = "SELECT nombre_usuario, puntos_experiencia FROM Usuario WHERE id_usuario = %s"
            cursor.execute(sql, (id_usuario,))
            resultado = cursor.fetchone()
            cursor.close()
            return resultado
        except Exception as e:
            print(f"Error al obtener perfil: {e}")
            return None

    def obtener_estadisticas_torneo(self, id_usuario):
        try:
            cursor = self.conexion.cursor()
            sql = "SELECT SUM(win), SUM(loss) FROM Participantes WHERE id_usuario = %s"
            cursor.execute(sql, (id_usuario,))
            resultado = cursor.fetchone()
            cursor.close()
            return resultado
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return (0, 0)