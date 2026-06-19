from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.core.security import get_current_user

from app.schemas.colaborador_mes import ColaboradorMesCreate

from app.models.colaborador import Colaborador

from app.services.colaborador_service import obtener_equipo_departamento
from app.services.colaborador_mes_service import (
    crear_solicitud, obtener_actual_mes
)

from app.repositories.colaborador_repository import ColaboradorRepository

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
# COLABORADOR DEL MES - SOLICITUD
# ================================
@router.post("/colaborador-mes")
def crear_solicitud_colaborador_mes(
    data: ColaboradorMesCreate,   
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    resultado = crear_solicitud(
        db=db,
        data=data,
        user=user
    )

    return {
        "message": "Solicitud creada correctamente",
        "data": resultado
    }

# ================================
# COLABORADOR DEL MES - OBTENER ACTUAL
# ================================
@router.get("/colaborador-mes/actual")
def obtener_colaborador_mes_actual(
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
    
):
    resultado = obtener_actual_mes(
        db,
        user.departamento
    )

    if not resultado:
        return {
            "message": "No existe colaborador del mes asignado para este departamento"
        }

    return resultado


# ================================
# COLABORADOR DEL MES - OBTENER POR NOMINA
# ================================
@router.get("/colaborador/{numero_nomina}")
def obtener_colaborador_por_nomina(
    numero_nomina: int,
    db: Session = Depends(get_db)
):
    colaborador = db.query(Colaborador).filter(
        Colaborador.numero_nomina == numero_nomina
    ).first()

    if not colaborador:
        return {
            "message": "Colaborador no encontrado"
        }

    return {
        "numero_nomina": colaborador.numero_nomina,
        "nombre": colaborador.nombre,
        "puesto": colaborador.puesto
    }


