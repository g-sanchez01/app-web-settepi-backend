from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.colaborador import Colaborador

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
        query = (
            db.query(Colaborador)
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


        return (
            query
            .order_by(Colaborador.fecha_creacion)  # o nombre, o fecha_creacion
            .offset(offset)
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def contar_integrantes(db, departamento: str):
        return (
            db.query(func.count(Colaborador.numero_nomina))
            .filter(Colaborador.departamento == departamento)
            .scalar()
        )