# ================================
# IMPORTS ORM
# ================================
from sqlalchemy import Column, Integer, String, DateTime, Identity
from datetime import datetime
from app.config.database import Base

# ================================
# MODELO: TABLA colaboradores
# ================================
class Colaborador(Base):

    # Nombre real de la tabla en SQL Server
    __tablename__ = "colaboradores"

    # ================================
    # COLUMNAS DE LA TABLA
    # ================================
    id = Column(
        Integer,
        Identity(),
        primary_key=True
    )

    numero_nomina = Column(
        Integer,
        unique=True,
        nullable=False
    )
    
    nombre = Column(String(100))
    telefono = Column(String(10))
    imss = Column(String(255))
    puesto = Column(String(100))
    departamento = Column(String(100))
    estado = Column(String(10))

    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    rol = Column(String(10))