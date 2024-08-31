from pydantic import BaseModel

class ItensCategoriasSchema(BaseModel):

    id: int
    nome: str

    class Config:
        orm_mode = True
        from_attributes = True


class ItensSubCategoriasSchema(BaseModel):

    id: int
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

    class Config:
        orm_mode = True
        from_attributes = True        

class ItensUnidadesSchema(BaseModel):

    id: int
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

    class Config:
        orm_mode = True
        from_attributes = True