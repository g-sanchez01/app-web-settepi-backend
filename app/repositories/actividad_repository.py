from app.models.actividades import ActividadDashboard
from sqlalchemy.exc import SQLAlchemyError

class ActividadRepository:

    @staticmethod
    def crear(db, descripcion: str, usuario: str, estado: str = None):
        try:
            actividad = ActividadDashboard(
                descripcion=descripcion,
                usuario=usuario,
                estado=estado
            )

            db.add(actividad)
            db.commit()
            db.refresh(actividad)

            return actividad

        except SQLAlchemyError as e:
            db.rollback()
            print("🔥 ERROR SQL AQUI:", str(e))
            raise

    @staticmethod
    def obtener_recientes(
        db,
        limite: int = 10
    ):
        return (
            db.query(ActividadDashboard)
            .order_by(ActividadDashboard.fecha.desc())
            .limit(limite)
            .all()
        )