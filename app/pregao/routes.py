from fastapi import APIRouter, Depends, Response
from typing import List
from http import HTTPStatus
from . import logic
from . import schemas

router = APIRouter(
    prefix="/pregoes",
    tags=["Pregao"]
)

@router.get("/{pregao_id}", response_model=schemas.PregaoSchema)
def get_pregao(pregao_id: int, logic: logic.PregaoLogic = Depends()):
    pregao = logic.get_pregao_by_id(pregao_id=pregao_id)
    return schemas.PregaoSchema.model_validate(pregao)    


@router.post("/novo", response_model=schemas.PregaoSchema)
def create_pregao(body: schemas.PregaoCreateSchema, logic: logic.PregaoLogic = Depends()):
    pregao = logic.create_pregao(body=body)
    return schemas.PregaoSchema.model_validate(pregao)

@router.post("/converter", response_model=schemas.PregaoSchema)
def create_pregao_por_conversao(body: schemas.PregaoCreateSchema, logic: logic.PregaoConversoesLogic = Depends()):
    pregao = logic.criar_pregao_por_conversao(body=body)
    return schemas.PregaoSchema.model_validate(pregao)

@router.patch("/{pregao_id}/cancelar", response_model=schemas.PregaoSchema)
def cancel_pregao(pregao_id: int, logic: logic.PregaoLogic = Depends()):
    pregao = logic.cancel_pregao(pregao_id=pregao_id)
    return schemas.PregaoSchema.model_validate(pregao)


@router.patch("/{pregao_id}/autorizar", response_model=schemas.PregaoSchema)
def authorize_pregao(pregao_id: int, logic: logic.PregaoLogic = Depends()):
    pregao = logic.authorize_pregao(pregao_id=pregao_id)
    return schemas.PregaoSchema.model_validate(pregao)   


@router.patch("/{pregao_id}/rejeitar", response_model=schemas.PregaoSchema)
def reject_pregao(pregao_id: int,  logic: logic.PregaoLogic = Depends()):
    pregao = logic.reject_pregao(pregao_id=pregao_id)
    return schemas.PregaoSchema.model_validate(pregao)

@router.get("/{pregao_id}/participantes", response_model=List[schemas.PregaoParticipanteResponseSchema])
def get_pregao_participantes(pregao_id: int, logic: logic.PregaoParticipantesLogic = Depends()):
    participantes = logic.get_pregao_participantes(pregao_id=pregao_id)
    return map(lambda p: schemas.PregaoParticipanteResponseSchema.model_validate(p), participantes)

@router.post("/{pregao_id}/comprador/novo", response_model=schemas.PregaoParticipanteResponseSchema)
def create_pregao_comprador(pregao_id: int, body: schemas.PregaoParticipanteBodySchema, logic: logic.PregaoParticipantesLogic = Depends()):
    comprador = logic.create_pregao_participante_comprador(pregao_id=pregao_id, body=body)
    return schemas.PregaoParticipanteResponseSchema.model_validate(comprador)

@router.post("/{pregao_id}/fornecedor/novo", response_model=schemas.PregaoParticipanteResponseSchema)
def create_pregao_fornecedor(pregao_id: int, body: schemas.PregaoParticipanteBodySchema, logic: logic.PregaoParticipantesLogic = Depends()):
    fornecedor = logic.create_pregao_participante_fornecedor(pregao_id=pregao_id, body=body)
    return schemas.PregaoParticipanteResponseSchema.model_validate(fornecedor)

@router.post("/{pregao_id}/itens/adicionar", response_model=schemas.PregaoItensResponseSchema)
def create_pregao_item(pregao_id: int, body: schemas.PregaoItensBodySchema, logic: logic.PregaoItensLogic = Depends()):
    pregao_item = logic.create_pregao_item(pregao_id=pregao_id, body=body)
    return schemas.PregaoItensResponseSchema.model_validate(pregao_item)

@router.patch("/itens/{pregao_item_id}/alterar", response_model=schemas.PregaoItensResponseSchema)
def update_pregao_item(pregao_item_id: int, body: schemas.PregaoItensBodyUpdateSchema, logic: logic.PregaoItensLogic = Depends()):
    pregao_item = logic.update_pregao_item(pregao_item_id=pregao_item_id, body=body)
    return schemas.PregaoItensResponseSchema.model_validate(pregao_item)

@router.delete("/itens/{pregao_item_id}/", response_model=schemas.PregaoItensResponseSchema)
def delete_pregao_item(pregao_item_id: int, logic: logic.PregaoItensLogic = Depends()):
    pregao_item = logic.delete_pregao_item(pregao_item_id=pregao_item_id)
    return schemas.PregaoItensResponseSchema.model_validate(pregao_item)

@router.get("/{pregao_id}/itens", response_model=List[schemas.PregaoItensResponseSchema])
def get_pregao_itens(pregao_id: int, logic: logic.PregaoItensLogic = Depends()):
    itens = logic.get_pregao_itens(pregao_id=pregao_id)
    return map(lambda i: schemas.PregaoItensResponseSchema.model_validate(i), itens)

@router.post("/{pregao_id}/lances/registrar", response_model=schemas.PregaoLancesResponseSchema)
def create_pregao_lance(pregao_id: int, body: schemas.PregaoLancesBodySchema, logic: logic.PregaoLancesLogic = Depends()):
    pregao_lance = logic.create_pregao_lance(pregao_id=pregao_id, body=body)
    return schemas.PregaoLancesResponseSchema.model_validate(pregao_lance)

@router.get("/{pregao_id}/lances", response_model=List[schemas.PregaoLancesResponseSchema])
def get_pregao_lances(pregao_id: int, logic: logic.PregaoLancesLogic = Depends()):
    pregao_lances = logic.get_pregao_lances(pregao_id=pregao_id)
    return map(lambda l: schemas.PregaoLancesResponseSchema.model_validate(l), pregao_lances)

@router.get("/{pregao_id}/lances/vencedor", response_model=schemas.PregaoLancesResponseSchema)
def get_pregao_lance_vencedor(pregao_id: int, logic: logic.PregaoLancesLogic = Depends()):
    pregao_lance_vencedor = logic.get_pregao_lance_vencedor(pregao_id=pregao_id)
    return schemas.PregaoLancesResponseSchema.model_validate(pregao_lance_vencedor)

@router.post("/lances/regras/nova", response_model=schemas.PregaoRegrasLancesResponseSchema)
def create_regra_lances(body: schemas.PregaoRegrasLanceBodySchema, logic: logic.PregaoRegrasLancesLogic = Depends()):
    regra = logic.create_regra_lances(body=body)
    return schemas.PregaoRegrasLancesResponseSchema.model_validate(regra)

@router.get("/lances/regras", response_model=List[schemas.PregaoRegrasLancesResponseSchema])
def get_all_regras_lances(logic: logic.PregaoRegrasLancesLogic = Depends()):
    regras = logic.get_all_regras_lances()
    return map(lambda r : schemas.PregaoRegrasLancesResponseSchema.model_validate(r), regras)

@router.get("/lances/regras/{regra_id}", response_model=schemas.PregaoRegrasLancesResponseSchema)
def get_regra_lance(regra_id: int, logic: logic.PregaoRegrasLancesLogic = Depends()):
    regra = logic.get_regra_lances_by_id(regra_id=regra_id)
    return schemas.PregaoRegrasLancesResponseSchema.model_validate(regra)