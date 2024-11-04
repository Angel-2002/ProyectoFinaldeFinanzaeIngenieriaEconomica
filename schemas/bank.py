from sqlalchemy import Column, Integer, String
from database import Base

class BankD(Base):
    __tablename__ = 'bank'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False, index=True)