from pydantic import BaseModel, field_validator
from datetime import datetime
from utils import errors

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

class PregaoCreateSchema(BaseModel):

    descricao: str
    usuarioID: int
    dataHoraInicio: str
    dataHoraFim: str

    class Config:
        orm_mode = True
        from_attributes = True

    @field_validator('dataHoraInicio', 'dataHoraFim', mode="before")
    def parse_datetime(cls, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value).isoformat()
            except ValueError:
                raise ValueError("DATETIME FORMAT INCORRECT")
            
        else:
            raise ValueError(errors.invalid_type(resource_name="dataHoraInicio | dataHoraFim",expected_type="String",received_type=type(value)))

class PregaoParticipanteSchema(BaseModel):
    
    usuarioID: int

    class Config:
        orm_mode = True
        from_attributes = True

class PregaoParticipantesResponseSchema(BaseModel):
    
    id: int
    pregaoID: int
    usuarioID: int
    tipoParticipante: str

    class Config:
        orm_mode = True
        from_attributes = True

class PregaoDemandaSchema(BaseModel):

    usuarioID: int
    descricao: str
    unidade: str
    quantidade: float

    class Config:
        orm_mode = True
        from_attributes = True
        
class PregaoDemandaResponseSchema(BaseModel):

    id: int
    pregaoID: int
    usuarioID: int
    descricao: str
    unidade: str
    quantidade: float
    criadoEm: datetime 

    class Config:
        orm_mode = True
        from_attributes = True