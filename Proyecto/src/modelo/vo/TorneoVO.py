class TorneoVO:
    def __init__(self, id_torneo=None, nombre=None, ubicacion=None, descripcion=None, reglas=None):
        self.id_torneo = id_torneo
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.descripcion = descripcion
        self.reglas = reglas