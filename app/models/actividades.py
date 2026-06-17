from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.config.database import Base

class ActividadDashboard(Base):
    __tablename__ = "ActividadDashboard"

    idActividad = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(255), nullable=False)
    usuario = Column(String(100), nullable=False)
    estado = Column(String(50), nullable=True)

    fecha = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )