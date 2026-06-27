from sqlalchemy.orm import Session
from datetime import date

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

# Obtener a todos los usuarios de la plataforma
def obtener_usuarios(
    db: Session,
    user: Colaborador,
    nomina: str | None = None,
    nombre: str | None = None,
    departamento: str | None = None,
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
        estado=estado,
        fecha_creacion=fecha_creacion,
        offset=offset,
        limit=limit
    )

def contar_usuarios(db: Session):
    return ColaboradorRepository.contar_usuarios(db)


