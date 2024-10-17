from database import engine
from schemas.company import Base

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)