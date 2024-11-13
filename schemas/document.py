from sqlalchemy import Column, Integer, String, Float,DateTime
from database import Base

class DocumentD(Base):
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True, index=True)
    id_cartera = Column(Integer, nullable=False, index=True)
    tipo = Column(String(200), nullable=False, index=True)
    valor_nominal=Column(Float, nullable=False, index=True)
    tipo_tasa = Column(String(200), nullable=False, index=True)
    periodo = Column(String(200), nullable=False, index=True)
    capitalizacion = Column(String(200), nullable=True, index=True)
    fecha_emision = Column(DateTime, nullable=False, index=True)
    fecha_vencimiento = Column(DateTime, nullable=False, index=True)
    ruc_cliente=Column(String(11), nullable=False, index=True)
    estado = Column(String(200), nullable=False, index=True)

    monto_recibido = Column(Float, nullable=True, index=True)
    plazo = Column(Integer, nullable=True, index=True)
    tasa_descuento = Column(Float, nullable=True, index=True)
    interes_descontado = Column(Float, nullable=True, index=True)
