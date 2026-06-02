import jaydebeapi
import traceback

class Conexion:
    def __init__(self, host='127.0.0.1', database='Paladex', user='root', password='TuPasswordFuerte123!'):
        self._host = host
        self._database = database
        self._user = user
        self._password = password
        self.conexion = None
        self.createConnection()

    def createConnection(self):
        try:
            jdbc_driver = "com.mysql.cj.jdbc.Driver"
            jar_file = "lib/mysql-connector-j-9.7.0.jar"
            
            url = f"jdbc:mysql://{self._host}:3306/{self._database}?useSSL=false&allowPublicKeyRetrieval=true"
            
            self.conexion = jaydebeapi.connect(
                jdbc_driver,
                url,
                [self._user, self._password],
                jar_file
            )
            self.conexion.jconn.setAutoCommit(False)

            return self.conexion
            
        except Exception as e:
            print("--- ERROR DE CONEXIÓN JAYDEBEAPI ---")
            print(f"Mensaje: {e}")
            traceback.print_exc() 
            self.conexion = None
            return None

    def getCursor(self):
        """
        Verifica la conexión antes de entregar el cursor para evitar el AttributeError.
        """
        if self.conexion is None:
            self.createConnection()
        
        if self.conexion is not None:
            return self.conexion.cursor()
        else:
            raise ConnectionError("No se pudo establecer la conexión con la base de datos a través de JayDeBeApi.")

    def closeConnection(self):
        try:
            if self.conexion:
                self.conexion.close()
                self.conexion = None
                print("Conexión cerrada correctamente.")
        except Exception as e:
            print(f"Error cerrando conexión: {e}")