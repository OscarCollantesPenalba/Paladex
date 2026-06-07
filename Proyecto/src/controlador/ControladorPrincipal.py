from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.UsuarioVo import UsuarioVO
from src.vista.VistaHome import VistaHome
from src.vista.VistaModerador import VistaModerador
from src.vista.VistaAdmin import VistaAdmin
from src.controlador.ControladorHome import ControladorHome
from src.controlador.ControladorModerador import ControladorModerador
from src.controlador.ControladorAdmin import ControladorAdmin


class ControladorPrincipal:
    """
    Controlador raíz de la aplicación.
    Gestiona el login, el registro y redirige al panel correspondiente
    según el rol del usuario autenticado.
    """

    def __init__(self, ref_vista, ref_modelo):
        self.__vista   = ref_vista
        self.__modelo  = ref_modelo
        self.usuario_actual    = None
        self.usuario_actual_id = None

    # ------------------------------------------------------------------ #
    # Login / Registro                                                     #
    # ------------------------------------------------------------------ #

    def abrirIniciarSesion(self):
        self.__vista.show()

    def comprobarLogin(self, usuario, contrasena):
        """Valida credenciales y redirige según el rol del usuario."""
        if not usuario or not contrasena:
            self.__vista.login_vacio()
            return

        loginVO  = LoginVO(usuario, contrasena)
        resultado = self.__modelo.HacerLogin(loginVO)

        if resultado is None:
            self.__vista.login_incorrecto()
            return

        self.usuario_actual    = resultado
        self.usuario_actual_id = resultado.id_usuario
        id_rol = getattr(resultado, 'id_rol', 3)
        self.__vista.close()

        if id_rol == 0:
            self.mostrar_menu_admin()
        elif id_rol == 1:
            self.mostrar_menu_moderador()
        else:
            self.__abrirHome(resultado)

    def comprobarRegistro(self, nombre_completo, nombre_usuario, correo,
                          contrasena, confirm_contrasena,
                          puntos_experiencia=0, id_rol=3):
        """Valida los datos del formulario de registro antes de insertar."""
        if not nombre_completo or not nombre_usuario or not correo \
                or not contrasena or not confirm_contrasena:
            self.__vista.sign_vacio()
            return

        if "@" not in correo or "." not in correo:
            self.__vista.email_correcto()
            return

        if contrasena != confirm_contrasena:
            self.__vista.contrasenas_diferentes()
            return

        if len(contrasena) < 8:
            self.__vista.contrasena_pequena()
            return

        usuarioVO = UsuarioVO(None, nombre_completo, nombre_usuario,
                              correo, contrasena, puntos_experiencia, id_rol)
        resultado = self.__modelo.ComprobarSign(usuarioVO)

        if resultado:
            self.__vista.usuario_email_existentes()
        else:
            self.__modelo.Insert(usuarioVO)
            self.__vista.volver_login()

    # ------------------------------------------------------------------ #
    # Home (usuarios con rol 2 y 3)                                        #
    # ------------------------------------------------------------------ #

    def __abrirHome(self, usuario):
        """Abre la ventana principal y conecta el sidebar al ControladorHome."""
        self.__vista_home = VistaHome()
        self.__ctrl_home  = ControladorHome(self.__vista_home, usuario)
        self.__vista_home.controlador = self.__ctrl_home

        # Botones del sidebar → ControladorHome
        if hasattr(self.__vista_home, 'btnPerfil'):
            self.__vista_home.btnPerfil.clicked.connect(self.__ctrl_home.abrirPerfil)
        if hasattr(self.__vista_home, 'btnMazos'):
            self.__vista_home.btnMazos.clicked.connect(self.__ctrl_home.abrirCreadorMazos)
        if hasattr(self.__vista_home, 'btnMisMazos'):
            self.__vista_home.btnMisMazos.clicked.connect(self.__ctrl_home.abrirMisMazos)
        if hasattr(self.__vista_home, 'btnTorneos'):
            self.__vista_home.btnTorneos.clicked.connect(self.__ctrl_home.abrirTorneos)
        if hasattr(self.__vista_home, 'btnCerrarSesion'):
            self.__vista_home.btnCerrarSesion.clicked.connect(self.__cerrarSesionHome)

        # Cerrar ventanas hijas si el usuario cierra la Home con la X
        self.__vista_home.closeEvent = lambda event: self.__on_home_cerrada(event)

        self.__vista_home.show()
        self.__ctrl_home.inicializar()

    def __on_home_cerrada(self, event):
        """Cierra todas las ventanas hijas al cerrar la Home."""
        self.__ctrl_home.cerrar_todo()
        event.accept()

    def __cerrarSesionHome(self):
        """Cierra sesión desde el botón del sidebar."""
        self.__ctrl_home.cerrar_todo()
        self.__vista_home.close()
        self.usuario_actual    = None
        self.usuario_actual_id = None
        self.abrirIniciarSesion()

    # ------------------------------------------------------------------ #
    # Panel Moderador (rol 1)                                              #
    # ------------------------------------------------------------------ #

    def mostrar_menu_moderador(self):
        self.__vista_mod = VistaModerador()
        self.__ctrl_mod  = ControladorModerador(self.__vista_mod, self.usuario_actual, self)
        self.__vista_mod.controlador = self.__ctrl_mod
        self.__vista_mod.show()
        self.__ctrl_mod.inicializar()

    # ------------------------------------------------------------------ #
    # Panel Admin (rol 0)                                                  #
    # ------------------------------------------------------------------ #

    def mostrar_menu_admin(self):
        self.__vista_admin = VistaAdmin()
        self.__ctrl_admin  = ControladorAdmin(self.__vista_admin, self.usuario_actual, self)
        self.__vista_admin.controlador = self.__ctrl_admin
        self.__vista_admin.show()
        self.__ctrl_admin.inicializar()