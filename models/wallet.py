from pydantic import BaseModel, Field
from typing import Optional

class Wallet(BaseModel):

    nombre: str
    tipo_moneda: str
    fecha_descuento: str
    id_banco: int
    estado: Optional[str] = Field(default="pendiente")
    tcea: Optional[float] = Field(default=0.00)
    tipo_tasa: str
    periodo: str
    tasa: float
    capitalizacion: Optional[str] = Field(default="diaria")
    ruc_user: str