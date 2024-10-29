from sqlalchemy import Column, Integer, String
from database import Base

class ClientD(Base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, index=True)
    ruc_company = Column(String(11), nullable=False, index=True)
    ruc = Column(String(11), nullable=False, index=True)
    direccion = Column(String(100), nullable=False, index=True)
    nombre=Column(String(50), nullable=True, index=True)
    apellido=Column(String(50), nullable=True, index=True)
    nombre_comercial=Column(String(100), nullable=True, index=True)
    razon_social = Column(String(300), nullable=True, index=True)
    rol = Column(String(100), nullable=False, index=True)