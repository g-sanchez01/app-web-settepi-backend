# ================================
# 📦 IMPORTS FASTAPI + BD
# ================================
from fastapi import FastAPI

from app.config.database import engine, Base

# modelos
from app.models.colaborador import Colaborador

# routers
from app.routes.auth import router as auth_router
from app.routes.general import router as general_router
from app.routes.ideas import router as ideas_router

# middleware
from fastapi.middleware.cors import CORSMiddleware

# ================================
# 🚀 CREACIÓN DE LA APP
# ================================
app = FastAPI()

# ================================
# 🌍 CORS
# ================================
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
# CREAR TABLAS EN BD
# (si no existen)
# ================================
Base.metadata.create_all(bind=engine)

# ================================
# ROUTES AUTH
# ================================
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)

# ================================
# ROUTES GENERAL
# ================================
app.include_router(
    general_router,
    tags=["General"]
)

# ================================
# ROUTES IDEAS
# ================================
app.include_router(
    ideas_router,
    prefix="/ideas",
    tags=["Ideas"]
)

# ================================
# 🏠 ENDPOINT PRINCIPAL
# ================================
@app.get("/")
def root():

    return {
        "message": "Conexión exitosa 🚀"
    }