from pydantic import BaseModel
from datetime import datetime

class SolicitacoesBodySchema(BaseModel):

    descricao: str
    criadoPor: int
    
    class Config:
        orm_mode = True
        from_attributes = True

class SolicitacoesResponseSchema(BaseModel):

    id: int
    descricao: str
    criadoPor: int
    status: str
    observacao: str
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