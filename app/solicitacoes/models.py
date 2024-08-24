from sqlalchemy import Column, BigInteger, String, DateTime, Double, Boolean, func
from database.instance import Base

class SolicitacoesModel(Base):

    __tablename__ = "PREGAO_SOLICITACOES"

    id = Column(BigInteger, primary_key=True, index=True)
    descricao = Column(String)
    informacoes = Column(String)
    status = Column(String)
    dataHoraInicioSugerida = Column(DateTime)
    dataHoraFimSugerida = Column(DateTime)
    criadoPor = Column(BigInteger)
    motivoRejeicao = Column(String)
    criadoEm = Column(DateTime, default=func.now())
    atualizadoEm = Column(DateTime, default=func.now(), onupdate=func.now())

class SolicitacoesItensModel(Base):

    __tablename__ = "PREGAO_SOLICITACOES_ITENS"

    id = Column(BigInteger, primary_key=True, index=True)
    solicitacaoID = Column(BigInteger)
    itemID = Column(BigInteger)
    criadoPor = Column(BigInteger)
    unidade = Column(String)
    projecaoQuantidade = Column(Double)
    criadoEm = Column(DateTime, default=func.now())
    atualizadoEm = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False)


class SolicitacoesParticipantesModel(Base):

    __tablename__ = "PREGAO_SOLICITACOES_PARTICIPANTES"

    id = Column(BigInteger, primary_key=True, index=True)
    solicitacaoID = Column(BigInteger)
    usuarioID = Column(BigInteger)
    participanteTipo = Column(String)