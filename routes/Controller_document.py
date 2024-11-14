from fastapi import APIRouter, HTTPException, status
from config.db_dependency import db_dependency
from datetime import datetime
#Importar las clases
from models.document import Document
from schemas.document import DocumentD
from schemas.wallet import WalletD

document=APIRouter()

@document.post("/document", status_code=status.HTTP_201_CREATED, tags=["Document"])
async def crear_document(document:Document, db:db_dependency):
    db_document = DocumentD(**document.dict())

    # Convertir el string a un objeto datetime
    fecha_emision = datetime.strptime(document.fecha_emision, "%d/%m/%Y")
    fecha_vencimiento = datetime.strptime(document.fecha_vencimiento, "%d/%m/%Y")

    db_document.fecha_emision = fecha_emision
    db_document.fecha_vencimiento = fecha_vencimiento

    # Consulta la cartera asociado
    wallet = db.query(WalletD).filter(WalletD.id == db_document.id_cartera).first()

    plazo = (fecha_vencimiento - wallet.fecha_descuento).days
    db_document.plazo = plazo

    TEplazo=wallet.tasa
    #Calcular tasa descuento
    if (wallet.tipo_tasa=="efectiva"):
        if(wallet.periodo=="anual"):
            #Pasamos de TEAnual a TEplazo:
            TEplazo=(1+wallet.tasa)**(plazo/360)-1

        elif(wallet.periodo=="mensual"):
            #Pasamos de TEMensual a TEplazo:
            TEplazo=(1+wallet.tasa)**(plazo/30)-1
        
        else:
            #Pasamos de TEDiaria a TEplazo:
            TEplazo=(1+wallet.tasa)**(plazo/1)-1
    else:
        #TASA NOMINAL
        if(wallet.capitalizacion=="anual"):
            if(wallet.periodo=="anual"):
                #Pasamos de TNAnual a TEplazo:
                TEplazo=(1+wallet.tasa/(360/360))**(plazo/360)-1
            
            elif(wallet.periodo=="mensual"):
                #Pasamos de TNMensual a TEplazo:
                TEplazo=(1+wallet.tasa/(30/360))**(plazo/360)-1
            
            else:
                #Pasamos de TNDiaria a TEplazo:
                TEplazo=(1+wallet.tasa/(1/360))**(plazo/360)-1
        
        elif(wallet.capitalizacion=="mensual"):
            if(wallet.periodo=="anual"):
                #Pasamos de TNAnual a TEplazo:
                TEplazo=(1+wallet.tasa/(360/30))**(plazo/30)-1
            
            elif(wallet.periodo=="mensual"):
                #Pasamos de TNMensual a TEplazo:
                TEplazo=(1+wallet.tasa/(30/30))**(plazo/30)-1
            
            else:
                #Pasamos de TNDiaria a TEplazo:
                TEplazo=(1+wallet.tasa/(1/30))**(plazo/30)-1

        else:
            if(wallet.periodo=="anual"):
                #Pasamos de TNAnual a TEplazo:
                TEplazo=(1+wallet.tasa/(360))**(plazo)-1
            
            elif(wallet.periodo=="mensual"):
                #Pasamos de TNMensual a TEplazo:
                TEplazo=(1+wallet.tasa/(30))**(plazo)-1
            
            else:
                #Pasamos de TNDiaria a TEplazo:
                TEplazo=(1+wallet.tasa/(1))**(plazo)-1

    #Calcular tasa descuento
    tasa_descuento=round((TEplazo/(1+TEplazo)),4)
    db_document.tasa_descuento = tasa_descuento

    #Calculamos interes descontado
    interes_descontado = round(db_document.valor_nominal*tasa_descuento,2)
    db_document.interes_descontado = interes_descontado

    #Calulamos Monto Recibido
    monto_recibido = round(db_document.valor_nominal*(1-tasa_descuento),2)
    db_document.monto_recibido = monto_recibido

    #Calculamos TCEA
    tcea = ((db_document.valor_nominal/db_document.monto_recibido)**(360/db_document.plazo))-1

    db_document.tcea = round(tcea,4)

    #Actualizamos la TCEA de la cartera
    listDocument = db.query(DocumentD).all()

    numerador   = 0.00
    denominador = 0.00

    if not listDocument:
        numerador=db_document.tcea*db_document.valor_nominal
        denominador=db_document.valor_nominal
        
    else:
        for document in listDocument:
            numerador=numerador+document.tcea*document.valor_nominal
            denominador=denominador+document.valor_nominal

    tcea_wallet=round((numerador/denominador),4)

    wallet.tcea = tcea_wallet


    db.add(db_document)
    db.add(wallet)
    db.commit()
    db.refresh(wallet)

    return {"message": "Document successfully created"}

@document.get("/documents", status_code=status.HTTP_200_OK, tags=["Document"])
async def consultar_documentos(db:db_dependency):
    listDocument = db.query(DocumentD).all()

    if not listDocument:
        raise HTTPException(status_code=404, detail="Documents had not found")

    return listDocument
