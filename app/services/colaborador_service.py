from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import date

from app.models.colaborador import Colaborador
from app.repositories.colaborador_repository import ColaboradorRepository
from app.schemas.usuario import UserCreate


# Obtener integrantes del equipo
def obtener_equipo_departamento(
    db: Session,
    user: Colaborador,
    numero_nomina: str | None = None,
    puesto: str | None = None,
    offset: int = 0,
    limit: int = 5
):

    return ColaboradorRepository.obtener_por_departamento(
        db=db,
        departamento=user.departamento,
        numero_nomina=numero_nomina,
        puesto=puesto,
        offset=offset,
        limit=limit
    )

# Obtener a todos los usuarios de la plataforma
def obtener_usuarios(
    db: Session,
    user: Colaborador,
    nomina: str | None = None,
    nombre: str | None = None,
    departamento: str | None = None,
    area: str | None = None,
    estado: str | None = None,
    fecha_creacion: date | None = None,
    offset: int = 0,
    limit: int = 10
):
    if user.rol != "ADMIN_DEV":
        nomina = user.numero_nomina

    return ColaboradorRepository.obtener_todos(
        db=db,
        nomina=nomina,
        nombre=nombre,
        departamento=departamento,
        area=area,
        estado=estado,
        fecha_creacion=fecha_creacion,
        offset=offset,
        limit=limit
    )

def obtener_por_nomina_usuario(
    db: Session,
    numero_nomina: int
):
    usuario = ColaboradorRepository.obtener_por_nomina(
        db,
        numero_nomina
)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario

def contar_usuarios(db: Session):
    return ColaboradorRepository.contar_usuarios(db)

def insertar_usuario(
    db: Session,
    usuario: UserCreate
):
    colaborador = ColaboradorRepository.obtener_por_nomina(
        db,
        usuario.numero_nomina
    )

    if colaborador:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un usuario con ese número de nómina."
        )

    return ColaboradorRepository.insertar_usuario(
        db=db,
        usuario=usuario
    )

def desactivar_usuario(
    db: Session,
    numero_nomina: int
):
    usuario = ColaboradorRepository.desactivar_usuario(
        db=db,
        numero_nomina=numero_nomina
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario

def reactivar_usuario(db: Session, numero_nomina: int):
    usuario = ColaboradorRepository.reactivar_usuario(db, numero_nomina)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario


