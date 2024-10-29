from pydantic import BaseModel
from typing import Optional

class Client(BaseModel):
    ruc_company : str
    ruc : str
    direccion : str
    nombre : Optional[str]    
    apellido : Optional[str]
    nombre_comercial : Optional[str]
    razon_social : Optional[str]
    rol : str