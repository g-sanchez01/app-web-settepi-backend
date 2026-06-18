from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.config.database import get_db
from app.core.security import get_current_user
from app.models.colaborador import Colaborador
from app.models.colaborador_mes import ColaboradorMes
from app.services.colaborador_service import obtener_equipo_departamento
from app.services.colaborador_mes_service import obtener_colaborador_mes
from app.repositories.colaborador_repository import ColaboradorRepository
from app.repositories.colaborador_mes_repository import ColaboradorMesRepository

router = APIRouter(
    prefix="/lider",
    tags=["Lider"]
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
# COLABORADOR DEL MES
# ================================

@router.post("/colaborador-mes/asignar")
def asignar_colaborador_mes(
    numero_nomina: int,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    resultado = ColaboradorMesRepository.asignar(
        db=db,
        numero_nomina=numero_nomina,
        departamento=user.departamento
    )

    if not resultado:
        return {
            "message": "Ya existe un colaborador del mes para este departamento"
        }

    return {
        "message": "Colaborador del mes asignado correctamente",
        "data": resultado
    }


@router.get("/colaborador-mes")
def obtener_colaborador_mes_endpoint(
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    result = obtener_colaborador_mes(
        db=db,
        departamento=user.departamento
    )

    if not result:
        return {"message": "No hay colaborador del mes asignado"}

    return result