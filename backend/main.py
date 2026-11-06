from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from backend.database import get_session, init_db
from backend.models import Solicitud
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="UTN - Sistema de Gestión de Solicitudes Académicas", version="2.0.0")

@app.on_event("startup")
def on_startup():
    init_db()

# DTOs de entrada (Validación estricta con Pydantic)
class SolicitudCreate(BaseModel):
    tipo: str = Field(..., min_length=3)
    descripcion: str = Field(..., min_length=10)
    email_estudiante: EmailStr
    prioridad: int = Field(..., ge=1, le=3)

class SolicitudUpdateEstado(BaseModel.Config):
    estado: str
    responsable: str

@app.post("/api/v1/solicitudes", response_model=Solicitud, status_code=status.HTTP_201_CREATED)
def crear_solicitud(payload: SolicitudCreate, session: Session = Depends(get_session)):
    try:
        nueva_solicitud = Solicitud(
            tipo=payload.tipo,
            descripcion=payload.descripcion,
            email_estudiante=payload.email_estudiante,
            prioridad=payload.prioridad
        )
        session.add(nueva_solicitud)
        session.commit()
        session.refresh(nueva_solicitud)
        
        # Simulación de notificación desacoplada
        print(f"[LOG NOTIFICACIÓN] Enviando correo a {nueva_solicitud.email_estudiante}: Solicitud registrada con éxito.")
        return nueva_solicitud
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error interno al procesar la solicitud en base de datos.")

@app.get("/api/v1/solicitudes", response_model=List[Solicitud])
def listar_solicitudes(session: Session = Depends(get_session)):
    solicitudes = session.exec(select(Solicitud)).all()
    return solicitudes