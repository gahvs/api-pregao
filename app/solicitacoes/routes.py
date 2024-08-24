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

@router.get("/{solicitacao_id}/participantes", response_model=List[schemas.SolicitacoesParticipantesResponseSchema])
def get_solicitacao_participantes(solicitacao_id: int, logic: logic.SolicitacaoParticipantesLogic = Depends()):
    participantes = logic.get_solicitacao_participantes(solicitacao_id=solicitacao_id)
    return map(lambda p: schemas.SolicitacoesParticipantesResponseSchema.model_validate(p), participantes)

@router.post("/{solicitacao_id}/comprador/novo", response_model=schemas.SolicitacoesParticipantesResponseSchema)
def create_solicitacao_comprador(solicitacao_id: int, body: schemas.SolicitacoesParticipantesBodySchema, logic: logic.SolicitacaoParticipantesLogic = Depends()):
    comprador = logic.create_solicitacao_comprador(solicitacao_id=solicitacao_id, body=body)
    return schemas.SolicitacoesParticipantesResponseSchema.model_validate(comprador)

@router.post("/{solicitacao_id}/fornecedor/novo", response_model=schemas.SolicitacoesParticipantesResponseSchema)
def create_solicitacao_fornecedor(solicitacao_id: int, body: schemas.SolicitacoesParticipantesBodySchema, logic: logic.SolicitacaoParticipantesLogic = Depends()):
    fornecedor = logic.create_solicitacao_fornecedor(solicitacao_id=solicitacao_id, body=body)
    return schemas.SolicitacoesParticipantesResponseSchema.model_validate(fornecedor)

@router.delete("/{solicitacao_id}/participante/{participante_id}")
def remove_solicitacao_participante(solicitacao_id: int, participante_id: int, logic: logic.SolicitacaoParticipantesLogic = Depends()):
    logic.remove_solicitacao_participante(solicitacao_id=solicitacao_id, solicitacao_participante_id=participante_id)
    return HTTPStatus.NO_CONTENT
