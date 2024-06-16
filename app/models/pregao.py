from sqlalchemy import Column, BigInteger, String, DateTime
from database.instance import Base

class PregaoModel(Base):

    __tablename__  = "PREGAO"

    id = Column(BigInteger, primary_key=True, index=True)
    descricao = Column(String)
    status = Column(String, index=True)
    criadoPor = Column(BigInteger)
    criadoEm = Column(DateTime)
    dataHoraInicio = Column(DateTime)
    dataHoraFim = Column(DateTime)