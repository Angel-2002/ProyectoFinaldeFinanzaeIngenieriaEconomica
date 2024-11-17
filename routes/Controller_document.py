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

    sstatus="pendiente"

    # Comparar la fecha de vencimiento con la fecha actual
    if fecha_vencimiento < datetime.now():
        sstatus = "vencido"
        db_document.estado = sstatus

    db_document.fecha_emision = fecha_emision
    db_document.fecha_vencimiento = fecha_vencimiento
    

    # Consulta la cartera asociado
    wallet = db.query(WalletD).filter(WalletD.id == db_document.id_cartera).first()

    # Actualizamos el estado pagado de la cartera a pendiente, si la nueva factura o letra tiene estado pendiente o vencido
    if (db_document.estado == "pendiente") or (db_document.estado == "vencido"):
        sstatus="pendiente"
        wallet.estado = sstatus 

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
    listDocument = db.query(DocumentD).filter(DocumentD.id_cartera==db_document.id_cartera).all()

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

@document.get("/documents/{id_cartera}", status_code=status.HTTP_200_OK, tags=["Document"])
async def consultar_documentos(id_cartera: int, db:db_dependency):
    listDocument = db.query(DocumentD).filter(DocumentD.id_cartera==id_cartera).all()

    if not listDocument:
        raise HTTPException(status_code=404, detail="Documents had not found")

    return listDocument


@document.put("/documents/{id}/{estado}", status_code=status.HTTP_200_OK, tags=["Document"])
async def actualizar_documento(id: int, estado: str, db: db_dependency):
    # Consulta el documento por ID
    docmento = db.query(DocumentD).filter(DocumentD.id == id).first()
    
    # Verifica si el documento existe
    if not docmento:
        raise HTTPException(status_code=404, detail="Document not found")

    # Actualiza el estado del documento
    docmento.estado = estado

    # Consulta la cartera asociado
    wallet = db.query(WalletD).filter(WalletD.id == docmento.id_cartera).first()

    listDocument = db.query(DocumentD).filter(DocumentD.id_cartera==docmento.id_cartera).all()

    statusWallet = "pagado"

    for aux in listDocument:
        if (aux.estado == "pendiente") or (aux.estado == "vencido"):
           statusWallet="pendiente"

    wallet.estado = statusWallet

    # Guarda los cambios en la base de datos
    db.add(wallet)
    db.add(docmento)
    db.commit()
    db.refresh(wallet)
    db.refresh(docmento)  # Refresca la instancia para obtener los valores actualizados

    # Retorna el documento actualizado directamente
    return docmento

