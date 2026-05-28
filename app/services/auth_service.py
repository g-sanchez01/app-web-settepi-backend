from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.colaborador import Colaborador
from app.core.security import create_token

# =========================
# 🔐 LOGIN SERVICE
# =========================
def authenticate_user(
    numero_nomina: int,
    imss: str,
    db: Session
):

    # buscar colaborador
    colab = db.query(Colaborador).filter(
        Colaborador.numero_nomina == numero_nomina
    ).first()

    # validar usuario
    if not colab:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    # temporal SIN HASH
    if imss != colab.imss:
        raise HTTPException(
            status_code=401,
            detail="IMSS incorrecto"
        )

    # crear token
    token = create_token({
        "nomina": colab.numero_nomina,
        "rol": colab.rol
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }