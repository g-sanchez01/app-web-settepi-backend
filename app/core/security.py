import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta

from app.config.database import SessionLocal
from app.models.colaborador import Colaborador

# =========================
# 🌱 LOAD ENV
# =========================
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_MINUTES = int(os.getenv("EXPIRE_MINUTES"))

# =========================
# 🔐 PASSWORD HASHING
# =========================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# =========================
# 🎫 CREATE JWT TOKEN
# =========================
def create_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

# =========================
# 🔐 HTTP BEARER
# =========================
security = HTTPBearer()

# =========================
# 👤 GET CURRENT USER
# =========================
def get_current_user(token=Depends(security)):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:

        payload = jwt.decode(
            token.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        numero_nomina = payload.get("nomina")
        rol = payload.get("rol")

        if numero_nomina is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    db = SessionLocal()

    user = db.query(Colaborador).filter(
        Colaborador.numero_nomina == numero_nomina
    ).first()

    db.close()

    if user is None:
        raise credentials_exception

    return user

# =========================
# 🛡️ VALIDAR ROLES
# =========================
def require_roles(roles: list):

    def role_checker(
        user=Depends(get_current_user)
    ):

        if user.rol not in roles:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos"
            )

        return user

    return role_checker