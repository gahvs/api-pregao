from sqlalchemy import Column, BigInteger, String
from database.instance import Base

class UserModel(Base):

    __tablename__  = "USUARIOS"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String)
    nome = Column(String)

class UsuarioInteressesModel(Base):

    __tablename__ = "USUARIOS_INTERESSES"

    id = Column(BigInteger, primary_key=True, index=True)
    usuarioID = Column(BigInteger)
    categoriaID = Column(BigInteger)
    interesseTipo = Column(String)
