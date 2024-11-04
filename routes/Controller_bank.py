from fastapi import APIRouter, HTTPException, status
from config.db_dependency import db_dependency

#Importar las clases
from models.bank import Bank
from schemas.bank import BankD

bank=APIRouter()

@bank.post("/bank", status_code=status.HTTP_201_CREATED, tags=["Bank"])
async def crear_bank(bank:Bank, db:db_dependency):
    db_bank = BankD(**bank.dict())
    
    db.add(db_bank)
    db.commit()

    return {"message": "Bank successfully created"}

@bank.get("/bank/{id_bank}", status_code=status.HTTP_200_OK, tags=["Bank"])
async def consultar_bankID(id_bank: int, db:db_dependency):
    bank = db.query(BankD).filter(BankD.id == id_bank).first()

    if bank is None:
        raise HTTPException(status_code=404, detail="Bank had not found")
    
    return bank

@bank.get("/bankn/{nombre}", status_code=status.HTTP_200_OK, tags=["Bank"])
async def consultar_banknombre(nombre: str, db:db_dependency):
    bank = db.query(BankD).filter(BankD.nombre == nombre).first()

    if bank is None:
        raise HTTPException(status_code=404, detail="Bank had not found")
    
    return bank
