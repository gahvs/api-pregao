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

class SolicitacoesItensResponseSchema(BaseModel):

    id: int
    criadoPor: int
    projecaoQuantidade: float
    criadoEm: datetime
    atualizadoEm: datetime
    deleted: bool
    itemNome: str
    itemDescricao: str
    itemCategoria: str
    itemSubcategoria: str
    itemUnidade: str
    itemMarca: str
    categoriaReferenciaID: Optional[int] = Field(default=None)
    subcategoriaReferenciaID: Optional[int] = Field(default=None)
    unidadeReferenciaID: Optional[int] = Field(default=None)
    marcaReferenciaID: Optional[int] = Field(default=None)
    itemReferenciaID: Optional[int] = Field(default=None)
    
    class Config:
        orm_mode = True
        from_attributes = True

class SolicitacoesItensBodySchema(BaseModel):

    participanteID: int
    projecaoQuantidade: float
    itemNome: str
    itemDescricao: str
    itemCategoria: str
    itemSubcategoria: str
    itemUnidade: str
    itemMarca: str
    categoriaReferenciaID: Optional[int] = Field(default=None)
    subcategoriaReferenciaID: Optional[int] = Field(default=None)
    unidadeReferenciaID: Optional[int] = Field(default=None)
    marcaReferenciaID: Optional[int] = Field(default=None)
    itemReferenciaID: Optional[int] = Field(default=None)
    
    class Config:
        orm_mode = True
        from_attributes = True

class SolicitacoesItensReferenciasSchema(BaseModel):
    
    categoriaReferenciaID: Optional[int] = Field(default=None)
    subcategoriaReferenciaID: Optional[int] = Field(default=None)
    unidadeReferenciaID: Optional[int] = Field(default=None)
    marcaReferenciaID: Optional[int] = Field(default=None)
    itemReferenciaID: Optional[int] = Field(default=None)
    
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