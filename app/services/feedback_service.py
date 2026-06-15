from sqlalchemy.orm import Session
from datetime import date
from app.models.feedback_formulario import FeedbackFormulario
from app.models.colaborador import Colaborador
from app.constants.estados_feedback import ESTADOS_GESTOR, ESTADOS_GENERAL
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
    user: Colaborador,
    idfeedback: int | None = None,
    departamento: str | None = None,
    tipo: str | None = None,
    nombre: str | None = None,
    nomina: str | None = None,
    telefono: str | None = None,
    area: str | None = None,
    planta: str | None = None,
    estado: str | None = None,
    fecha: date | None = None,
):
    
    # Administrador: ve todas las ideas
    if user.rol == "GESTOR":
        estado_filtro = estado if estado else ESTADOS_GESTOR

        return FeedbackRepository.obtener_todas(
            db=db,
            nombre=nombre,
            departamento=departamento,
            telefono=telefono,
            idfeedback=idfeedback,
            tipo=tipo,
            area=area,
            planta=planta,
            estado=estado_filtro,
            fecha=fecha
        )
    

    # Usuario General
    estado_filtro = estado if estado else ESTADOS_GENERAL

    return FeedbackRepository.obtener_por_nomina(
        db=db,
        nomina=user.numero_nomina,
        idfeedback=idfeedback,
        tipo=tipo,
        area=area,
        estado=ESTADOS_GENERAL,
        fecha=fecha
    )