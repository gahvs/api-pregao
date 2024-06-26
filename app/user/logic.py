from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.instance import get_db
from . import models
from utils import errors


class UserLogic:
    '''
        Realiza ações que tem como contexto a tabela PREGAO
    '''

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db: Session = db


    def get_user_by_id(self, user_id: int) -> models.UserModel | HTTPException:
        user = self.db.query(models.UserModel).filter(models.UserModel.id == user_id).first()

        if user is None:
            raise HTTPException(status_code=404, detail=errors.not_found_message("USUARIO", user_id))
        
        return user