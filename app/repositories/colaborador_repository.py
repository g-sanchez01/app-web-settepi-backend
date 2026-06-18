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
            .all()
        )