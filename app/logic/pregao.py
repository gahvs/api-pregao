from sqlalchemy.orm import Session
from models.pregao import PregaoModel

def get_pregao(db: Session, pregao_id: int):
    return db.query(PregaoModel).filter(PregaoModel.id == pregao_id).first()