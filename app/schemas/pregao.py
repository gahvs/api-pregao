from pydantic import BaseModel
from datetime import datetime

class PregaoSchema(BaseModel):

    id: int
    descricao: str
    status: str
    criadoPor: int
    criadoEm: datetime
    dataHoraInicio: datetime
    dataHoraFim: datetime

    class Config:
        orm_mode = True
        from_attributes = True