from pydantic import BaseModel
from datetime import datetime

# Datos de entrada (Como respondera la API)
class CreateFeedback(BaseModel):
    tipo: str
    area: str
    comentario: str
    planta: str
    anonimo: bool = False

# Datos de salida (Como respondera la API)
class FeedbackResponse(BaseModel):
    idfeedback: int

    departamento: str | None = None
    tipo: str

    nombre: str | None = None
    telefono: str | int | None = None
    
    area: str
    comentario: str
    planta: str

    fecha: datetime

    estado: str

    nomina: int

    class Config:
        from_attributes = True
    
# Actualizar estado de idea (GESTOR)
class FeedbackEstadoUpdate(BaseModel):
    estado: str
    