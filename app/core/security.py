import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta

from app.config.database import SessionLocal
from app.models.colaborador import Colaborador

# =========================
# 🌱 LOAD ENV
# =========================
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRE_MINUTES = int(os.getenv("EXPIRE_MINUTES", "60"))

if not SECRET_KEY:
    raise Exception("SECRET_KEY no configurada en .env")

# =========================
# 🔐 HTTP BEARER (REEMPLAZA OAUTH2)
# =========================
oauth2_scheme = HTTPBearer()

# =========================
# 🔐 PASSWORD HASHING
# =========================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

# =========================
# 🎫 CREATE JWT TOKEN
# =========================
def create_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

# =========================
# 👤 GET CURRENT USER (HTTPBEARER VERSION)
# =========================
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
):

    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=401,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        numero_nomina = payload.get("nomina")

        if not numero_nomina:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    db = SessionLocal()
    try:
        user = db.query(Colaborador).filter(
            Colaborador.numero_nomina == numero_nomina
        ).first()
    finally:
        db.close()

    if not user:
        raise credentials_exception

    return user

# =========================
# 🛡️ VALIDAR ROLES
# =========================
def require_roles(roles: list):

    def role_checker(user: Colaborador = Depends(get_current_user)):

        if user.rol not in roles:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos"
            )

        return user

    return role_checker