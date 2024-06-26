from sqlalchemy import Column, BigInteger, String, DateTime, Double, func
from database.instance import Base

class SolicitacoesModel(Base):

    __tablename__ = "PREGAO_SOLICITACOES"

    id = Column(BigInteger, primary_key=True, index=True)
    descricao = Column(String)
    status = Column(String)
    criadoPor = Column(BigInteger)
    observacao = Column(String)
    criadoEm = Column(DateTime, default=func.now())
    atualizadoEm = Column(DateTime, default=func.now(), onupdate=func.now())

class SolicitacoesItensModel(Base):

    __tablename__ = "PREGAO_SOLICITACOES_ITENS"

    id = Column(BigInteger, primary_key=True, index=True)
    solicitacaoID = Column(BigInteger)
    criadoPor = Column(BigInteger)
    descricao = Column(String)
    unidade = Column(String)
    projecaoQuantidade = Column(Double)
    criadoEm = Column(DateTime, default=func.now())
    atualizadoEm = Column(DateTime, default=func.now(), onupdate=func.now())