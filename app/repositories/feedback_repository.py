from app.models.feedback_formulario import FeedbackFormulario
from sqlalchemy import cast, Date
from datetime import date

class FeedbackRepository:

    @staticmethod
    def crear_feedback(db: Session, feedback: FeedbackFormulario):
        db.add(feedback)
        db.commit()
        db.refresh(feedback)

        return feedback
    
    @staticmethod
    def obtener_por_nomina(
        db: Session,
        nomina: str,
        idfeedback: int | None = None,
        tipo: str | None = None,
        estado: str | None = None,
        fecha: date | None = None
    ):
        query = (
            db.query(FeedbackFormulario)
            .filter(
                FeedbackFormulario.nomina == nomina
            )
        )

        if idfeedback:
            query = query.filter(
                FeedbackFormulario.idfeedback == idfeedback
            )

        if tipo:
            query = query.filter(
                FeedbackFormulario.tipo == tipo
            )

        if estado:
            query = query.filter(
                FeedbackFormulario.estado == estado
            )

        if fecha:
            query = query.filter(
                cast(FeedbackFormulario.fecha, Date) == fecha
            )

        return (
            query
            .order_by(
                FeedbackFormulario.fecha.desc()
            )
            .all()
        )