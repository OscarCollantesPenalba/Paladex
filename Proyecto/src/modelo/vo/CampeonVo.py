class CampeonVO:
    def __init__(self, id_campeon, nombre, titulo, salud, daño, velocidad, id_clase, nombre_clase=None):
        self._id_campeon = id_campeon
        self._nombre = nombre
        self._titulo = titulo
        self._salud = salud
        self._daño = daño
        self._velocidad = velocidad
        self._id_clase = id_clase
        self._nombre_clase = nombre_clase  
        self._habilidades = []  

    @property
    def id_campeon(self):
        return self._id_campeon

    @property
    def nombre(self):
        return self._nombre

    @property
    def titulo(self):
        return self._titulo

    @property
    def salud(self):
        return self._salud

    @property
    def daño(self):
        return self._daño

    @property
    def velocidad(self):
        return self._velocidad

    @property
    def id_clase(self):
        return self._id_clase

    @property
    def nombre_clase(self):
        return self._nombre_clase

    @property
    def habilidades(self):
        return self._habilidades

    @habilidades.setter
    def habilidades(self, lista):
        self._habilidades = lista

    def __str__(self):
        return f"CampeonVO(id={self._id_campeon}, nombre={self._nombre}, clase={self._nombre_clase})"