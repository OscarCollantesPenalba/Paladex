class UsuarioVO:
    def __init__(self, id_usuario, nombre_completo, nombre_usuario, correo, contrasena, puntos_experiencia=0, id_rol=3):
        self.__id_usuario = id_usuario
        self.__nombre_completo = nombre_completo
        self.__nombre_usuario = nombre_usuario
        self.__correo = correo
        self.__contrasena = contrasena
        self.__puntos_experiencia = puntos_experiencia
        self.__id_rol = id_rol

    @property
    def id_usuario(self): return self.__id_usuario

    @property
    def nombre_completo(self): return self.__nombre_completo

    @property
    def nombre_usuario(self): return self.__nombre_usuario

    @property
    def correo(self): return self.__correo

    @property
    def contrasena(self): return self.__contrasena

    @property
    def puntos_experiencia(self):
        return self.__puntos_experiencia

    @puntos_experiencia.setter
    def puntos_experiencia(self, valor):
        self.__puntos_experiencia = valor

    @property
    def id_rol(self):
        return self.__id_rol

    @id_rol.setter
    def id_rol(self, valor):
        self.__id_rol = valor