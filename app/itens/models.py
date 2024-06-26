from sqlalchemy import Column, BigInteger, String, DateTime, Double
from database.instance import Base

class ItensCategoriasModel(Base):

    __tablename__ = "ITENS_CATEGORIAS"

    id = Column(BigInteger, primary_key=True, index=True)
    nome = Column(String)


class ItensSubCategoriasModel(Base):

    __tablename__ = "ITENS_SUBCATEGORIAS"

    id = Column(BigInteger, primary_key=True, index=True)
    nome = Column(String)
    categoriaID = Column(BigInteger)


class ItensMarcasModel(Base):

    __tablename__ = "ITENS_MARCAS"

    id = Column(BigInteger, primary_key=True, index=True)
    nome = Column(String)


class ItensModel(Base):

    __tablename__ = "ITENS"

    id = Column(BigInteger, primary_key=True, index=True)
    nome = Column(String)
    descricao = Column(String)
    categoriaID = Column(BigInteger)
    subcategoriaID = Column(BigInteger)
    marcaID = Column(BigInteger)


