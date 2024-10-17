from fastapi import Depends
from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session

#Para abrir y cerrar la base de datos
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency= Annotated[Session, Depends(get_db)]