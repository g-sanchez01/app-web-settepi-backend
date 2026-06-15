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
        area: str | None = None,
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
        
        if area:
            query = query.filter(
                FeedbackFormulario.area == area
            )

        if estado:

            if isinstance(estado, list):
                query = query.filter(
                    FeedbackFormulario.estado.in_(estado)
                )
            else:
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
    
    @staticmethod
    def obtener_todas(
        db: Session,
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
        offset: int = 0,
        limit: int = 10
    ):
        query = db.query(FeedbackFormulario)

        if idfeedback:
            query = query.filter(
                FeedbackFormulario.idfeedback == idfeedback
            )
        
        if departamento:
            query = query.filter(
                FeedbackFormulario.departamento == departamento
            )

        if tipo:
            query = query.filter(
                FeedbackFormulario.tipo == tipo
            )
        
        if nombre:
            query = query.filter(
                FeedbackFormulario.nombre == nombre
            )
        
        if nomina:
            query = query.filter(
                FeedbackFormulario.nomina == nomina
            )
        
        if telefono:
            query = query.filter(
                FeedbackFormulario.telefono == telefono
            )
        
        if area:
            query = query.filter(
                FeedbackFormulario.area == area
            )
        
        if planta:
            query = query.filter(
                FeedbackFormulario.planta == planta
            )
        
        if estado:

            if isinstance(estado, list):
                query = query.filter(
                    FeedbackFormulario.estado.in_(estado)
                )
            else:
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
            .offset(offset)
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def obtener_por_id(db: Session, id_feedback: int):
        return (
            db.query(FeedbackFormulario)
            .filter(FeedbackFormulario.idfeedback == id_feedback)
            .first()
        )
