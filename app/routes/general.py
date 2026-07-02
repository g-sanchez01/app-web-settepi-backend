from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.security import require_roles, get_current_user
from app.config.database import get_db

from app.schemas.colaborador import ColaboradorResponse
from app.models.colaborador import Colaborador

from app.repositories.colaborador_mes_repository import ColaboradorMesRepository

router = APIRouter(prefix="/general", tags=["General"])


@router.get(
    "/home",
    response_model=ColaboradorResponse
)
def home(
    user: Colaborador = Depends(require_roles(["ADMIN", "GENERAL", "GESTOR"]))
):
    return user

@router.get("/colaborador-mes/actual")
def obtener_colaborador_mes_actual(
    db: Session = Depends(get_db),
    user: Colaborador = Depends(get_current_user)
    
):
    resultado = ColaboradorMesRepository.obtener_actual(
        db,
        user.departamento
    )

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="No existe colaborador del mes para este departamento"
        )


    return resultado