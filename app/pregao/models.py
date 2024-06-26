from sqlalchemy import Column, BigInteger, String, DateTime, Double
from database.instance import Base
from datetime import datetime

class PregaoModel(Base):

    __tablename__  = "PREGAO_PREGOES"

    id = Column(BigInteger, primary_key=True, index=True)
    descricao = Column(String)
    status = Column(String, index=True, default="PENDENTE")
    criadoPor = Column(BigInteger)
    criadoEm = Column(DateTime, default=datetime.now().isoformat())
    dataHoraInicio = Column(DateTime)
    dataHoraFim = Column(DateTime)

class PregaoParticipantesModel(Base):

    __tablename__ = "PREGAO_PREGOES_PARTICIPANTES"

    id = Column(BigInteger, primary_key=True, index=True)
    pregaoID = Column(BigInteger)
    usuarioID = Column(BigInteger)
    tipoParticipante = Column(String)


class PregaoDemandasModel(Base):

    __tablename__ = "PREGAO_PREGOES_ITENS"
    
    id = Column(BigInteger, primary_key=True, index=True)
    pregaoID = Column(BigInteger)
    criadoPor = Column(BigInteger)
    descricao = Column(String)
    quantidade = Column(Double)
    unidade = Column(String)
    criadoEm = Column(DateTime, default=datetime.now().isoformat())
    criadoEm = Column(DateTime, onupdate=datetime.now().isoformat())