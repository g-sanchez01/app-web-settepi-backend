from sqlalchemy.orm import Session
from app.models.feedback_formulario import FeedbackFormulario
from app.models.colaborador import Colaborador
from app.schemas.feedback import CreateFeedback
from app.utils.datetime_utils import now_mexico

from app.repositories.feedback_repository import FeedbackRepository

# Crear Feedback
def crear_feedback(data: CreateFeedback, user: Colaborador, db: Session):

    nuevo_feedback = FeedbackFormulario(
        departamento = "ANONIMO" if data.anonimo else user.departamento,

        tipo = data.tipo,

        nombre = "ANÓNIMO" if data.anonimo else user.nombre,
        telefono = "0" if data.anonimo else user.telefono,

        area = data.area,
        comentario = data.comentario,
        planta = data.planta,
        
        fecha=now_mexico(),

        nomina = user.numero_nomina
    )

    return FeedbackRepository.crear_feedback(db, nuevo_feedback)

# Obtener feedbacks
def obtener_feedbacks(
    db: Session,
    nomina: str,
    idfeedback: int | None = None,
    tipo: str | None = None,
    estado: str | None = None,
    fecha: str | None = None
):
    return FeedbackRepository.obtener_por_nomina(
        db=db,
        nomina=nomina,
        idfeedback=idfeedback,
        tipo=tipo,
        estado=estado,
        fecha=fecha
    )