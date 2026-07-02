from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.config.database import Base

class ColaboradorMes(Base):
    __tablename__ = "colaborador_mes"

    id = Column(Integer, primary_key=True, index=True)

    numero_nomina = Column(
        Integer,
        ForeignKey("colaboradores.numero_nomina"),
        nullable=False
    )

    departamento = Column(String(100), nullable=False)
    area = Column(String(100), nullable=False)

    puesto = Column(String(100), nullable=False)

    motivo_solicitud = Column(String(500), nullable=False)

    mes = Column(Integer, nullable=False)
    anio = Column(Integer, nullable=False)

    fecha_solicitud = Column(
        DateTime,
        server_default=func.now()
    )

    fecha_asignacion = Column(
        DateTime,
        nullable=True
    )

    estado = Column(
        String(20),
        nullable=False,
        default="PENDIENTE"
    )