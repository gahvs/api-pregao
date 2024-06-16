from sqlalchemy.orm import Session
from models.pregao import PregaoModel
from schemas.pregao import PregaoSchema, PregaoCreateSchema

def get_pregao(db: Session, pregao_id: int):
    return db.query(PregaoModel).filter(PregaoModel.id == pregao_id).first()

def create_pregao(db: Session, pregao_data: PregaoCreateSchema):

    pregao = PregaoModel(**pregao_data.model_dump())

    db.add(pregao)
    db.commit()
    db.refresh(pregao)
    
    return pregao