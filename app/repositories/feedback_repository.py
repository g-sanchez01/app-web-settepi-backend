from app.models.feedback_formulario import FeedbackFormulario

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
        nomina: str
    ):
        return(
            db.query(FeedbackFormulario)
            .filter(
                FeedbackFormulario.nomina == nomina
            )
            .order_by(
                FeedbackFormulario.fecha.desc()
            )
            .all()
        )