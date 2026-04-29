class UsuarioVO:
    
    def __init__(self, id_usuario=None, nombre=None, correo=None, contrasena=None,id_rol = None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.id_rol = id_rol