class HabilidadVO:
    def __init__(self, id_habilidad, nombre, tipo, descripcion, id_campeon):
        self._id_habilidad = id_habilidad
        self._nombre = nombre
        self._tipo = tipo
        self._descripcion = descripcion
        self._id_campeon = id_campeon

    @property
    def id_habilidad(self):
        return self._id_habilidad

    @property
    def nombre(self):
        return self._nombre

    @property
    def tipo(self):
        return self._tipo

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def id_campeon(self):
        return self._id_campeon

    def __str__(self):
        return f"HabilidadVO(nombre={self._nombre}, tipo={self._tipo})"