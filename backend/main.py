# backend/main.py (VERSIÓN REFACTORIZADA - CLEAN CODE Y SOLID)
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="UTN Gestor de Solicitudes Académicas", version="2.0.0")

# --- 1. DTOs (Data Transfer Objects) con validación robusta (Adiós a Primitive Obsession) ---
class SolicitudCreate(BaseModel):
    tipo: str = Field(..., min_length=3, description="Tipo de solicitud académica")
    descripcion: str = Field(..., min_length=10, description="Detalle ampliado de la solicitud")
    email: EmailStr = Field(..., description="Correo electrónico institucional válido")
    prioridad: int = Field(..., ge=1, le=3, description="Prioridad de 1 a 3")

class SolicitudResponse(SolicitudCreate):
    id: int
    estado: str
    fecha: str

# --- 2. Capa de Repositorio (Principio de Responsabilidad Única - SRP) ---
class SolicitudRepository:
    def __init__(self):
        # Simulación de persistencia segura (en un entorno real conecta a PostgreSQL con SQLModel)
        self._storage = []
        self._counter = 1

    def save(self, data: SolicitudCreate) -> dict:
        nueva_solicitud = {
            "id": self._counter,
            "tipo": data.tipo,
            "descripcion": data.descripcion,
            "email": data.email,
            "prioridad": data.prioridad,
            "estado": "PENDIENTE",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self._storage.append(nueva_solicitud)
        self._counter += 1
        return nueva_solicitud

    def get_all(self) -> List[dict]:
        return self._storage

# --- 3. Capa de Servicios (Lógica de Negocio aislada) ---
class NotificacionService:
    @staticmethod
    def enviar_notificacion(email: str, tipo: str):
        # Abstracción limpia del servicio de correo (Evita acoplar un print en el controlador)
        print(f"[LOG NOTIFICACIÓN] Enviando correo electrónico a {email}: Su solicitud de tipo '{tipo}' fue registrada con éxito.")

class SolicitudService:
    def __init__(self, repository: SolicitudRepository = Depends()):
        self.repository = repository

    def procesar_nueva_solicitud(self, data: SolicitudCreate) -> dict:
        # Lógica de negocio encapsulada y validada por Pydantic
        solicitud_creada = self.repository.save(data)
        
        # Disparar notificación de forma desacoplada
        NotificacionService.enviar_notificacion(solicitud_creada["email"], solicitud_creada["tipo"])
        
        return solicitud_creada

# --- 4. Capa de Enrutamiento / Controladores (Limpios y desacoplados) ---
@app.post("/api/v1/solicitudes", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_solicitud(payload: SolicitudCreate, service: SolicitudService = Depends()):
    try:
        resultado = service.procesar_nueva_solicitud(payload)
        return {"status": "success", "data": resultado}
    except Exception as e:
        # Manejo de errores profesional (Sin filtrar trazas internas del sistema)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno al procesar la solicitud académica."
        )

@app.get("/api/v1/solicitudes", response_model=List[dict])
def listar_solicitudes(service: SolicitudService = Depends()):
    return service.repository.get_all()