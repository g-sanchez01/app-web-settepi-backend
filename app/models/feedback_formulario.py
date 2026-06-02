from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.config.database import Base
from app.utils.datetime_utils import now_mexico

class FeedbackFormulario(Base):
    __tablename__ = "settepi_feedback"

    idfeedback = Column(Integer, primary_key = True, index = True)

    departamento = Column(String(255))
    tipo = Column(String(50))
    nombre = Column(String(255))
    telefono = Column(String(10))
    area = Column(String(50))
    comentario = Column(String)
    planta = Column(String(50))
    fecha = Column(DateTime, default=now_mexico)
    estado = Column(String(50), default="PENDIENTE")