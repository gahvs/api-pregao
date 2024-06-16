from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.instance import get_db
from logic import pregao as pregao_logic
from schemas.pregao import PregaoSchema
from utils.functions import not_found_message

router = APIRouter(
    prefix="/pregao",
    tags=["PREGAO"]
)

@router.get("/{pregao_id}", response_model=PregaoSchema)
def get_pregao(pregao_id: int, db: Session = Depends(get_db)):
    pregao = pregao_logic.get_pregao(db, pregao_id)

    if pregao is None:
        raise HTTPException(status_code=404, detail=not_found_message("PREGAO", pregao_id))
    
    return PregaoSchema.model_validate(pregao)    
