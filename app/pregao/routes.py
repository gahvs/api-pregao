from fastapi import APIRouter, Depends
from typing import List
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


@router.post("/{pregao_id}/fornecedor", response_model=schemas.PregaoParticipantesResponseSchema)
def create_pregao_fornecedor(pregao_id: int, body: schemas.PregaoParticipanteSchema, logic: logic.PregaoParticipanteLogic = Depends()):
    fornecedor = logic.create_fornecedor(body=body, pregao_id=pregao_id)
    return schemas.PregaoParticipantesResponseSchema.model_validate(fornecedor)


@router.post("/{pregao_id}/demandante", response_model=schemas.PregaoParticipantesResponseSchema)
def create_pregao_demandante(pregao_id: int, body: schemas.PregaoParticipanteSchema, logic: logic.PregaoParticipanteLogic = Depends()):
    demandante = logic.create_demandante(body=body, pregao_id=pregao_id)
    return schemas.PregaoParticipantesResponseSchema.model_validate(demandante)


@router.get("/{pregao_id}/participantes", response_model=List[schemas.PregaoParticipantesResponseSchema])
def get_pregao_participantes(pregao_id: int, logic: logic.PregaoParticipanteLogic = Depends()):
    participantes = logic.get_pregao_participantes(pregao_id=pregao_id)
    return list(map(lambda p: schemas.PregaoParticipantesResponseSchema.model_validate(p), participantes))


@router.post("/{pregao_id}/demanda", response_model=schemas.PregaoDemandaResponseSchema)
def create_pregao_demanda(pregao_id: int, body: schemas.PregaoDemandaSchema, logic: logic.PregaoDemandasLogic = Depends()):
    demanda = logic.create_pregao_demanda(pregao_id=pregao_id, body=body)
    return schemas.PregaoDemandaResponseSchema.model_validate(demanda)


@router.get("/{pregao_id}/demandas", response_model=List[schemas.PregaoDemandaResponseSchema])
def get_pregao_demandas(pregao_id: int, logic: logic.PregaoDemandasLogic = Depends()):
    demandas = logic.get_pregao_demandas(pregao_id=pregao_id)
    return list(map(lambda d: schemas.PregaoDemandaResponseSchema.model_validate(d), demandas))


@router.put("/demanda/{demanda_id}/alterar/quantidade", response_model=schemas.PregaoDemandaResponseSchema)
def update_demanda_quantidade(demanda_id: int, body: schemas.PregaoDemandaUpdateQuantidadeSchema, logic: logic.PregaoDemandasLogic = Depends()):
    demanda = logic.update_demanda_quantidade(demanda_id=demanda_id, body=body)
    return schemas.PregaoDemandaResponseSchema.model_validate(demanda)