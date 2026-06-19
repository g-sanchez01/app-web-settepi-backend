from pydantic import BaseModel

class ColaboradorMesCreate(BaseModel):
    numero_nomina: int
    motivo_solicitud: str