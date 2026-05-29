from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.services.auth_service import authenticate_user

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