from pydantic import BaseModel, field_validator
from datetime import datetime
from utils import error_functions

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
    criadoPor: int
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
            raise ValueError(error_functions.invalid_type(resource_name="dataHoraInicio | dataHoraFim",expected_type="String",received_type=type(value)))
        