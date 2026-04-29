import mysql.connector

class Conexion:
    def __init__(self):
        self.conexion = None
        self.conectar()

    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="TuPasswordFuerte123!",
                database="Paladex"
            )
            print("¡Conectado exitosamente a MySQL en Docker!")
        except Exception as e:
            print(f"Error de conexión: {e}")
            self.conexion = None

    def getCursor(self):
        if self.conexion:
            return self.conexion.cursor()
        print("No hay conexión establecida.")
        return None
        
    def closeConnection(self):
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print("Conexión cerrada.")