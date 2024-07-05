from pydantic import BaseModel
from typing import List


class CompradorCreateSchema(BaseModel):

    nome: str
    cpf: str
    usuarioID: int

    class Config:
        orm_mode = True
        from_attributes = True


class CompradorResponseSchema(BaseModel):

    id: int
    nome: str
    cpf: str
    usuarioID: int

    class Config:
        orm_mode = True
        from_attributes = True


class CompradorInteresseResponseSchema(BaseModel):

    id: int
    nome: str
    cpf: str
    usuarioID: int
    categoriaInteresse: str

    class Config:
        orm_mode = True
        from_attributes = True


class FornecedorCreateSchema(BaseModel):

    nomeEmpresa: str
    cnpj: str
    usuarioID: int

    class Config:
        orm_mode = True
        from_attributes = True
        

class FornecedorResponseSchema(BaseModel):

    id: int
    nomeEmpresa: str
    cnpj: str
    usuarioID: int

    class Config:
        orm_mode = True
        from_attributes = True


class FornecedorInteresseResponseSchema(BaseModel):

    id: int
    nomeEmpresa: str
    cnpj: str
    usuarioID: int
    categoriaInteresse: str

    class Config:
        orm_mode = True
        from_attributes = True
