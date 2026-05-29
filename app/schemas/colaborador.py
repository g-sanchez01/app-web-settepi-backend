from pydantic import BaseModel
from typing import Optional

# Datos del usuario desde SQL
# Backend → frontend (mostrar perfil / datos)
class ColaboradorResponse(BaseModel):

    numero_nomina: int
    nombre: str
    telefono: Optional[str] = None
    puesto: str
    departamento: str
    rol: str

    class Config:
        from_attributes = True