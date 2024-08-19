from sqlalchemy import Column, BigInteger, String, DateTime, Double, func
from database.instance import Base
from datetime import datetime

class PregaoModel(Base):

    __tablename__  = "PREGAO_PREGOES"

    id = Column(BigInteger, primary_key=True, index=True)
    descricao = Column(String)
    informacoes = Column(String)
    status = Column(String, index=True, default="PENDENTE")
    criadoPor = Column(BigInteger)
    criadoEm = Column(DateTime, default=func.now())
    atualizadoEm = Column(DateTime, default=func.now(), onupdate=func.now())
    dataHoraInicio = Column(DateTime)
    dataHoraFim = Column(DateTime)
    abertoADemandasEm = Column(DateTime)
    abertoADemandasAte = Column(DateTime)


class PregaoItensModel(Base):

    __tablename__ = "PREGAO_PREGOES_ITENS"
    
    id = Column(BigInteger, primary_key=True, index=True)
    pregaoID = Column(BigInteger)
    itemID = Column(BigInteger)
    criadoPor = Column(BigInteger)
    quantidade = Column(Double)
    unidade = Column(String)
    criadoEm = Column(DateTime, default=func.now())
    atualizadoEm = Column(DateTime, default=func.now(), onupdate=func.now())

class PregaoCompradoresModel(Base):

    __tablename__ = "PREGAO_PREGOES_COMPRADORES"

    id = Column(BigInteger, primary_key=True, index=True)
    solicitacaoID = Column(BigInteger)
    compradorID = Column(BigInteger)
    

class PregaoFornecedoresModel(Base):

    __tablename__ = "PREGAO_PREGOES_FORNECEDORES"

    id = Column(BigInteger, primary_key=True, index=True)
    solicitacaoID = Column(BigInteger)
    fornecedorID = Column(BigInteger)