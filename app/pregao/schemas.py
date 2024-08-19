from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
from utils import errors

class PregaoSchema(BaseModel):

    id: int
    descricao: str
    informacoes: str
    status: str
    criadoPor: int
    criadoEm: datetime
    atualizadoEm: datetime
    dataHoraInicio: datetime
    dataHoraFim: datetime
    abertoADemandasEm: datetime
    abertoADemandasAte: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class PregaoCreateSchema(BaseModel):

    descricao: str
    informacoes: str
    usuarioID: int
    dataHoraInicio: str
    dataHoraFim: str
    abertoADemandasEm: str
    abertoADemandasAte: str
    solicitacoes: Optional[List[int]] = Field(default=[])

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


class PregaoItensSchema(BaseModel):

    criadoPor: int
    itemID: int
    unidade: str
    quantidade: float

    class Config:
        orm_mode = True
        from_attributes = True


class PregaoItensUpdateQuantidadeSchema(BaseModel):

    quantidade: float

    class Config:
        orm_mode = True
        from_attributes = True


class PregaoItensResponseSchema(BaseModel):

    id: int
    pregaoID: int
    criadoPor: int
    itemID: int
    unidade: str
    quantidade: float
    criadoEm: datetime 

    class Config:
        orm_mode = True
        from_attributes = True


class PregaoCompradoresBodySchema(BaseModel):

    compradorID: int

    class Config:
        orm_mode = True
        from_attributes = True


class PregaoCompradoresResponseSchema(BaseModel):

    id: int
    solicitacaoID: int
    compradorID: int

    class Config:
        orm_mode = True
        from_attributes = True


class PregaoFornecedoresResponseSchema(BaseModel):

    id: int
    solicitacaoID: int
    fornecedorID: int
        
    class Config:
        orm_mode = True
        from_attributes = True


class PregaoFornecedoresBodySchema(BaseModel):

    fornecedorID: int

    class Config:
        orm_mode = True
        from_attributes = True        