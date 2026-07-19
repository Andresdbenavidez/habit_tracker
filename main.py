import mysql.connector

from mysql.connector import Error

def conectar_base_datos():
    try:
        conexion = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "qwerty"
        )
        cursor = conexion.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS habit_tracker;")
        cursor.execute("USE habit_tracker;")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habitos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100),
                racha INT
            );            
        """)

        return conexion, cursor
    except Error as e:
        print(f"[ERROR DE INFRAESTRUCTURA]: No se pudo conectar a MySQL")
        print(f"Detalle técnico del error: {e}")

        return None, None
    

def crear_habito(conexion, cursor, nombre_habito):
    try:
        consulta = "INSERT INTO habitos (nombre, racha) VALUES (%s, %s)"
        datos = (nombre_habito, 0)

        cursor.execute(consulta, datos)
        conexion.commmit()
        print(f"[HÁBITO CREADO]: '{nombre_habito}' se ha registrado con éxito.")
    except Error as e:
        print(f"[ERROR AL CREAR HÁBITO]: No se pudo guardar en la base de datos.")
        print(f"Detalle: {e}")