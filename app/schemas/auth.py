from pydantic import BaseModel

# =========================
# LOGIN REQUEST: Schema de entrada (request) para el login
# Frontend → Backend (credenciales)
# =========================
class LoginSchema(BaseModel):

    numero_nomina: int
    imss: str