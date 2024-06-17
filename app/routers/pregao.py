from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.instance import get_db
from utils.error_functions import not_found_message
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

@router.post("/{pregao_id}/participants", response_model=schemas.PregaoParticipantsResponseSchema)
def set_participants(pregao_id: int, pregao_data: schemas.PregaoParticipantsSchema, db: Session = Depends(get_db)):
    
    pregao = logic.get_pregao(db, pregao_id)
    if pregao is None:
        raise HTTPException(status_code=404, detail=not_found_message("PREGAO", pregao_id))


    participants = logic.create_pregao_participants(db, pregao_id=pregao_id, participants=pregao_data.demandantes)

    pregao_dict = schemas.PregaoSchema.model_validate(pregao).model_dump()
    pregao_dict['demandantes'] = list(map(lambda participants: participants.demandanteID, participants))
    pregao_schema = schemas.PregaoParticipantsResponseSchema(**pregao_dict)

    return pregao_schema
