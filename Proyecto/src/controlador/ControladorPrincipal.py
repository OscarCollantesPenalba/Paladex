from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.UsuarioVo import UsuarioVO
from src.vista.VistaMazo import VistaMazo
from src.modelo.vo.MazoVO import MazoVO

class ControladorPrincipal:
    def __init__(self, ref_vista, ref_modelo):
        self.__vista = ref_vista
        self.__modelo = ref_modelo
        
        if hasattr(self.__vista, 'btnIrAMazos'):
            self.__vista.btnIrAMazos.clicked.connect(self.abrirCreadorMazos)

    def cargar_datos_iniciales(self):
    
        campeones = self.__modelo.obtener_campeones()

        self.__nueva_vista.cbCampeon.clear()

        for id_amp, nombre in campeones:
            self.__nueva_vista.cbCampeon.addItem(nombre, id_amp)

    def abrirIniciarSesion(self):
        self.__vista.show()

    
    def abrirIniciarSesion(self):
        self.__vista.show()

    def comprobarLogin(self, usuario, contrasena):
        
        loginVO = LoginVO(usuario, contrasena)
        resultado = self.__modelo.HacerLogin(loginVO)

        if resultado:
            self.usuario_actual = resultado
            self.__vista.close()
            self.abrirCreadorMazos()
        else:
            self.__vista.login_incorrecto()

    def abrirCreadorMazos(self):
        self.__nueva_vista = VistaMazo()
        self.cargar_datos_iniciales()

        self.__nueva_vista.btnGuardarMazo.clicked.connect(self.guardarMazoDesdeInterfaz)

        self.__nueva_vista.cbCampeon.currentIndexChanged.connect(self.actualizar_cartas_interfaz)

        self.__nueva_vista.show()

    def guardarMazoDesdeInterfaz(self):
        nombre = self.__nueva_vista.txtNombreMazo.text()
        id_campeon = self.__nueva_vista.cbCampeon.currentData()

        id_usuario = getattr(self, 'usuario_actual_id', 1) 

        if not nombre:
            print("El mazo debe tener un nombre")
            return

        lista_cartas = [
            (self.__nueva_vista.cbCarta1.currentData(), self.__nueva_vista.spinNivel1.value()),
            (self.__nueva_vista.cbCarta2.currentData(), self.__nueva_vista.spinNivel2.value()),
            (self.__nueva_vista.cbCarta3.currentData(), self.__nueva_vista.spinNivel3.value()),
            (self.__nueva_vista.cbCarta4.currentData(), self.__nueva_vista.spinNivel4.value()),
            (self.__nueva_vista.cbCarta5.currentData(), self.__nueva_vista.spinNivel5.value())
        ]

        nuevo_mazo = MazoVO(None, nombre, id_usuario, id_campeon, lista_cartas)

        exito = self.__modelo.guardar_mazo_en_db(nuevo_mazo)

        if exito:
            print("¡Mazo guardado con éxito!")
        else:
            print("Error al guardar el mazo en la base de datos")

    def actualizar_cartas_interfaz(self):
        id_c = self.__nueva_vista.cbCampeon.currentData()
        cartas = self.__modelo.obtener_cartas_por_campeon(id_c)

        combos = [self.__nueva_vista.cbCarta1, self.__nueva_vista.cbCarta2, 
                  self.__nueva_vista.cbCarta3, self.__nueva_vista.cbCarta4, 
                  self.__nueva_vista.cbCarta5]

        for cb in combos:
            cb.clear()
            for id_car, nombre, desc, cat in cartas:
                cb.addItem(nombre, id_car)

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
