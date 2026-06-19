from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.core.security import get_current_user

from app.schemas.colaborador_mes import ColaboradorMesCreate

from app.models.colaborador import Colaborador

from app.services.colaborador_service import obtener_equipo_departamento
from app.services.colaborador_mes_service import (
    aprobar_solicitud
)

from app.repositories.colaborador_repository import ColaboradorRepository

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# ================================
# EQUIPO
# ================================

@router.get("/equipo")
def obtener_equipo(
    numero_nomina: str | None = None,
    puesto: str | None = None,
    offset: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    return obtener_equipo_departamento(
        db=db,
        user=user,
        numero_nomina=numero_nomina,
        puesto=puesto,
        offset=offset,
        limit=limit
    )

@router.get("/equipo/total")
def obtener_total_equipo(
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):
    total = ColaboradorRepository.contar_integrantes(
        db=db,
        departamento=user.departamento
    )

    return {"total": total}

# ================================
# COLABORADOR DEL MES - ASIGNACION
# ================================

@router.put("/colaborador-mes/aprobar/{id_solicitud}")
def aprobar_colaborador_mes(
    id_solicitud: int,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    return aprobar_solicitud(
        db=db,
        id_solicitud=id_solicitud,
        user=user
    )


