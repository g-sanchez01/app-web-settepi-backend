from sqlalchemy.orm import Session
from datetime import datetime, date
from sqlalchemy import cast, Date, func
from app.models.colaborador import Colaborador
from app.models.colaborador_mes import ColaboradorMes

class ColaboradorRepository:

    @staticmethod
    def obtener_por_departamento(
        db: Session,
        departamento: str,
        numero_nomina: str | None = None,
        puesto: str | None = None,
        offset: int = 0,
        limit: int = 5

    ):
        hoy = datetime.now()

        ultima_solicitud = (
            db.query(
                ColaboradorMes.numero_nomina,
                func.max(ColaboradorMes.id).label("ultimo_id")
            )
            .filter(
                ColaboradorMes.mes == hoy.month,
                ColaboradorMes.anio == hoy.year
            )
            .group_by(ColaboradorMes.numero_nomina)
            .subquery()
        )

        query = (
            db.query(
                Colaborador,
                ColaboradorMes.estado.label("estado_solicitud")
            )
            .outerjoin(
                ultima_solicitud,
                Colaborador.numero_nomina == ultima_solicitud.c.numero_nomina
            )
            .outerjoin(
                ColaboradorMes,
                ColaboradorMes.id == ultima_solicitud.c.ultimo_id
            )
            .filter(
                Colaborador.departamento == departamento,
                Colaborador.estado == "ACTIVO",
                Colaborador.puesto != "GERENTE",
                Colaborador.puesto != "GERENTE REGIONAL"
            )
        )

        if numero_nomina:
            query = query.filter(
                Colaborador.numero_nomina == numero_nomina
            )

        if puesto:
            query = query.filter(
                Colaborador.puesto.ilike(f"%{puesto}%")
            )

        resultados = (
            query
            .order_by(Colaborador.fecha_creacion)
            .offset(offset)
            .limit(limit)
            .all()
        )

        return [
            {
                "numero_nomina": colaborador.numero_nomina,
                "nombre": colaborador.nombre,
                "puesto": colaborador.puesto,
                "departamento": colaborador.departamento,
                "estado_solicitud": estado if estado else "SIN SOLICITUD"
            }
            
            for colaborador, estado in resultados
        ]
    
    @staticmethod
    def contar_integrantes(db, departamento: str):
        return (
            db.query(func.count(Colaborador.numero_nomina))
            .filter(Colaborador.departamento == departamento)
            .scalar()
        )
    
    # Obtener a todos los usuarios de la plataforma
    @staticmethod
    def obtener_todos(
        db: Session,
        nomina: str | None = None,
        nombre: str | None = None,
        departamento: str | None = None,
        estado: str | None = None,
        fecha_creacion: date | None = None,
        offset: int = 0,
        limit: int = 10
    ):
        query = db.query(Colaborador)

        if nomina:
            query = query.filter(
                Colaborador.numero_nomina == nomina
            )

        if nombre:
            query = query.filter(
                Colaborador.nombre == nombre
            )
        
        if departamento:
            query = query.filter(
                Colaborador.departamento == departamento
            )

        if estado:

            if isinstance(estado, list):
                query = query.filter(
                    Colaborador.estado.in_(estado)
                )
            else:
                query = query.filter(
                    Colaborador.estado == estado
                )

        if fecha_creacion:
            query = query.filter(
                cast(Colaborador.fecha_creacion, Date) == fecha_creacion
            )
        
        return (
            query
            .order_by(
                Colaborador.fecha_creacion.desc()
            )
            .offset(offset)
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def contar_usuarios(db: Session):

        return (
            db.query(Colaborador)
            .filter(Colaborador.estado == "ACTIVO")
            .count()
        )