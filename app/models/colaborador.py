# ================================
# IMPORTS ORM
# ================================
from sqlalchemy import Column, Integer, String, DateTime
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
    numero_nomina = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    telefono = Column(String(10))
    imss = Column(String(255))
    puesto = Column(String(100))
    departamento = Column(String(100))
    estado = Column(String(10))

    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    rol = Column(String(10))