from sqlalchemy import Column, BigInteger, String, DateTime
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