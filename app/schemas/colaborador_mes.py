from pydantic import BaseModel

class ColaboradorMesCreate(BaseModel):
    numero_nomina: int
    departamento: str
    puesto: str
    motivo_solicitud: str