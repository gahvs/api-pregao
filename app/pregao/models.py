from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Double, Boolean, func
from database.instance import Base


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
    projecaoQuantidade = Column(Double)
    unidadeID = Column(BigInteger)
    criadoEm = Column(DateTime, default=func.now())
    atualizadoEm = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False)


class PregaoParticipantesModel(Base):

    __tablename__ = "PREGAO_PREGOES_PARTICIPANTES"

    id = Column(BigInteger, primary_key=True, index=True)
    pregaoID = Column(BigInteger)
    usuarioID = Column(BigInteger)
    participanteTipo = Column(String)


class PregaoConversoesModel(Base):

    __tablename__ = "PREGAO_CONVERSOES"

    id = Column(BigInteger, primary_key=True, index=True)
    pregaoID = Column(BigInteger)
    solicitacaoID = Column(BigInteger)


class PregaoLancesModel(Base):

    __tablename__ = "PREGAO_PREGOES_LANCES"

    id = Column(BigInteger, primary_key=True, index=True)
    pregaoID = Column(BigInteger)
    participanteID = Column(BigInteger)
    itemID = Column(BigInteger)
    valorLance = Column(Double)
    dataHoraLance = Column(DateTime)
    dataHoraRegistro = Column(DateTime, default=func.now())


class PregaoLancesRegrasModel(Base):

    __tablename__ = "PREGAO_LANCES_REGRAS"

    id = Column(BigInteger, primary_key=True, index=True)
    ativa = Column(Boolean)
    diferencaDeValorMinima = Column(Double)
    intervaloDeTempoEmMinutos = Column(Integer)
    lancesPorIntervaloDeTempo = Column(Integer)