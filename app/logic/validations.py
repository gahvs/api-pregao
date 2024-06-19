from sqlalchemy.orm import Session
from . import user 
from . import pregao

class UserValidation:
    @classmethod
    def user_exists(cls, db: Session, user_id: int) -> bool:
        return user.get_user(db=db, user_id=user_id) is not None

class PregaoValidation:
    @classmethod
    def pregao_exists(cls, db: Session, pregao_id: int) -> bool:
        return pregao.get_pregao(db=db, pregao_id=pregao_id) is not None