from pydantic import BaseModel
from datetime import datetime

# Este schema se usa normalmente cuando el usuario crea una idea:
# Que los 4 campos existan.
# Que los 4 sean tipo string.
class IdeaCreate(BaseModel):
    unidadNegocio: str
    zona: str
    tituloIdea: str
    descripcionIdea: str

# Este schema define cómo responderá el API.
class IdeaResponse(BaseModel):
    idRegistroIdea: int
    tituloIdea: str
    descripcionIdea: str
    estado: str
    fecha: datetime

    class Config:
        from_attributes = True