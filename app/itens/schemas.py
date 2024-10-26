from pydantic import BaseModel
from datetime import datetime

class ItensCategoriasSchema(BaseModel):

    id: int
    nome: str
    criadoEm: datetime
    atualizadoEm: datetime
    deleted: bool

    class Config:
        orm_mode = True
        from_attributes = True

class ItensCategoriasBodySchema(BaseModel):

    nome: str

    class Config:
        orm_mode = True
        from_attributes = True

class ItensSubCategoriasSchema(BaseModel):

    id: int
    categoriaID: int
    nome: str
    criadoEm: datetime
    atualizadoEm: datetime
    deleted: bool

    class Config:
        orm_mode = True
        from_attributes = True

class ItensSubCategoriasBodySchema(BaseModel):

    categoriaID: int
    nome: str

    class Config:
        orm_mode = True
        from_attributes = True          

class ItensMarcasBodySchema(BaseModel):

    nome: str   

    class Config:
        orm_mode = True
        from_attributes = True    
        
class ItensMarcasSchema(BaseModel):

    id: int
    nome: str
    criadoEm: datetime
    atualizadoEm: datetime
    deleted: bool

    class Config:
        orm_mode = True
        from_attributes = True        

class ItensUnidadesSchema(BaseModel):

    id: int
    unidade: str
    descricao: str
    criadoEm: datetime
    atualizadoEm: datetime
    deleted: bool

    class Config:
        orm_mode = True
        from_attributes = True

class ItensUnidadesBodySchema(BaseModel):

    unidade: str
    descricao: str

    class Config:
        orm_mode = True
        from_attributes = True
        
class ItensSchema(BaseModel):

    id: int
    nome: str
    descricao: str
    categoriaID: int
    subcategoriaID: int
    marcaID: int
    criadoEm: datetime
    atualizadoEm: datetime
    deleted: bool

    class Config:
        orm_mode = True
        from_attributes = True

class ItensBodySchema(BaseModel):

    nome: str
    descricao: str
    categoriaID: int
    subcategoriaID: int
    marcaID: int

    class Config:
        orm_mode = True
        from_attributes = True        