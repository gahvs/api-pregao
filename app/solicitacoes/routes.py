from fastapi import APIRouter, Depends, Response
from typing import List
from http import HTTPStatus
from . import logic
from . import schemas

router = APIRouter(
    prefix="/solicitacoes",
    tags=["Solicitacoes"]
)

@router.get("/{solicitacao_id}", response_model=schemas.SolicitacoesResponseSchema)
def get_solicitacao_by_id(solicitacao_id: int, logic: logic.SolicitacaoLogic = Depends()):
    solicitacao = logic.get_solicitacao_by_id(solicitacao_id=solicitacao_id)
    return schemas.SolicitacoesResponseSchema.model_validate(solicitacao)


@router.post("/nova", response_model=schemas.SolicitacoesResponseSchema)
def create_solicitacao(body: schemas.SolicitacoesBodySchema, logic: logic.SolicitacaoLogic = Depends()):
    solicitacao = logic.create_solicitacao(body=body)
    return schemas.SolicitacoesResponseSchema.model_validate(solicitacao)


@router.post("/{solicitacao_id}/aprovar", response_model=schemas.SolicitacoesResponseSchema)
def approve_solicitacao(solicitacao_id: int, logic: logic.SolicitacaoLogic = Depends()):
    solicitacao = logic.approve_solicitacao(solicitacao_id=solicitacao_id)
    return schemas.SolicitacoesResponseSchema.model_validate(solicitacao)


@router.post("/{solicitacao_id}/rejeitar", response_model=schemas.SolicitacoesResponseSchema)
def approve_solicitacao(solicitacao_id: int, body: schemas.SolicitacoesRejeicaoBodySchema, logic: logic.SolicitacaoLogic = Depends()):
    solicitacao = logic.reject_solicitacao(solicitacao_id=solicitacao_id, body=body)
    return schemas.SolicitacoesResponseSchema.model_validate(solicitacao)


@router.post("/{solicitacao_id}/itens/adicionar", response_model=schemas.SolicitacoesItensResponseSchema)
def create_solicitacao_item(solicitacao_id: int, body: schemas.SolicitacoesItensBodySchema, logic: logic.SolicitacaoItensLogic = Depends()):
    item = logic.create_solicitacao_item(solicitacao_id=solicitacao_id, body=body)
    return schemas.SolicitacoesItensResponseSchema.model_validate(item)

@router.get("/{solicitacao_id}/itens", response_model=List[schemas.SolicitacoesItensResponseSchema])
def get_solicitacao_itens(solicitacao_id: int, logic: logic.SolicitacaoItensLogic = Depends()):
    itens = logic.get_solicitacao_itens(solicitacao_id=solicitacao_id)
    return list(map(lambda i: schemas.SolicitacoesItensResponseSchema.model_validate(i), itens))

@router.post("/{solicitacao_id}/compradores", response_model=schemas.SolicitacoesCompradoresResponseSchema)
def create_solicitacao_comprador(solicitacao_id: int, body: schemas.SolicitacoesCompradoresBodySchema, logic: logic.SolicitacaoCompradoresLogic = Depends()):
    comprador = logic.create_solicitacao_comprador(solicitacao_id=solicitacao_id, body=body)
    return schemas.SolicitacoesCompradoresResponseSchema.model_validate(comprador)

@router.get("/{solicitacao_id}/compradores", response_model=List[schemas.SolicitacoesCompradoresResponseSchema])
def get_solicitacao_compradores(solicitacao_id:int, logic: logic.SolicitacaoCompradoresLogic = Depends()):
    compradores = logic.get_compradores_by_solicitacao(solicitacao_id=solicitacao_id)
    return list(map(lambda c: schemas.SolicitacoesCompradoresResponseSchema.model_validate(c), compradores))

@router.delete("/compradores/{solicitacao_comprador_id}")
def delete_solicitacao_comprador(solicitacao_comprador_id: int, logic: logic.SolicitacaoCompradoresLogic = Depends()):
    logic.remove_solicitacao_comprador(solicitacao_comprador_id=solicitacao_comprador_id)
    return Response(status_code=HTTPStatus.NO_CONTENT)

@router.post("/{solicitacao_id}/fornecedores", response_model=schemas.SolicitacoesFornecedoresResponseSchema)
def create_solicitacao_fornecedor(solicitacao_id: int, body: schemas.SolicitacoesFornecedoresBodySchema, logic: logic.SolicitacaoFornecedoresLogic = Depends()):
    fornecedor = logic.create_solicitacao_fornecedor(solicitacao_id=solicitacao_id, body=body)
    return schemas.SolicitacoesFornecedoresResponseSchema.model_validate(fornecedor)

@router.get("/{solicitacao_id}/fornecedores", response_model=List[schemas.SolicitacoesFornecedoresResponseSchema])
def get_solicitacao_forncedores(solicitacao_id:int, logic: logic.SolicitacaoFornecedoresLogic = Depends()):
    forncedores = logic.get_fornecedores_by_solicitacao(solicitacao_id=solicitacao_id)
    return list(map(lambda f: schemas.SolicitacoesFornecedoresResponseSchema.model_validate(f), forncedores))

@router.delete("/fornecedores/{solicitacao_fornecedor_id}")
def delete_solicitacao_fornecedor(solicitacao_fornecedor_id: int, logic: logic.SolicitacaoFornecedoresLogic = Depends()):
    logic.remove_solicitacao_fornecedor(solicitacao_fornecedor_id=solicitacao_fornecedor_id)
    return Response(status_code=HTTPStatus.NO_CONTENT)