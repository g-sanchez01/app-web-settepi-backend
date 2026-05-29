from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.idea import IdeaCreate
from app.models.colaborador import Colaborador
from app.services.idea_service import crear_idea
from app.core.security import get_current_user

router = APIRouter(tags=["Ideas"])


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