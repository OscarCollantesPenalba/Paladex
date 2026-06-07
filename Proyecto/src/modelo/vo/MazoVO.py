class MazoVO:
    def __init__(self, id_mazo=None, nombre_mazo=None, id_usuario=None, id_campeon=None, lista_cartas=None):
        self.id_mazo = id_mazo
        self.nombre_mazo = nombre_mazo
        self.id_usuario = id_usuario
        self.id_campeon = id_campeon
        self.lista_cartas = lista_cartas if lista_cartas else []