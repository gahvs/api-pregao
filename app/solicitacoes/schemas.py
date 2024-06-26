from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SolicitacoesBodySchema(BaseModel):

    descricao: str
    informacoes: str
    dataHoraInicioSugerida: Optional[str] = Field(default=None)
    dataHoraFimSugerida: Optional[str] = Field(default=None)
    criadoPor: int
    
    class Config:
        orm_mode = True
        from_attributes = True

class SolicitacoesRejeicaoBodySchema(BaseModel):

    motivoRejeicao: str
    
    class Config:
        orm_mode = True
        from_attributes = True

class SolicitacoesResponseSchema(BaseModel):

    id: int
    descricao: str
    informacoes: str
    dataHoraInicioSugerida: Optional[datetime] = Field(default=None)
    dataHoraFimSugerida: Optional[datetime] = Field(default=None)
    criadoPor: int
    status: str
    motivoRejeicao: str
    criadoEm: datetime
    atualizadoEm: datetime
    
    class Config:
        orm_mode = True
        from_attributes = True

class SolicitacoesItensBodySchema(BaseModel):

    solicitacaoID: int
    descricao: str
    unidade: str
    projecaoQuantidade: float
        
    class Config:
        orm_mode = True
        from_attributes = True

class SolicitacoesItensResponseSchema(BaseModel):

    solicitacaoID: int
    criadoPor: int
    descricao: str
    unidade: str
    projecaoQuantidade: float
    criadoEm: datetime
    atualizadoEm: datetime

    class Config:
        orm_mode = True
        from_attributes = True