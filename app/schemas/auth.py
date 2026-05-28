from pydantic import BaseModel

# =========================
# LOGIN REQUEST
# =========================
class LoginSchema(BaseModel):

    numero_nomina: int
    imss: str