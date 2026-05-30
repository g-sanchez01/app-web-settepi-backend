from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.schemas.idea import IdeaCreate, IdeaResponse, IdeaUpdate
from app.repositories.idea_repository import IdeaRepository


from app.models.colaborador import Colaborador
from app.services.idea_service import crear_idea, editar_idea
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
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    return IdeaRepository.obtener_por_nomina(
        db,
        str(user.numero_nomina)
    )

# Editar Idea
@router.put(
    "/editar/{id_idea}",
    status_code=status.HTTP_200_OK
)
def editar_idea_endpoint(
    id_idea: int,
    data: IdeaUpdate,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    idea_editada = editar_idea(db, id_idea, data)

    return {
        "message": "Idea actualizada correctamente ",
        "idRegistroIdea": idea_editada.idRegistroIdea
    }
        