from fastapi import APIRouter, Depends
from app.core.security import get_current_user

router = APIRouter()

@router.delete("/admin/usuarios")
def delete_user(
    user=Depends(require_roles(["admin"]))
):
    return {
        "message": "Solo admin"
    }