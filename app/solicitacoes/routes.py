from fastapi import APIRouter, Depends
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

@router.post("/itens/adicionar", response_model=schemas.SolicitacoesItensResponseSchema)
def create_solicitacao_item(body: schemas.SolicitacoesItensBodySchema, logic: logic.SolicitacaoItensLogic = Depends()):
    item = logic.create_solicitacao_item(body=body)
    return schemas.SolicitacoesItensResponseSchema.model_validate(item)

# TODO:
# DEFINIR ESTADOS DAS SOLICITACOES
# ADICIONAR MUDANÇA DE ESTADO NAS SOLICITACOES
# MELHORAR ESQUEMA DA OBSERVACAO (DEIXAR PARA USUARIO E CRIAR UM MOTIVO REJEICAO)
# CRIAR CAMPO NA SOLICITACAO QUE MOSTRE QUE FOI VINCULADA A UM PREGAO
# ALTERAR ENDPOINT DE CRIACAO DE PREGAO: RECEBER NO BODY AS SOLICITACOES QUE DEVEM VIRAR PREGAO, ALEM DE CAMPOS PERTINENTES
# REMOVER STAUTS DESNECESSARIOS DO PREGAO