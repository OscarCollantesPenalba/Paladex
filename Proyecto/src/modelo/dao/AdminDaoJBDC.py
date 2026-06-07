from src.modelo.conexion.Conexion import Conexion
from datetime import datetime


class AdminDaoJBDC(Conexion):
    """DAO exclusivo del administrador. Operaciones que solo el admin puede realizar."""

    def __init__(self):
        super().__init__()

    def hacer_backup(self, ruta_destino):
        """
        Exporta todas las tablas de la BD a un fichero .sql.
        Devuelve (True, ruta) si tiene éxito o (False, mensaje_error) si falla.
        """
        cursor = self.getCursor()
        if not cursor:
            return False, "No se pudo conectar a la base de datos."
        try:
            tablas = [
                "rol", "clase_campeon", "usuario", "campeon",
                "habilidades", "cartas", "mazos", "mazo_carta",
                "torneos", "participantes", "modera_mazo", "secciones"
            ]

            lineas = []
            lineas.append("-- Backup Paladex")
            lineas.append(f"-- Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            lineas.append("")
            lineas.append("SET FOREIGN_KEY_CHECKS = 0;")
            lineas.append("")

            for tabla in tablas:
                try:
                    # Obtener columnas
                    cursor.execute(f"DESCRIBE {tabla}")
                    columnas = [col[0] for col in cursor.fetchall()]

                    # Obtener datos
                    cursor.execute(f"SELECT * FROM {tabla}")
                    filas = cursor.fetchall()

                    lineas.append(f"-- Tabla: {tabla}")
                    lineas.append(f"DELETE FROM `{tabla}`;")

                    if filas:
                        cols = ", ".join(f"`{c}`" for c in columnas)
                        for fila in filas:
                            valores = []
                            for v in fila:
                                if v is None:
                                    valores.append("NULL")
                                elif isinstance(v, str):
                                    v_escaped = v.replace("'", "''")
                                    valores.append(f"'{v_escaped}'")
                                else:
                                    valores.append(str(v))
                            vals = ", ".join(valores)
                            lineas.append(f"INSERT INTO `{tabla}` ({cols}) VALUES ({vals});")

                    lineas.append("")
                except Exception as e:
                    lineas.append(f"-- Error en tabla {tabla}: {e}")
                    lineas.append("")

            lineas.append("SET FOREIGN_KEY_CHECKS = 1;")

            with open(ruta_destino, 'w', encoding='utf-8') as f:
                f.write("\n".join(lineas))

            return True, ruta_destino

        except Exception as e:
            return False, str(e)
        finally:
            self.closeConnection()