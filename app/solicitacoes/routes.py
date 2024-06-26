from fastapi import APIRouter, Body, Depends
from typing import List
from . import logic
from . import schemas

router = APIRouter(
    prefix="/solicitacoes",
    tags=["SOLICITACOES"]
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


@router.post("/itens/adicionar", response_model=schemas.SolicitacoesItensResponseSchema)
def create_solicitacao_item(body: schemas.SolicitacoesItensBodySchema, logic: logic.SolicitacaoItensLogic = Depends()):
    item = logic.create_solicitacao_item(body=body)
    return schemas.SolicitacoesItensResponseSchema.model_validate(item)

# TODO:
# ALTERAR ENDPOINT DE CRIACAO DE PREGAO: RECEBER NO BODY AS SOLICITACOES QUE DEVEM VIRAR PREGAO, ALEM DE CAMPOS PERTINENTES
# REMOVER STAUTS DESNECESSARIOS DO PREGAO