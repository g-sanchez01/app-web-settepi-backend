from pydantic import BaseModel

class IdeaCreate(BaseModel):
    unidadNegocio: str
    zona: str
    tituloIdea: str
    descripcionIdea: str