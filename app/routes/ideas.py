from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import date

from app.config.database import get_db

from app.schemas.idea import IdeaCreate, IdeaResponse, IdeaUpdate, IdeaEstadoUpdate
from app.repositories.idea_repository import IdeaRepository


from app.models.colaborador import Colaborador
from app.services.idea_service import crear_idea, editar_idea, obtener_ideas, actualizar_estado_idea, enviar_idea as enviar_idea_service
from app.core.security import get_current_user

router = APIRouter(tags=["Ideas"])


# Registrar Ideas
@router.post(
        "/registrar",
        status_code=status.HTTP_201_CREATED
    )
def registrar_idea(
    data: IdeaCreate,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    nueva = crear_idea(data, user, db)

    return {
        "message": "Idea registrada correctamente 🚀",
        "idRegistroIdea": nueva.idRegistroIdea
    }

# Mostrar ideas propias
@router.get(
    "/mis-ideas",
    response_model=list[IdeaResponse]
)
def obtener_mis_ideas(
    idRegistroIdea: int | None = None,
    nombre: str | None = None,
    nomina: str | None = None,
    telefono: str | None = None,
    unidadNegocio: str | None = None,
    departamento: str | None = None,
    tituloIdea: str | None = None,
    estado: str | None = None,
    fecha: date | None = None,
    offset: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    return obtener_ideas(
        db=db,
        user=user,
        idRegistroIdea=idRegistroIdea,
        nombre=nombre,
        nomina=nomina,
        telefono=telefono,
        unidadNegocio=unidadNegocio,
        departamento=departamento,
        tituloIdea=tituloIdea,
        estado=estado,
        fecha=fecha,
        offset=offset,
        limit=limit
    )

@router.get("/estadisticas")
def obtener_estadisticas(
    db: Session = Depends(get_db)
):
    return IdeaRepository.obtener_estadisticas(db)

# Cambiar estado de idea (GESTOR)
@router.put("/{id_idea}/estado")
def actualizar_estado_endpoint(
    id_idea: int,
    data: IdeaEstadoUpdate,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    idea = actualizar_estado_idea(
        db=db,
        id_idea=id_idea,
        estado=data.estado
    )

    return {
        "message": "Estado actualizado correctamente",
        "idRegistroIdea": idea.idRegistroIdea,
        "estado": idea.estado
    }

# Obtener id de la idea
@router.get("/{id_idea}")
def obtener_idea_por_id(
    id_idea: int,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    idea = IdeaRepository.obtener_por_id(db, id_idea)

    if not idea:
        raise HTTPException(
            status_code=404,
            detail="Idea no encontrada"
        )

    return idea

# Editar Idea
@router.put("/{id_idea}")
def editar_idea_endpoint(
    id_idea: int,
    data: IdeaUpdate,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    idea_editada = editar_idea(db, id_idea, data)

    return {
        "message": "Idea actualizada correctamente",
        "idRegistroIdea": idea_editada.idRegistroIdea
    }

# Enviar Idea
@router.put("/enviar/{id_idea}")
def enviar_idea_endpoint(
    id_idea: int,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):
    idea = enviar_idea_service(
        db,
        id_idea
    )

    return {
        "message": "Idea enviada correctamente",
        "idRegistroIdea": idea.idRegistroIdea
    }

