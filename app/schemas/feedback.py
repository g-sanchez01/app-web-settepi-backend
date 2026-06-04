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
    tipo: str
    area: str
    comentario: str
    planta: str
    fecha: datetime
    estado: str

    class Config:
        from_attributes = True