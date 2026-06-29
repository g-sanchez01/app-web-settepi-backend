from pydantic import BaseModel

class UserCreate(BaseModel):
    numero_nomina: int
    nombre: str
    telefono: str
    imss: str
    puesto: str
    departamento: str