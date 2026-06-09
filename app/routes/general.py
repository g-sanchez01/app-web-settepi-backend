from fastapi import APIRouter, Depends

from app.core.security import require_roles
from app.schemas.colaborador import ColaboradorResponse
from app.models.colaborador import Colaborador

router = APIRouter(prefix="/general", tags=["General"])


@router.get(
    "/home",
    response_model=ColaboradorResponse
)
def home(
    user: Colaborador = Depends(require_roles(["ADMIN", "GENERAL", "GESTOR"]))
):
    return user