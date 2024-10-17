from sqlalchemy import Column, Integer, String
from database import Base

class CompanyD(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True, index=True)
    ruc = Column(String(11), nullable=False, unique=True, index=True)
    razon_social = Column(String(300), nullable=False, index=True)
    direccion = Column(String(100), nullable=False, unique=True, index=True)
    sector = Column(String(50), nullable=False, index=True)
    password = Column(String(200), nullable=False, index=True)