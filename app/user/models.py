from sqlalchemy import Column, BigInteger, String
from database.instance import Base

class UserModel(Base):

    __tablename__  = "USUARIOS"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String)
    nome = Column(String)