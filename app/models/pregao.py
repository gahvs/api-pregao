from sqlalchemy import Column, BigInteger, String, DateTime, Double
from database.instance import Base
from datetime import datetime

class PregaoModel(Base):

    __tablename__  = "PREGAO"

    id = Column(BigInteger, primary_key=True, index=True)
    descricao = Column(String)
    status = Column(String, index=True, default="PENDENTE")
    criadoPor = Column(BigInteger)
    criadoEm = Column(DateTime, default=datetime.now().isoformat())
    dataHoraInicio = Column(DateTime)
    dataHoraFim = Column(DateTime)

class PregaoParticipantesModel(Base):

    __tablename__ = "PREGAO_PARTICIPANTES"

    id = Column(BigInteger, primary_key=True, index=True)
    pregaoID = Column(BigInteger)
    usuarioID = Column(BigInteger)
    tipoParticipante = Column(String)

class PregaoProdutosModel(Base):

    __tablename__ = "PREGAO_PRODUTOS"

    id = Column(BigInteger, primary_key=True, index=True)
    demandanteID = Column(BigInteger)
    descricao = Column(String)
    unidade = Column(String)
    criadoEm = Column(DateTime, default=datetime.now().isoformat())

class PregaoDemandasModel(Base):

    __tablename__ = "PREGAO_DEMANDAS"
    
    id = Column(BigInteger, primary_key=True, index=True)
    pregaoID = Column(BigInteger)
    demandanteID = Column(BigInteger)
    produtoID = Column(BigInteger)
    demanda = Column(Double)
    criadoEm = Column(DateTime, default=datetime.now().isoformat())