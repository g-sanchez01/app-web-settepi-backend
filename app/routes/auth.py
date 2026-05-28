from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.schemas.auth import LoginSchema
from app.services.auth_service import authenticate_user

router = APIRouter()

# =========================
# 📦 DB SESSION
# =========================
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# =========================
# 🔐 LOGIN
# =========================
@router.post("/login")
def login(
    data: LoginSchema,
    db: Session = Depends(get_db)
):

    return authenticate_user(
        numero_nomina=data.numero_nomina,
        imss=data.imss,
        db=db
    )