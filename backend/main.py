# backend/main.py (VERSIÓN INICIAL CON DEUDA TÉCNICA)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2 # Conexión directa, sin ORM ni inyección de dependencias
import re
from datetime import datetime

app = FastAPI()

# Primitive Obsession: En lugar de usar un DTO bien tipado, recibimos strings sueltos
class SolicitudReq(BaseModel):
    t: str # tipo
    d: str # descripcion
    e_mail: str
    prio: int

# God Class / Long Method: Una sola función hace validación, base de datos, lógica y notificaciones
@app.post("/api/v1/solicitudes")
def procesar_solicitud_estudiante(req: SolicitudReq):
    # 1. Code Smell: Magic Numbers y validaciones repetidas (Duplicated Code)
    if req.prio < 1 or req.prio > 3:
        raise HTTPException(status_code=400, detail="Prioridad incorrecta")
    
    if len(req.d) < 10:
        raise HTTPException(status_code=400, detail="Falta descripcion")
        
    # 2. Code Smell: Lógica de validación mezclada con negocio
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(regex, req.e_mail):
        raise HTTPException(status_code=400, detail="Email invalido")

    # 3. Code Smell: Alto acoplamiento (Hardcoding credenciales y base de datos directo en el router)
    try:
        conn = psycopg2.connect(
            dbname="utn_db", user="postgres", password="password", host="localhost"
        )
        cursor = conn.cursor()
        
        # 4. Code Smell: Exposición a SQL Injection y falta de abstracción (Sin Repository Pattern)
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = f"INSERT INTO solicitudes (tipo, descripcion, email, prioridad, fecha, estado) VALUES ('{req.t}', '{req.d}', '{req.e_mail}', {req.prio}, '{fecha_actual}', 'PENDIENTE')"
        cursor.execute(query)
        conn.commit()
        
        # 5. Code Smell: Violación de SRP (Single Responsibility Principle) - El endpoint también manda "emails"
        print(f"SIMULACION: Enviando email a {req.e_mail} informando que la solicitud {req.t} fue recibida.")
        
        cursor.close()
        conn.close()
        
        return {"msg": "ok", "status": 200, "fecha": fecha_actual}
        
    except Exception as e:
        # 6. Code Smell: Mal manejo de errores, filtra detalles internos de la base de datos al usuario
        raise HTTPException(status_code=500, detail=str(e))