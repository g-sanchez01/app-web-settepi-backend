from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.repositories.actividad_repository import ActividadRepository
from app.schemas.actividad import ActividadResponse

router = APIRouter(
    tags=["Actividades"]
)

@router.get(
    "",
    response_model=list[ActividadResponse]
)
def obtener_actividades(
    db: Session = Depends(get_db)
):
    return ActividadRepository.obtener_recientes(
        db=db,
        limite=10
    )