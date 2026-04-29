# pip install mysql-connector-python
"""
Este archivo define la clase ConexionMYSQL, encargada de gestionar la conexión
con una base de datos MySQL para la aplicación.

La clase almacena como atributos estáticos los datos necesarios para conectarse
al servidor, como el host, el nombre de la base de datos, el usuario y la contraseña.

Además, incluye dos métodos estáticos:
- getConnection(): abre y devuelve una conexión a la base de datos.
- close(conn): cierra una conexión existente de forma segura.

Su objetivo es centralizar la lógica de conexión y cierre, facilitando el acceso
a la base de datos desde otras partes del programa.
"""
# Como parte del acceso anticipado al recurso desbloqueado, te adelanto que la próxima semana el aprendizaje activo será INDIVIDUAL y de repaso de todos los conceptos de cara al exámen

import mysql.connector


class ConexionMYSQL:

    # Especifica los detalles de la conexión
    host = 'localhost'
    database = 'mysql'
    user = 'sa'
    password = 'TuPaasswordFuerte123!'

    "Abre una conexión a la base de datos."
    @staticmethod
    def getConnection():
        try:
            return mysql.connector.connect(
                host= ConexionMYSQL.host,
                database= ConexionMYSQL.database,
                user= ConexionMYSQL.user,
                password= ConexionMYSQL.password,
            )
        except mysql.connector.Error as e:
            print(e)

    "Cierra una conexión a la base de datos."
    @staticmethod
    def close(conn):
        try:
            conn.close()
        except mysql.connector.Error as e:
            print(e)

