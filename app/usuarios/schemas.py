from pydantic import BaseModel

class CompradorSchemaCreate(BaseModel):

    nome: str
    cpf: str
    usuarioID: int

    class Config:
        orm_mode = True
        from_attributes = True



class FornecedorSchemaCreate(BaseModel):

    nomeEmpresa: str
    cnpj: str
    usuarioID: int

    class Config:
        orm_mode = True
        from_attributes = True