from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker, declarative_base

password = quote_plus("admin2026$")

# ================================
# 🔗 CONFIGURACIÓN DE CONEXIÓN A BD PROD
# ================================
DATABASE_URL = (
   f"mssql+pyodbc://adminsql:{password}"
   "@databasesettepiapp.database.windows.net:1433/SettepiApp"
   "?driver=ODBC+Driver+18+for+SQL+Server"
   "&Encrypt=yes"
   "&TrustServerCertificate=no"
)

# # ================================
# # 🔗 CONFIGURACIÓN DE CONEXIÓN A BD QA
# # ================================
# DATABASE_URL = (
#     "mssql+pyodbc://settepi_userDEV:s3tt3p02026@localhost/SettepiDB_DEV"
#     "?driver=ODBC+Driver+17+for+SQL+Server"
# )

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