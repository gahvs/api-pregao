from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.instance import get_db
from utils.error_functions import not_found_message
import logic.user as user_logic
import logic.pregao as logic
import schemas.pregao as schemas 

router = APIRouter(
    prefix="/pregao",
    tags=["PREGAO"]
)

@router.get("/{pregao_id}", response_model=schemas.PregaoSchema)
def get_pregao(pregao_id: int, db: Session = Depends(get_db)):
    pregao = logic.get_pregao(db, pregao_id)

    if pregao is None:
        raise HTTPException(status_code=404, detail=not_found_message("PREGAO", pregao_id))
    
    return schemas.PregaoSchema.model_validate(pregao)    

@router.post("/novo", response_model=schemas.PregaoSchema)
def create_pregao(pregao_data: schemas.PregaoCreateSchema, db: Session = Depends(get_db)):
    created_pregao = logic.create_pregao(db, pregao_data)

    if create_pregao is None:
        raise HTTPException(status_code=400, detail="")
    
    return schemas.PregaoSchema.model_validate(created_pregao)

@router.post("/{pregao_id}/cancel", response_model=schemas.PregaoSchema)
def cancel_pregao(pregao_id: int, db: Session = Depends(get_db)):
    pregao = logic.set_pregao_as_canceled(db, pregao_id=pregao_id)
    
    if pregao is None:
        raise HTTPException(status_code=404, detail=not_found_message("PREGAO", pregao_id))
    
    return schemas.PregaoSchema.model_validate(pregao)


@router.post("{pregao_id}/authorize", response_model=schemas.PregaoSchema)
def authorize_pregao(pregao_id: int, db: Session = Depends(get_db)):
    pregao = logic.set_pregao_as_authorized(db, pregao_id=pregao_id)
    
    if pregao is None:
        raise HTTPException(status_code=404, detail=not_found_message("PREGAO", pregao_id))
    
    return schemas.PregaoSchema.model_validate(pregao)   

@router.post("{pregao_id}/reject", response_model=schemas.PregaoSchema)
def reject_pregao(pregao_id: int, db: Session = Depends(get_db)):
    pregao = logic.set_pregao_as_rejected(db, pregao_id=pregao_id)
    
    if pregao is None:
        raise HTTPException(status_code=404, detail=not_found_message("PREGAO", pregao_id))
    
    return schemas.PregaoSchema.model_validate(pregao)


@router.post("/{pregao_id}/fornecedor", response_model=schemas.PregaoParticipantesResponseSchema)
def create_pregao_fornecedor(pregao_id: int, body: schemas.PregaParticipanteSchema, db: Session = Depends(get_db)):
    pregao = logic.get_pregao(db, pregao_id)
    usuario = user_logic.get_user(db, body.usuarioId)

    if pregao is None:
        raise HTTPException(status_code=404, detail=not_found_message("PREGAO", pregao_id))

    if usuario is None:
        raise HTTPException(status_code=404, detail=not_found_message("USUARIO", ))

    fornecedor = logic.create_pregao_fornecedor(db, pregao_id, body.usuarioId)
    return schemas.PregaoParticipantesResponseSchema.model_validate(fornecedor)

@router.post("/{pregao_id}/demandante", response_model=schemas.PregaoParticipantesResponseSchema)
def create_pregao_demandante(pregao_id: int, body: schemas.PregaParticipanteSchema, db: Session = Depends(get_db)):
    pregao = logic.get_pregao(db, pregao_id)
    usuario = user_logic.get_user(db, body.usuarioId)

    if pregao is None:
        raise HTTPException(status_code=404, detail=not_found_message("PREGAO", pregao_id))

    if usuario is None:
        raise HTTPException(status_code=404, detail=not_found_message("USUARIO", body.usuarioId))

    demandante = logic.create_pregao_demandante(db, pregao_id, body.usuarioId)
    return schemas.PregaoParticipantesResponseSchema.model_validate(demandante)