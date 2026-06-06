class TorneoVO:
    def __init__(self, id_torneo, nombre, ubicacion, descripcion, reglas):
        self._id_torneo = id_torneo
        self._nombre = nombre
        self._ubicacion = ubicacion
        self._descripcion = descripcion
        self._reglas = reglas

    @property
    def id_torneo(self):
        return self._id_torneo

    @property
    def nombre(self):
        return self._nombre

    @property
    def ubicacion(self):
        return self._ubicacion

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def reglas(self):
        return self._reglas

    def __str__(self):
        return f"TorneoVO(id={self._id_torneo}, nombre={self._nombre}, ubicacion={self._ubicacion})"