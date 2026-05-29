from app.models.idea_formulario import IdeaFormulario

class IdeaRepository:

    @staticmethod
    def obtener_por_nomina(
        db: Session,
        nomina: str
    ):
        return (
            db.query(IdeaFormulario)
            .filter(
                IdeaFormulario.nomina == nomina
            )
            .order_by(
                IdeaFormulario.fecha.desc()
            )
            .all()
        )