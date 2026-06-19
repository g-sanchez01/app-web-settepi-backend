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
from app.routes.lider import router as lider_router
from app.routes.admin import router as admin_router
from app.routes.ideas import router as ideas_router
from app.routes.feedback import router as feedbacks_router
from app.routes.actividades import router as actividades_router

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
# ROUTES LIDER
# ================================
app.include_router(
    lider_router
)

# ================================
# ROUTES ADMIN
# ================================
app.include_router(
    admin_router
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
# ROUTES FEEDBACK
# ================================
app.include_router(
    feedbacks_router,
    prefix="/feedbacks",
    tags=["Feedbacks"]
)

# ================================
# ROUTES ACTIVIDADES
# ================================
app.include_router(
    actividades_router,
    prefix="/actividades",
    tags=["Actividades"]
)


# ================================
# 🏠 ENDPOINT PRINCIPAL
# ================================
@app.get("/")
def root():

    return {
        "message": "Conexión exitosa 🚀"
    }