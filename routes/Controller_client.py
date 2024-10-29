from fastapi import APIRouter, HTTPException, status
from config.db_dependency import db_dependency
import bcrypt
#Importar las clases
from models.client import Client
from schemas.client import ClientD

client=APIRouter()

@client.post("/client", status_code=status.HTTP_201_CREATED, tags=["Client"])
async def crear_client(client:Client, db:db_dependency):
    db_client = ClientD(**client.dict())

    db.add(db_client)
    db.commit()

    return {"message": "Client successfully created"}

@client.get("/client/{id_company}/{role}", status_code=status.HTTP_200_OK, tags=["Client"])
async def consultar_clientP(id_company: int, rol: str,db:db_dependency):
    listClientP = db.query(ClientD).filter(ClientD.id == id_company, ClientD.rol == rol).all

    if not listClientP:
        raise HTTPException(status_code=404, detail="Client not found")

    return listClientP