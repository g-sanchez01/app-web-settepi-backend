from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.schemas.feedback import CreateFeedback
from app.repositories.feedback_repository import FeedbackRepository

from app.models.colaborador import Colaborador
from app.services.feedback_service import crear_feedback
from app.core.security import get_current_user

router = APIRouter(tags=["Feedbacks"])

# Registrar Ideas
@router.post(
        "/registrar",
        status_code=status.HTTP_201_CREATED
    )
def registrar_feedback(
    data: CreateFeedback,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    nueva = crear_feedback(data, user, db)

    return {
        "message": "Feedback envíado correctamente 🚀",
        "idfeedback": nueva.idfeedback
    }