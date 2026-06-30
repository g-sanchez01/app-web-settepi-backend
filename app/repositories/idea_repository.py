from app.models.idea_formulario import IdeaFormulario
from sqlalchemy import cast, Date, func
from datetime import date

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
        nomina: str,
        idRegistroIdea: str | None = None,
        tituloIdea: str | None = None,
        estado: str | None = None,
        fecha: date | None = None,
        offset: int = 0,
        limit: int = 10
    ):
        query = (
            db.query(IdeaFormulario)
            .filter(
                IdeaFormulario.nomina == nomina
            )
        )

        if idRegistroIdea:
            query = query.filter(
                IdeaFormulario.idRegistroIdea == idRegistroIdea
            )
            
        if tituloIdea:
            query = query.filter(
                IdeaFormulario.tituloIdea == tituloIdea
            )

        if estado:

            if isinstance(estado, list):
                query = query.filter(
                    IdeaFormulario.estado.in_(estado)
                )
            else:
                query = query.filter(
                    IdeaFormulario.estado == estado
                )

        if fecha:
            query = query.filter(
                cast(IdeaFormulario.fecha, Date) == fecha
            )
            
        return (
            query
            .order_by(
                IdeaFormulario.fecha.desc()
            )
            .offset(offset)
            .limit(limit)
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
    def actualizar_idea(db: Session, idea: IdeaFormulario, data: IdeaUpdate):
        for field, value in data.model_dump().items():
            setattr(idea, field, value)

        db.commit()
        db.refresh(idea)
        return idea
    
    @staticmethod
    def enviar_idea(db: Session, idea: IdeaFormulario):
        idea.estado = "ENVIADA"

        db.commit()
        db.refresh(idea)

        return idea
    
    @staticmethod
    def obtener_todas(
        db: Session,
        idRegistroIdea: str | None = None,
        nombre: str | None = None,
        nomina: str | None = None,
        telefono: str | None = None,
        unidadNegocio: str | None = None,
        departamento: str | None = None,
        tituloIdea: str | None = None,
        estado: str | None = None,
        fecha: date | None = None,
        offset: int = 0,
        limit: int = 10
    ):
        query = db.query(IdeaFormulario)

        if idRegistroIdea:
            query = query.filter(
                IdeaFormulario.idRegistroIdea == idRegistroIdea
            )
        
        if nombre:
            query = query.filter(
                IdeaFormulario.nombre == nombre
            )

        if nomina:
            query = query.filter(
                IdeaFormulario.nomina == nomina
            )
        
        if telefono:
            query = query.filter(
                IdeaFormulario.telefono == telefono
            )
        
        if unidadNegocio:
            query = query.filter(
                IdeaFormulario.unidadNegocio == unidadNegocio
            )
        
        if unidadNegocio:
            query = query.filter(
                IdeaFormulario.unidadNegocio == unidadNegocio
            )
        
        if departamento:
            query = query.filter(
                IdeaFormulario.departamento == departamento
            )
        
        if tituloIdea:
            query = query.filter(
                IdeaFormulario.tituloIdea == tituloIdea
            )

        if estado:

            if isinstance(estado, list):
                query = query.filter(
                    IdeaFormulario.estado.in_(estado)
                )
            else:
                query = query.filter(
                    IdeaFormulario.estado == estado
                )

        if fecha:
            query = query.filter(
                cast(IdeaFormulario.fecha, Date) == fecha
            )

        return (
            query
            .order_by(IdeaFormulario.fecha.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def actualizar_estado(
        db: Session,
        idea: IdeaFormulario,
        estado: str
    ):

        idea.estado = estado

        db.commit()
        db.refresh(idea)

        return idea
    
    @staticmethod
    def obtener_estadisticas(db: Session):
        resultados = (
            db.query(
                IdeaFormulario.estado,
                func.count().label("cantidad")
            )
            .group_by(IdeaFormulario.estado)
            .all()
        )

        stats = {
            "total": 0,
            "pendiente": 0,
            "en_proceso": 0,
            "finalizada": 0
        }

        for estado, cantidad in resultados:
            stats["total"] += cantidad

            if estado == "PENDIENTE":
                stats["pendiente"] = cantidad
            elif estado == "EN PROCESO":
                stats["en_proceso"] = cantidad
            elif estado == "APROBADA":
                stats["finalizada"] = cantidad
            elif estado == "RECHAZADA":
                stats["finalizada"] = cantidad

        return stats