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


@router.put("/{pregao_id}/cancelar", response_model=schemas.PregaoSchema)
def cancel_pregao(pregao_id: int, logic: logic.PregaoLogic = Depends()):
    pregao = logic.cancel_pregao(pregao_id=pregao_id)
    return schemas.PregaoSchema.model_validate(pregao)


@router.put("/{pregao_id}/autorizar", response_model=schemas.PregaoSchema)
def authorize_pregao(pregao_id: int, logic: logic.PregaoLogic = Depends()):
    pregao = logic.authorize_pregao(pregao_id=pregao_id)
    return schemas.PregaoSchema.model_validate(pregao)   


@router.put("/{pregao_id}/rejeitar", response_model=schemas.PregaoSchema)
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