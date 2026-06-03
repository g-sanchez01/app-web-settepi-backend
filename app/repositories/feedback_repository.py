from app.models.feedback_formulario import FeedbackFormulario

class FeedbackRepository:

    @staticmethod
    def crear_feedback(db: Session, feedback: FeedbackFormulario):
        db.add(feedback)
        db.commit()
        db.refresh(feedback)

        return feedback