from src.modelo.dao.UsersDaoJBDC import UsersDaoJBDC
from src.modelo.vo.UsuarioVo import UsuarioVO 
from src.modelo.dao.MazoDAO import MazoDAO
from src.modelo.dao.TorneoDAO import TorneoDAO
from src.modelo.conexion.Conexion import Conexion

class Logica:
    def __init__(self):
        pass

    def HacerLogin(self, login_vo):
        dao = UsersDaoJBDC()
        return dao.check_login(login_vo)

    def ComprobarSign(self, usuario_vo):
        dao = UsersDaoJBDC()
        return dao.chek_sign(usuario_vo)

    def Insert(self, usuario_vo):
        dao = UsersDaoJBDC()
        return dao.insert(usuario_vo)

    def obtener_campeones(self):
        conexion_obj = Conexion()
        conexion = conexion_obj.createConnection()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_campeon, nombre FROM Campeon")
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultados

    def obtener_cartas_por_campeon(self, id_campeon):
        dao = MazoDAO()
        return dao.obtener_cartas_por_campeon(id_campeon)

    def guardar_mazo_en_db(self, mazo_vo):
        dao = MazoDAO()
        return dao.guardar_mazo_completo(mazo_vo)

    def obtener_torneos(self):
        dao = TorneoDAO()
        return dao.obtener_todos_los_torneos()

    def inscribir_usuario_torneo(self, id_usuario, id_torneo, alias, equipo):
        dao = TorneoDAO()
        return dao.inscribir_participante(id_usuario, id_torneo, alias, equipo)

    def obtener_datos_perfil(self, id_usuario):
        dao = UsersDaoJBDC()
        return dao.obtener_perfil_por_id(id_usuario)

    def obtener_estadisticas_torneo(self, id_usuario):
        dao = UsersDaoJBDC()
        return dao.obtener_totales_participante(id_usuario)
    
    def obtener_mazos_usuario(self, id_usuario):
        dao = MazoDAO()
        return dao.obtener_mazos_por_usuario(id_usuario)

    def obtener_detalles_mazo(self, id_mazo):
        dao = MazoDAO()
        return dao.obtener_detalles_cartas_mazo(id_mazo)

    def eliminar_mazo_db(self, id_mazo):
        dao = MazoDAO()
        return dao.eliminar_mazo_por_id(id_mazo)
    
    def obtener_usuarios_por_rol(self, id_rol):
        return UsersDaoJBDC().obtener_usuarios_por_rol(id_rol)

    def eliminar_usuario_db(self, id_usuario):
        return UsersDaoJBDC().eliminar_usuario_por_id(id_usuario)

    def añadir_torneo_db(self, torneo_vo):
        return TorneoDAO().insertar_nuevo_torneo(torneo_vo)

    def eliminar_torneo_db(self, id_torneo):
        return TorneoDAO().eliminar_torneo_por_id(id_torneo)

    def obtener_participantes_torneo(self, id_torneo):
        return TorneoDAO().obtener_participantes_torneo(id_torneo)

    def eliminar_participante_torneo(self, id_usuario, id_torneo):
        return TorneoDAO().eliminar_participante_torneo(id_usuario, id_torneo)

    def obtener_todos_los_mazos_global(self):
        return MazoDAO().obtener_todos_los_mazos()

    def obtener_datos_perfil_vo(self, id_usuario):
        from src.modelo.dao.UsersDaoJBDC import UsersDaoJBDC
        dao = UsersDaoJBDC()
        return dao.obtener_perfil_por_id(id_usuario)

    def obtener_estadisticas_torneo(self, id_usuario):
        from src.modelo.dao.UsersDaoJBDC import UsersDaoJBDC
        dao = UsersDaoJBDC()
        return dao.obtener_totales_participante(id_usuario)

    def registrar_resultado_combate(self, id_usuario, es_victoria):
        try:
            from src.modelo.dao.UsersDaoJBDC import UsersDaoJBDC
            dao = UsersDaoJBDC()
            
            usuario_vo = dao.obtener_perfil_por_id(id_usuario)
            stats_torneo = dao.obtener_totales_participante(id_usuario)
            
            if not usuario_vo:
                return False
                
            victorias = stats_torneo[0]
            derrotas = stats_torneo[1]
            
            if es_victoria:
                victorias += 1
                usuario_vo.puntos_experiencia += 25
            else:
                derrotas += 1
                usuario_vo.puntos_experiencia = max(0, usuario_vo.puntos_experiencia - 10)
                
            if usuario_vo.id_rol == 3 and usuario_vo.puntos_experiencia >= 100:
                usuario_vo.id_rol = 4
            elif usuario_vo.id_rol == 4 and usuario_vo.puntos_experiencia < 100:
                usuario_vo.id_rol = 3
                
            return dao.actualizar_progreso_usuario(
                id_usuario, 
                victorias, 
                derrotas, 
                usuario_vo.puntos_experiencia, 
                usuario_vo.id_rol
            )
        except Exception as e:
            print(f"Error en Logica al procesar combate: {e}")
            return False