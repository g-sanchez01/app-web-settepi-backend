from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.config.database import get_db
from app.core.security import get_current_user

from app.schemas.colaborador_mes import ColaboradorMesCreate
from app.schemas.colaborador import ColaboradorResponse
from app.schemas.usuario import UserCreate

from app.models.colaborador import Colaborador

from app.services.colaborador_service import obtener_equipo_departamento, obtener_usuarios, contar_usuarios, obtener_por_nomina_usuario, insertar_usuario, desactivar_usuario, reactivar_usuario
from app.services.colaborador_mes_service import (
    aprobar_solicitud, rechazar_solicitud, obtener_historial_colaborador_mes, obtener_historial_admin, 
    contar_asignados, contar_pendientes, obtener_actual_mes, 
)

from app.repositories.colaborador_repository import ColaboradorRepository
from app.repositories.colaborador_mes_repository import ColaboradorMesRepository

router = APIRouter(
    prefix="/admindev",
    tags=["AdminDev"]
)

# ================================
# EQUIPO
# ================================

@router.get("/equipo")
def obtener_equipo(
    numero_nomina: str | None = None,
    area: str | None = None,
    offset: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    return obtener_equipo_departamento(
        db=db,
        user=user,
        numero_nomina=numero_nomina,
        area=area,
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

# ================================
# COLABORADOR DEL MES - RECHAZAR
# ================================

@router.put("/colaborador-mes/rechazar/{id_solicitud}")
def rechazar_colaborador_mes(
    id_solicitud: int,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    return rechazar_solicitud(
        db=db,
        id_solicitud=id_solicitud,
        user=user
    )


# ================================
# COLABORADOR DEL MES - HISTORIAL
# ================================
@router.get("/colaborador-mes/historial")
def obtener_historial(
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):
    return obtener_historial_colaborador_mes(
        db=db,
        user=user
    )

@router.get("/colaborador-mes/historial-admin")
def obtener_historial_admin_colaborador_mes(
    id: int | None = None,
    numero_nomina: str | None = None,
    nombre: str | None = None,
    departamento: str | None = None,
    fecha_solicitud: date | None = None,
    estado: str | None = None,
    offset: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):
    return obtener_historial_admin(
        db=db,
        user=user,
        id=id,
        numero_nomina=numero_nomina,
        nombre=nombre,
        departamento=departamento,
        fecha_solicitud=fecha_solicitud,
        estado=estado,
        offset=offset,
        limit=limit
    )

@router.get("/colaborador-mes/asignados/total")
def total_asignados(
    db: Session = Depends(get_db),
):

    return {
        "total": contar_asignados(db)
    }

@router.get("/colaborador-mes/pendientes/total")
def total_asignados(
    db: Session = Depends(get_db),
):

    return {
        "total": contar_pendientes(db)
    }

# Obtener id de la solicitud
@router.get("/colaborador-mes/{id_solicitud}")
def obtener_solicitud_por_id(
    id_solicitud: int,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    solicitud = ColaboradorMesRepository.obtener_por_id(db, id_solicitud)

    if not solicitud:
        raise HTTPException(
            status_code=404,
            detail="Solicitud no encontrada"
        )

    return solicitud

# ================================
# USUARIOS
# ================================
@router.get("/usuarios")
def obtener_usuarios_admin(
    nomina: str | None = None,
    nombre: str | None = None,
    departamento: str | None = None,
    estado: str | None = None,
    fecha_creacion: date | None = None,
    offset: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    return obtener_usuarios(
        db=db,
        user=user,
        nomina=nomina,
        nombre=nombre,
        departamento=departamento,
        estado=estado,
        fecha_creacion=fecha_creacion,
        offset=offset,
        limit=limit
    )


@router.get("/usuarios/total")
def total_asignados(
    db: Session = Depends(get_db),
):

    return {
        "total": contar_usuarios(db)
    }


@router.get(
    "/usuarios/{numero_nomina}",
    response_model=ColaboradorResponse
)
def obtener_usuario(
    numero_nomina: int,
    db: Session = Depends(get_db)
):
    return obtener_por_nomina_usuario(
        db,
        numero_nomina
    )

@router.post("/usuarios/create")
def crear_usuario(
    usuario: UserCreate,
    db: Session = Depends(get_db)
):
    return insertar_usuario(
        db=db,
        usuario=usuario
    )

@router.patch("/usuarios/{numero_nomina}/desactivar")
def desactivar_usuario_admin(
    numero_nomina: int,
    db: Session = Depends(get_db)
):
    return desactivar_usuario(
        db=db,
        numero_nomina=numero_nomina
    )

@router.patch("/usuarios/{numero_nomina}/reactivar")
def reactivar_usuario_admin(
    numero_nomina: int,
    db: Session = Depends(get_db)
):
    return reactivar_usuario(
        db=db,
        numero_nomina=numero_nomina
    )




