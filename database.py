from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# URL de conexión sin especificar la base de datos
DATABASE_URL = "mysql+pymysql://uw22ckhjs0feymzy:eIJcSfdI6Qd1oPToQbPm@bmuzeq6lp8atx6sph7dm-mysql.services.clever-cloud.com:3306/"

#URL LOCAL:
#DATABASE_URL = "mysql+pymysql://root:Zota25@localhost:3306/"

# Nombre de la base de datos
DATABASE_NAME = "bmuzeq6lp8atx6sph7dm"

#Nombre de la base de datos local
#DATABASE_NAME = "cartera_finanzas"

# Crear un motor de base de datos conectado al servidor MySQL
engine = create_engine(DATABASE_URL)

# Crear la base de datos si no existe
with engine.connect() as connection:
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME};"))

# Actualizar la URL de la base de datos para incluir el nombre de la base de datos
DATABASE_URL = f"mysql+pymysql://uw22ckhjs0feymzy:eIJcSfdI6Qd1oPToQbPm@bmuzeq6lp8atx6sph7dm-mysql.services.clever-cloud.com:3306/{DATABASE_NAME}"

#Actualizar localmente la base de datos
#DATABASE_URL = f"mysql+pymysql://root:Zota25@localhost:3306/{DATABASE_NAME}"

# Crear el motor actualizado para conectarse a la base de datos específica
engine = create_engine(DATABASE_URL)

# Crear la sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()
