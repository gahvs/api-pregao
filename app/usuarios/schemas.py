from pydantic import BaseModel
from typing import List



class UsuarioInteresseBodySchema(BaseModel):

    categoriaID: int

    class Config:
        orm_mode = True
        from_attributes = True 


class UsuarioInteresseResponseSchema(BaseModel):
    
    id: int
    usuarioID: int
    categoriaID: int
    interesseTipo: str

    class Config:
        orm_mode = True
        from_attributes = True   