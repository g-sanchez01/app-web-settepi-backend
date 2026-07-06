# routes/maintenance.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.system_config import SystemConfig

router = APIRouter(prefix="/system", tags=["System"])

@router.get("/maintenance")
def get_maintenance(db: Session = Depends(get_db)):

    config = db.query(SystemConfig)\
        .filter(SystemConfig.key_name == "maintenance")\
        .first()

    return {
        "maintenance": config.value.lower() == "true"
    }