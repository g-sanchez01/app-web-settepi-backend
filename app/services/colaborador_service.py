from sqlalchemy.orm import Session

from app.models.colaborador import Colaborador
from app.repositories.colaborador_repository import ColaboradorRepository


# Obtener integrantes del equipo
def obtener_equipo_departamento(
    db: Session,
    user: Colaborador,
    numero_nomina: str | None = None,
    puesto: str | None = None,
    offset: int = 0,
    limit: int = 5
):
    
    print("Departamento:", user.departamento)

    return ColaboradorRepository.obtener_por_departamento(
        db=db,
        departamento=user.departamento,
        numero_nomina=numero_nomina,
        puesto=puesto,
        offset=offset,
        limit=limit
    )