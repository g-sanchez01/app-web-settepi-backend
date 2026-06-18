from sqlalchemy.orm import Session
from app.models.colaborador import Colaborador

class ColaboradorRepository:

    @staticmethod
    def obtener_por_departamento(
        db: Session,
        departamento: str
    ):
        return (
            db.query(Colaborador)
            .filter(
                Colaborador.departamento == departamento,
                Colaborador.estado == "ACTIVO",
                Colaborador.puesto != "GERENTE"
            )
            .order_by(Colaborador.fecha_creacion)  # o nombre, o fecha_creacion
            .limit(5)
            .all()
        )