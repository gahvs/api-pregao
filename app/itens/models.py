from sqlalchemy import Column, BigInteger, String, DateTime, Double, Boolean, func
from database.instance import Base

class ItensCategoriasModel(Base):

    __tablename__ = "ITENS_CATEGORIAS"

    id = Column(BigInteger, primary_key=True, index=True)
    nome = Column(String)
    criadoEm = Column(DateTime, default=func.now())
    atualizadoEm = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False)


class ItensSubCategoriasModel(Base):

    __tablename__ = "ITENS_SUBCATEGORIAS"

    id = Column(BigInteger, primary_key=True, index=True)
    nome = Column(String)
    categoriaID = Column(BigInteger)
    criadoEm = Column(DateTime, default=func.now())
    atualizadoEm = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False)


class ItensMarcasModel(Base):

    __tablename__ = "ITENS_MARCAS"

    id = Column(BigInteger, primary_key=True, index=True)
    nome = Column(String)
    criadoEm = Column(DateTime, default=func.now())
    atualizadoEm = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False)


class ItensUnidadesModel(Base):

    __tablename__ = "ITENS_UNIDADES"

    id = Column(BigInteger, primary_key=True, index=True)
    unidade = Column(String)
    descricao = Column(String)
    criadoEm = Column(DateTime, default=func.now())
    atualizadoEm = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False)
    

class ItensModel(Base):

    __tablename__ = "ITENS"

    id = Column(BigInteger, primary_key=True, index=True)
    nome = Column(String)
    descricao = Column(String)
    categoriaID = Column(BigInteger)
    subcategoriaID = Column(BigInteger)
    marcaID = Column(BigInteger)
    criadoEm = Column(DateTime, default=func.now())
    atualizadoEm = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False)


