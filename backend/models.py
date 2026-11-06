from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Solicitud(SQLModel, table=True):
    __tablename__ = "solicitudes"

    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str = Field(index=True)
    descripcion: str
    email_estudiante: str = Field(index=True)
    responsable_asignado: Optional[str] = Field(default=None)
    prioridad: int = Field(ge=1, le=3)
    estado: str = Field(default="PENDIENTE")
    fecha_creacion: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))