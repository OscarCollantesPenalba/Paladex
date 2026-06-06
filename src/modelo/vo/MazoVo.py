class MazoVO:
    def __init__(self, id_mazo, nombre_mazo, descripcion, estado, id_usuario, id_campeon, es_oficial,
                 nombre_campeon=None, nombre_usuario=None):
        self._id_mazo = id_mazo
        self._nombre_mazo = nombre_mazo
        self._descripcion = descripcion
        self._estado = estado
        self._id_usuario = id_usuario
        self._id_campeon = id_campeon
        self._es_oficial = es_oficial
        self._nombre_campeon = nombre_campeon  # JOIN con campeon
        self._nombre_usuario = nombre_usuario  # JOIN con usuario
        self._cartas = []                      # Lista de CartaVO (se carga aparte)

    @property
    def id_mazo(self):
        return self._id_mazo

    @property
    def nombre_mazo(self):
        return self._nombre_mazo

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def estado(self):
        return self._estado

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def id_campeon(self):
        return self._id_campeon

    @property
    def es_oficial(self):
        return bool(self._es_oficial)

    @property
    def nombre_campeon(self):
        return self._nombre_campeon

    @property
    def nombre_usuario(self):
        return self._nombre_usuario

    @property
    def cartas(self):
        return self._cartas

    @cartas.setter
    def cartas(self, lista):
        self._cartas = lista

    def __str__(self):
        return f"MazoVO(id={self._id_mazo}, nombre={self._nombre_mazo}, campeon={self._nombre_campeon})"