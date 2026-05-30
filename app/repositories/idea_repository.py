from app.models.idea_formulario import IdeaFormulario

class IdeaRepository:

    @staticmethod
    def crear_idea(db: Session, idea: IdeaFormulario):
        db.add(idea)
        db.commit()
        db.refresh(idea)
        return idea

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
    
    @staticmethod
    def obtener_por_id(db: Session, id_idea: int):
        return (
            db.query(IdeaFormulario)
            .filter(IdeaFormulario.idRegistroIdea == id_idea)
            .first()
        )
    
    @staticmethod
    def actualizar_idea(db: Session, idea: IdeaFormulario, data):
        idea.unidadNegocio = data.unidadNegocio
        idea.zona = data.zona
        idea.tituloIdea = data.tituloIdea
        idea.descripcionIdea = data.descripcionIdea

        db.commit()
        db.refresh(idea)

        return idea