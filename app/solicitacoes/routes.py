from fastapi import APIRouter, Depends
from typing import List
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