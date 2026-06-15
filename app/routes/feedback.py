from fastapi import APIRouter, Depends, status
from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.config.database import get_db

from app.schemas.feedback import CreateFeedback, FeedbackResponse
from app.repositories.feedback_repository import FeedbackRepository

from app.models.colaborador import Colaborador
from app.services.feedback_service import crear_feedback, obtener_feedbacks
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
    idfeedback: int | None = None,
    departamento: str | None = None,
    tipo: str | None = None,
    nombre: str | None = None,
    telefono: str | None = None,
    area: str | None = None,
    planta: str | None = None,
    estado: str | None = None,
    fecha: date | None = None,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):
    return obtener_feedbacks(
        db=db,
        user=user,
        nomina=str(user.numero_nomina),
        nombre=nombre,
        departamento=departamento,
        telefono=telefono,
        idfeedback=idfeedback,
        tipo=tipo,
        area=area,
        planta=planta,
        estado=estado,
        fecha=fecha
    )

# Obtener id del feedback
@router.get("/{id_feedback}")
def obtener_feedback_por_id(
    id_feedback: int,
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):
    feedback = FeedbackRepository.obtener_por_id(db, id_feedback)

    if not feedback:
        raise HTTPException(
            status_code=404,
            detail="Feedback no encontrado"
        )

    return feedback