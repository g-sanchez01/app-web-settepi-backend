from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.config.database import Base
from app.utils.datetime_utils import now_mexico

class IdeaFormulario(Base):

    __tablename__ = "ideasFormulario"

    idRegistroIdea = Column(Integer, primary_key = True, index = True)

    nombre = Column(String(150))
    nomina = Column(String(50))
    telefono = Column(String(10))

    unidadNegocio = Column(String(100))
    zona = Column(String(100))
    departamento = Column(String(255))

    tituloIdea = Column(String(255))
    descripcionIdea = Column(String)

    fecha = Column(DateTime, default=now_mexico)
    estado = Column(String(50), default="BORRADOR")