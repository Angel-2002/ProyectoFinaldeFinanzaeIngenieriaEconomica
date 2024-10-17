from pydantic import BaseModel

class Company(BaseModel):
    ruc: str
    razon_social: str
    direccion: str
    sector: str
    password: str