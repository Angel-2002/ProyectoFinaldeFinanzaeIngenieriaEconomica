from fastapi import APIRouter, HTTPException, status
from config.db_dependency import db_dependency
import bcrypt
#Importar las clases
from models.company import Company
from schemas.company import CompanyD

company=APIRouter()

@company.post("/company", status_code=status.HTTP_201_CREATED, tags=["Company"])
async def crear_company(company:Company, db:db_dependency):
    db_company = CompanyD(**company.dict())
    # Hasheo de la contraseña
    psswrd = company.password
    hash = psswrd.encode('utf-8')
    sal = bcrypt.gensalt()
    encript = bcrypt.hashpw(hash,sal)

    # Convertir bytes a string
    db_company.password = encript.decode('utf-8')

    db.add(db_company)
    db.commit()

    return {"message": "Company successfully created"}

@company.get("/company/{id_company}", status_code=status.HTTP_200_OK, tags=["Company"])
async def consultar_companyID(id_company: int, db:db_dependency):
    company = db.query(CompanyD).filter(CompanyD.id == id_company).first()

    if company is None:
        raise HTTPException(status_code=404, detail="Company had not found")
    
    return company

@company.get("/company/{id_company}", status_code=status.HTTP_200_OK, tags=["Company"])
async def consultar_companyID(id_company: int, db:db_dependency):
    company = db.query(CompanyD).filter(CompanyD.id == id_company).first()

    if company is None:
        raise HTTPException(status_code=404, detail="Company had not found")
    
    return company

@company.get("/company/{RUC}/{password}", status_code=status.HTTP_200_OK, tags=["Company"])
async def consultar_usuarioRUCpsswrd(RUC:str, password:str, db:db_dependency):

    company = db.query(CompanyD).filter(CompanyD.ruc == RUC).first()
    
    if company is None:
        raise HTTPException(status_code=404, detail="${password}")
    
    if not bcrypt.checkpw(password.encode('utf-8'), company.password.encode('utf-8')):
        return False

    return True