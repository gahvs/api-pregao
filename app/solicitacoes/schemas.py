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

    itemID: int
    unidade: str
    projecaoQuantidade: float
    participanteID: int
        
    class Config:
        orm_mode = True
        from_attributes = True

class SolicitacoesItensBodyUpdateSchema(BaseModel):

    unidade: Optional[str] = None
    projecaoQuantidade: Optional[float] = None
        
    class Config:
        orm_mode = True
        from_attributes = True        

class SolicitacoesItensResponseSchema(BaseModel):

    id: int
    solicitacaoID: int
    criadoPor: int
    itemID: int
    unidade: str
    projecaoQuantidade: float
    criadoEm: datetime
    atualizadoEm: datetime
    deleted: bool

    class Config:
        orm_mode = True
        from_attributes = True

class SolicitacoesParticipantesBodySchema(BaseModel):

    usuarioID: int

    
    class Config:
        orm_mode = True
        from_attributes = True

class SolicitacoesParticipantesResponseSchema(BaseModel):

    id: int
    solicitacaoID: int
    usuarioID: int
    participanteTipo: str

    class Config:
        orm_mode = True
        from_attributes = True