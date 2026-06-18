from datetime import datetime
from sqlalchemy.orm import Session
from app.models.colaborador_mes import ColaboradorMes
from app.models.colaborador import Colaborador

def obtener_colaborador_mes(db: Session, departamento: str):

    now = datetime.now()

    result = (
        db.query(ColaboradorMes, Colaborador)
        .join(Colaborador, Colaborador.numero_nomina == ColaboradorMes.numero_nomina)
        .filter(
            ColaboradorMes.departamento == departamento,
            ColaboradorMes.mes == now.month,
            ColaboradorMes.anio == now.year
        )
        .first()
    )

    if not result:
        return None

    colaborador_mes, colaborador = result

    return {
        "numero_nomina": colaborador.numero_nomina,
        "nombre": colaborador.nombre,
        "puesto": colaborador.puesto,
        "departamento": colaborador.departamento,
        "mes": colaborador_mes.mes,
        "anio": colaborador_mes.anio
    }