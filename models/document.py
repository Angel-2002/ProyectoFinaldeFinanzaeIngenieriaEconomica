from pydantic import BaseModel, Field
from typing import Optional

class Document(BaseModel):

    id_cartera: int
    tipo: str
    valor_nominal: float
    tipo_tasa: str
    periodo: str
    capitalizacion: Optional[str]
    fecha_emision: str
    fecha_vencimiento: str
    ruc_cliente: str
    estado: Optional[str] = Field(default="pendiente")
