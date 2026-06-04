from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.schemas.feedback import CreateFeedback, FeedbackResponse
from app.repositories.feedback_repository import FeedbackRepository

from app.models.colaborador import Colaborador
from app.services.feedback_service import crear_feedback
from app.core.security import get_current_user

router = APIRouter(tags=["Feedbacks"])

# Registrar Feedbacks
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


# Mostrar Feedbacks propios
@router.get(
    "/settepi-te-escucha",
    response_model=list[FeedbackResponse]
)
def obtener_mis_feedbacks(
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    return FeedbackRepository.obtener_por_nomina(
        db,
        str(user.numero_nomina)
    )