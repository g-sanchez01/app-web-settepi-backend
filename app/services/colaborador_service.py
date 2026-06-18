from sqlalchemy.orm import Session

from app.models.colaborador import Colaborador
from app.repositories.colaborador_repository import ColaboradorRepository


# Obtener integrantes del equipo
def obtener_equipo_departamento(
    db: Session,
    user: Colaborador
):
    
    print("Departamento:", user.departamento)

    return ColaboradorRepository.obtener_por_departamento(
        db=db,
        departamento=user.departamento
    )