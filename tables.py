from database import engine
#Agregar las tablas
from schemas.company import Base
from schemas.client import Base
from schemas.bank import Base
from schemas.wallet import Base
from schemas.document import Base

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)