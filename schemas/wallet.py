from sqlalchemy import Column, Integer, String, Float,DateTime
from database import Base

class WalletD(Base):
    __tablename__ = 'wallet'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False, index=True)
    tipo_moneda = Column(String(200), nullable=False, index=True)
    fecha_descuento = Column(DateTime, nullable=False, index=True)
    id_banco=Column(Integer, nullable=False, index=True)
    estado=Column(String(200), nullable=True, index=True)
    tcea = Column(Float, nullable=True, index=True)
    tipo_tasa = Column(String(200), nullable=False, index=True)
    periodo = Column(String(200), nullable=False, index=True)
    tasa = Column(Float, nullable=False, index=True)
    capitalizacion = Column(String(200), nullable=False, index=True)
    ruc_user = Column(String(200), nullable=False, index=True)
