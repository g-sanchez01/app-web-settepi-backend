from fastapi import APIRouter, Depends
from app.core.security import require_roles
from app.schemas.colaborador import ColaboradorResponse

router = APIRouter()

@router.get(
    "/general/home",
    response_model=ColaboradorResponse
)
def home(
    user=Depends(require_roles(["ADMIN", "GENERAL"]))
):

    return user