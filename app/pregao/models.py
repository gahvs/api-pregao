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

class PregaoParticipantesModel(Base):

    __tablename__ = "PREGAO_PREGOES_PARTICIPANTES"

    id = Column(BigInteger, primary_key=True, index=True)
    pregaoID = Column(BigInteger)
    usuarioID = Column(BigInteger)
    tipoParticipante = Column(String)


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