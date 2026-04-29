
class Coordinador:
    def __init__(self):
        self.__mi_logica = None
        self.__ventana_registro = None

    # Métodos set/get para enlazar las capas...
    def set_logica(self, logica): self.__mi_logica = logica
    
    def registrar_usuario(self, usuario_vo):
        return self.__mi_logica.validar_registro(usuario_vo)