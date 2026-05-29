from pydantic import BaseModel

# Lo que viaja dentro del token
# Backend → genera token → frontend → backend lo decodifica

class UserToken(BaseModel):
    numero_nomina: int
    nombre: str
    telefono: str
    departamento: str
    rol: str