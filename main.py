import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/habit_tracker_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class HabitoModel(Base):
    __tablename__ = "habitos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    racha = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Habit Tracker API",
    description="Backend modular en Python para conectar una base de datos MySQL con una app de Android",
    version="1.0.0"
)

class HabitoEsquema(BaseModel):
    nombre: str

def conectar_base_datos():
    try:
        conexion = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "root"
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


@app.get("/habitos")
def api_listar_habitos():
    conexion, cursor = conectar_base_datos()

    if not conexion or not cursor:
        raise HTTPException(status_code=500, detail="Error interno de infraestructura al conectar a la base de datos.")
    
    try:
        consulta = "SELECT id, nombre, racha FROM habitos;"
        cursor.execute(consulta)
        resultados = cursor.fetchall()

        lista_habitos = []
        for fila in resultados:
            lista_habitos.append({
                "id": fila[0],
                "nombre": fila[1],
                "racha": fila[2]
            })

        return lista_habitos
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error en la consulta {e}")
    finally:
        cursor.close()
        conexion.close()

@app.post("/habitos")
def api_crear_habito(habito: HabitoEsquema):
    conexion, cursor = conectar_base_datos()

    if not conexion or not cursor:
        raise HTTPException(status_code=500, detail="Error de conexión con la base de datos.")

    try:
        nombre_nuevo = habito.nombre

        consulta = "INSERT INTO habitos (nombre, racha) VALUES (%s, 0);"
        cursor.execute(consulta, (nombre_nuevo,))
        conexion.commit()

        return {"status": "éxito", "mensaje": f"Hábito '{nombre_nuevo}' registrado correctamente."}
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"No se pudo guardar el hábito: {e}")
    
    finally:
        cursor.close()
        conexion.close()

@app.patch("/habitos/{id_habito}/completar")
def api_completar_habitos(id_habito: int):
    conexion, cursor = conectar_base_datos()

    if not conexion or not cursor:
        raise HTTPException(status_code=500, detail="Error de conexión con la base de datos.")    

    try:
        consulta = "UPDATE habitos SET racha = racha + 1 WHERE id = %s;"

        cursor.execute(consulta, (id_habito,))
        conexion.commit()

        if cursor.rowcount > 0:
            return {"status": "éxito", "mensaje": "La racha ha aumentado!"}
        else:
            raise HTTPException(status_code=404, detail=f"No se pudo actualizar la racha.")        
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la racha: {e}")
    finally:
        cursor.close()
        conexion.close()

@app.patch("/habitos/{id_habito}/reiniciar_racha")
def api_reiniciar_racha(id_habito: int):
    conexion, cursor = conectar_base_datos()

    if not conexion or not cursor:
        raise HTTPException(status_code=500, detail="Error de conexión con la base de datos.")
    
    try:
        consulta = "UPDATE habitos SET racha=0 WHERE id = %s;"

        cursor.execute(consulta, (id_habito,))
        conexion.commit()

        if cursor.rowcount > 0:
            return {"status": "éxito", "mensaje": "La racha se ha reiniciado correctamente."}
        else:
            raise HTTPException(status_code=404, detail=f"No se pudo actualizar la racha.")
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error al reiniciar la racha: {e}")
    finally:
        cursor.close()
        conexion.close()