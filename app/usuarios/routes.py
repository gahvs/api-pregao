from fastapi import APIRouter, Depends
from typing import List
from . import logic
from . import schemas

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.get("/compradores/{comprador_id}", response_model=schemas.CompradorResponseSchema)
def get_comprador_by_id(comprador_id: int, logic: logic.CompradoresLogic = Depends()):
    comprador = logic.get_comprador_by_id(comprador_id=comprador_id)
    return schemas.CompradorResponseSchema.model_validate(comprador)


@router.get("/{usuario_id}/compradores/perfil", response_model=schemas.CompradorResponseSchema)
def get_comprador_by_usuario_id(usuario_id: int, logic: logic.CompradoresLogic = Depends()):
    comprador = logic.get_comprador_by_usuario_id(usuario_id=usuario_id)
    return schemas.CompradorResponseSchema.model_validate(comprador)


@router.post("/compradores/novo", response_model=schemas.CompradorResponseSchema)
def create_comprador(body: schemas.CompradorCreateSchema, logic: logic.CompradoresLogic = Depends()):
    comprador = logic.create_comprador(body=body)
    return schemas.CompradorResponseSchema.model_validate(comprador)


@router.post("/compradores/{comprador_id}/interesses/{categoria_id}", response_model=schemas.CompradorInteresseResponseSchema)
def create_comprador_interesse(comprador_id: int, categoria_id: int, logic: logic.CompradoresLogic = Depends()):
    comprador, categoria = logic.set_comprador_interesse(comprador_id=comprador_id, categoria_id=categoria_id)
    return schemas.CompradorInteresseResponseSchema(id=comprador.id, nome=comprador.nome, cpf=comprador.cpf, usuarioID=comprador.usuarioID, categoriaInteresse=categoria.nome)


@router.get("/compradores/{comprador_id}/interesses", response_model=List[str])
def get_comprador_interesses(comprador_id: int, logic: logic.CompradoresLogic = Depends()):
    categoriasInteresse = logic.get_comprador_interesses(comprador_id=comprador_id)
    return map(lambda categoriaInteresse: categoriaInteresse.nome, categoriasInteresse)


@router.get("/fornecedores/{fornecedor_id}", response_model=schemas.FornecedorResponseSchema)
def get_fornecedor_by_id(fornecedor_id: int, logic: logic.FornecedoresLogic = Depends()):
    fornecedor = logic.get_fornecedor_by_id(fornecedor_id=fornecedor_id)
    return schemas.FornecedorResponseSchema.model_validate(fornecedor)


@router.get("/{usuario_id}/fornecedores/perfil", response_model=schemas.FornecedorResponseSchema)
def get_fornecedor_by_usuario_id(usuario_id: int, logic: logic.FornecedoresLogic = Depends()):
    fornecedor = logic.get_fornecedor_by_usuario_id(usuario_id=usuario_id)
    return schemas.FornecedorResponseSchema.model_validate(fornecedor)


@router.post("/fornecedores/novo", response_model=schemas.FornecedorCreateSchema)
def create_fornecedor(body: schemas.FornecedorCreateSchema, logic: logic.FornecedoresLogic = Depends()):
    fornecedor = logic.create_fornecedor(body=body)
    return schemas.FornecedorResponseSchema.model_validate(fornecedor)


@router.post("/fornecedores/{fornecedor_id}/interesses/{categoria_id}", response_model=schemas.FornecedorInteresseResponseSchema)
def create_fornecedor_interesse(fornecedor_id: int, categoria_id: int, logic: logic.FornecedoresLogic = Depends()):
    fornecedor, categoria = logic.set_fornecedor_interesse(fornecedor_id=fornecedor_id, categoria_id=categoria_id)
    return schemas.FornecedorInteresseResponseSchema(id=fornecedor.id, nomeEmpresa=fornecedor.nomeEmpresa, cnpj=fornecedor.cnpj, usuarioID=fornecedor.usuarioID, categoriaInteresse=categoria.nome)


@router.get("/fornecedores/{fornecedor_id}/interesses", response_model=List[str])
def get_fornecedor_interesses(fornecedor_id: int, logic: logic.FornecedoresLogic = Depends()):
    categoriasInteresse = logic.get_fornecedor_interesses(fornecedor_id=fornecedor_id)
    return map(lambda categoriaInteresse: categoriaInteresse.nome, categoriasInteresse)