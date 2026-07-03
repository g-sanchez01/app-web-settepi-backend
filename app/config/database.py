# ================================
# 📦 IMPORTS DE SQLALCHEMY
# ================================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ================================
# 🔗 CONFIGURACIÓN DE CONEXIÓN A BD PROD
# ================================
#DATABASE_URL = (
#    "mssql+pyodbc://settepi_userPROD:S33TT3P1MTY_2026@localhost/SettepiDB_PROD"
#    "?driver=ODBC+Driver+17+for+SQL+Server"
#)

# ================================
# 🔗 CONFIGURACIÓN DE CONEXIÓN A BD QA
# ================================
DATABASE_URL = (
    "mssql+pyodbc://settepi_userDEV:s3tt3p02026@localhost/SettepiDB_DEV"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

# Engine: conecta la app con la base de datos
engine = create_engine(DATABASE_URL)

# ================================
# 🧠 SESIONES (QUERY / INSERT / UPDATE / DELETE)
# ================================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ================================
# 🧱 BASE PARA MODELOS ORM
# ================================
Base = declarative_base()

# ================================
# 🔌 DEPENDENCY FASTAPI (OBLIGATORIO)
# ================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()