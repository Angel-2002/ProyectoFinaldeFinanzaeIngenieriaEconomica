from fastapi import APIRouter, HTTPException, status
from config.db_dependency import db_dependency
from datetime import datetime
#Importar las clases
from models.wallet import Wallet
from schemas.wallet import WalletD
from schemas.bank import BankD

wallet=APIRouter()

@wallet.post("/wallet", status_code=status.HTTP_201_CREATED, tags=["Wallet"])
async def crear_wallet(wallet:Wallet, db:db_dependency):
    db_wallet = WalletD(**wallet.dict())

    # Convertir el string a un objeto datetime
    fecha_descuento = datetime.strptime(wallet.fecha_descuento, "%d/%m/%Y")

    db_wallet.fecha_descuento = fecha_descuento

    db.add(db_wallet)
    db.commit()

    return {"message": "Wallet successfully created"}

@wallet.get("/wallet/{id}", status_code=status.HTTP_200_OK, tags=["Wallet"])
async def consultar_cartera(id: int, db:db_dependency):
    cartera = db.query(WalletD).filter(WalletD.id == id).all()

    if not cartera:
        raise HTTPException(status_code=404, detail="Wallet had not found")

    return cartera

@wallet.get("/walletr/{ruc_user}", status_code=status.HTTP_200_OK, tags=["Wallet"])
async def consultar_cartera(ruc_user: str, db:db_dependency):
    listCartera = db.query(WalletD).filter(WalletD.ruc_user == ruc_user).all()
    for cartera in listCartera:
        # Consulta el banco asociado y asigna el nombre al atributo `nombre_banco`
        banco = db.query(BankD).filter(BankD.id == cartera.id_banco).first()
        if banco:
            cartera.nombre_banco = banco.nombre

    if not listCartera:
        raise HTTPException(status_code=404, detail="Wallets had not found")

    return listCartera