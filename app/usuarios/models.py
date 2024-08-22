from sqlalchemy import Column, BigInteger, String
from database.instance import Base

class UserModel(Base):

    __tablename__  = "USUARIOS"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String)
    nome = Column(String)


class UsuarioInteressesCompra(Base):

    __tablename__ = "USUARIOS_INTERESSES_COMPRA"

    id = Column(BigInteger, primary_key=True, index=True)
    usuarioID = Column(BigInteger)
    categoriaID = Column(BigInteger)


class UsuarioInteressesVenda(Base):

    __tablename__ = "USUARIOS_INTERESSES_VENDA"

    id = Column(BigInteger, primary_key=True, index=True)
    usuarioID = Column(BigInteger)
    categoriaID = Column(BigInteger)