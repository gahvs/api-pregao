from sqlalchemy import Column, BigInteger, String
from database.instance import Base

class UserModel(Base):

    __tablename__  = "USUARIOS"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String)
    nome = Column(String)


class CompradoresModel(Base):

    __tablename__ = "COMPRADORES"

    id = Column(BigInteger, primary_key=True, index=True)
    nome = Column(String)
    cpf = Column(String)
    usuarioID = Column(BigInteger)


class FornecedoresModel(Base):

    __tablename__ = "FORNECEDORES"

    id = Column(BigInteger, primary_key=True, index=True)
    nomeEmpresa = Column(String)
    cnpj = Column(String)
    usuarioID = Column(BigInteger)


class CompradoresInteressesModel(Base):

    __tablename__ = "COMPRADORES_INTERESSES"

    id = Column(BigInteger, primary_key=True, index=True)
    compradorID = Column(BigInteger)
    categoriaID = Column(BigInteger)


class FornecedoresInteressesModel(Base):

    __tablename__ = "FORNECEDORES_INTERESSES"

    id = Column(BigInteger, primary_key=True, index=True)
    fornecedorID = Column(BigInteger)
    categoriaID = Column(BigInteger)
