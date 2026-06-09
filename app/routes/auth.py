from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.services.auth_service import authenticate_user

from app.core.security import get_current_user
from app.schemas.colaborador import ColaboradorResponse
from app.models.colaborador import Colaborador

router = APIRouter()

@router.post("/login")
def login(
    data: dict,
    db: Session = Depends(get_db)
):
    return authenticate_user(
        numero_nomina=data["numero_nomina"],
        imss=data["imss"],
        db=db
    )


@router.get(
    "/me",
    response_model=ColaboradorResponse
)
def me(
    user: Colaborador = Depends(get_current_user)
):
    return user