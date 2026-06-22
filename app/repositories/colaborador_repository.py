from sqlalchemy.orm import Session
from sqlalchemy import func
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
        ultima_solicitud = (
            db.query(
                ColaboradorMes.numero_nomina,
                func.max(ColaboradorMes.id).label("ultimo_id")
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
                Colaborador.puesto != "GERENTE"
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
                "estado_solicitud": estado or "SIN SOLICITUD"
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