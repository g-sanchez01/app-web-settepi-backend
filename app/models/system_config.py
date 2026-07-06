from sqlalchemy import Column, Integer, String
from app.config.database import Base

class SystemConfig(Base):
    __tablename__ = "system_config"

    id = Column(Integer, primary_key=True)
    key_name = Column(String, unique=True, index=True)
    value = Column(String)