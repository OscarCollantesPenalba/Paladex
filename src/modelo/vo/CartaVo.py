class CartaVO:
    def __init__(self, id_carta, nombre, descripcion, categoria, id_campeon, nombre_campeon=None):
        self._id_carta = id_carta
        self._nombre = nombre
        self._descripcion = descripcion
        self._categoria = categoria
        self._id_campeon = id_campeon
        self._nombre_campeon = nombre_campeon  # JOIN con campeon

    @property
    def id_carta(self):
        return self._id_carta

    @property
    def nombre(self):
        return self._nombre

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def categoria(self):
        return self._categoria

    @property
    def id_campeon(self):
        return self._id_campeon

    @property
    def nombre_campeon(self):
        return self._nombre_campeon

    def __str__(self):
        return f"CartaVO(id={self._id_carta}, nombre={self._nombre}, categoria={self._categoria})"