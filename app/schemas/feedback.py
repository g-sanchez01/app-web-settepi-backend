from pydantic import BaseModel
from datetime import datetime

class CreateFeedback(BaseModel):
    tipo: str
    area: str
    comentario: str
    planta: str
    anonimo: bool = False