from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from app.config.database import Base

# ================================
# MODELO: TABLA colaborador del mes
# ================================

class ColaboradorMes(Base):
    __tablename__ = "empleado_mes"

    id = Column(Integer, primary_key=True, index=True)
    numero_nomina = Column(Integer, ForeignKey("colaboradores.numero_nomina"), nullable=False)
    departamento = Column(String(100), nullable=False)
    mes = Column(Integer, nullable=False)
    anio = Column(Integer, nullable=False)
    fecha_asignacion = Column(DateTime, server_default=func.now())