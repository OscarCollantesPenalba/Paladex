from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.UsuarioVo import UsuarioVO

class ControladorPrincipal:
    def __init__(self, ref_vista, ref_modelo):
        self.__vista = ref_vista
        self.__modelo = ref_modelo

    def abrirIniciarSesion(self):
        self.__vista.show()

    def comprobarLogin(self, usuario, contrasena):
        
        loginVO = LoginVO(usuario,contrasena)
        
        resultado = self.__modelo.HacerLogin(loginVO)

        if not usuario or not contrasena:
            self.__vista.login_vacio()
        
        elif resultado == None:
            self.__vista.login_incorrecto()
        
        else:
            self.__vista.close()
            #self.__vista = ""#objeto vista del menu(aplicación dentro)


    def comprobarRegistro(self,nombre_completo,nombre_usuario, correo, contrasena,confirm_contrasena, puntos_experiencia = 0, id_rol=3):
        
        if not nombre_completo or not nombre_usuario or not correo or not contrasena or not confirm_contrasena:
            self.__vista.sign_vacio()

        if "@" not in correo or "." not in correo:
            self.__vista.email_correcto()

        if contrasena != confirm_contrasena:
            self.__vista.contrasenas_diferentes()
        
        if len(contrasena) < 8:
            self.__vista.contrasena_pequena()
        
        usuarioVO =UsuarioVO(None,
                           nombre_completo,
                           nombre_usuario,
                           correo, 
                           contrasena, 
                           puntos_experiencia, 
                           id_rol)
        
        resultado = self.__modelo.ComprobarSign(usuarioVO)

        if resultado:
            self.__vista.usuario_email_existentes()
        else:
            
            self.__modelo.Insert(usuarioVO)
            
            self.__vista.close()
            #self.__vista= "" #objeto vista del menu(aplicación dentro)