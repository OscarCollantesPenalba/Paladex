class LoginVO:
    def __init__(self, usuario, contrasena):
        self._usuario = usuario
        self._contrasena = contrasena

    @property
    def contrasena(self):
        return self._contrasena

    @contrasena.setter
    def contrasena(self, value):
        self._contrasena = value

    @property
    def usuario(self):
        return self._usuario