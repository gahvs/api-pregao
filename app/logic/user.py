from sqlalchemy.orm import Session
from models.user import UserModel

def get_user(db: Session, user_id: int) -> UserModel:
    return db.query(UserModel).filter(UserModel.id == user_id).first()
