from fastapi import APIRouter, Depends
from typing import List
from . import logic
from . import schemas

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.post("/{usuario_id}/interesses/compra", response_model=schemas.UsuarioInteresseResponseSchema)
def create_interesse_compra(usuario_id: int, body: schemas.UsuarioInteresseBodySchema, logic: logic.UsuarioInteresses = Depends()):
    interesse_compra = logic.create_interesse_compra(usuario_id=usuario_id, body=body)
    return schemas.UsuarioInteresseResponseSchema.model_validate(interesse_compra)

@router.post("/{usuario_id}/interesses/venda", response_model=schemas.UsuarioInteresseResponseSchema)
def create_interesse_compra(usuario_id: int, body: schemas.UsuarioInteresseBodySchema, logic: logic.UsuarioInteresses = Depends()):
    interesse_venda = logic.create_interesse_venda(usuario_id=usuario_id, body=body)
    return schemas.UsuarioInteresseResponseSchema.model_validate(interesse_venda)

@router.get("/{usuario_id}/interesses", response_model=List[schemas.UsuarioInteresseResponseSchema])
def get_interesses_compra(usuario_id: int, logic: logic.UsuarioInteresses = Depends()):
    interesses = logic.get_usuario_interesses(usuario_id=usuario_id)
    return map(lambda i: schemas.UsuarioInteresseResponseSchema.model_validate(i), interesses)
