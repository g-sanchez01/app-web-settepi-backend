from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.core.security import get_current_user
from app.models.colaborador import Colaborador
from app.services.colaborador_service import obtener_equipo_departamento

router = APIRouter(
    prefix="/lider",
    tags=["Lider"]
)

@router.get("/equipo")
def obtener_equipo(
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
):

    return obtener_equipo_departamento(
        db=db,
        user=user
    )