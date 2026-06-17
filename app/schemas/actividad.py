from pydantic import BaseModel
from datetime import datetime

class ActividadResponse(BaseModel):
    idActividad: int
    descripcion: str
    usuario: str
    estado: str | None
    fecha: datetime

    class Config:
        from_attributes = True