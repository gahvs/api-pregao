from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.instance import get_db
from itens.logic import ItensCategoriaLogic
from utils import errors
from . import models
from . import schemas


class UserLogic:
    '''
        Realiza ações que tem como contexto a tabela USUARIO
    '''

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db: Session = db


    def get_user_by_id(self, user_id: int) -> models.UserModel | HTTPException:
        user = self.db.query(models.UserModel).filter(models.UserModel.id == user_id).first()

        if user is None:
            raise HTTPException(status_code=404, detail=errors.not_found_message("USUARIO", user_id))
        
        return user
    

class UsuarioInteresses: 

    '''
        Realiza operações com as entidades USUARIOS_INTERESSES_COMPRA e USUARIOS_INTERESSES_VENDA.
        Principais operações:
        - Registro de Interesse de Compra
        - Registro de Interesse de Venda
        - Listagem de Interesses de Compra
        - Listagem dos Interesses de Venda
        - Remoção de Interesse de Compra
        - Remoção de Interesse de Venda
    '''

    INTERESSE_TIPO_COMPRA = "COMPRA"
    INTERESSE_TIPO_VENDA = "VENDA"

    def __init__(self,
                 db: Session = Depends(get_db),
                 user_logic: UserLogic = Depends(UserLogic),
                 categoria_logic: ItensCategoriaLogic = Depends(ItensCategoriaLogic)
                 ) -> None:
        
        self.db: Session = db
        self.user_logic: UserLogic = user_logic
        self.categoria_logic: ItensCategoriaLogic = categoria_logic

    def get_interesse_compra_using_usuario_categoria(self, usuario_id: int, categoria_id: int) -> models.UsuarioInteressesModel | HTTPException:

        interesse_compra = self.db.query(models.UsuarioInteressesModel).filter(
            models.UsuarioInteressesModel.usuarioID==usuario_id,
            models.UsuarioInteressesModel.categoriaID==categoria_id,
            models.UsuarioInteressesModel.interesseTipo==self.INTERESSE_TIPO_COMPRA
        ).first()

        if interesse_compra == None:
            raise HTTPException(status_code=404, detail=f"Não há interesse de compra definido para o Usuário {usuario_id} e Categoria {categoria_id}")

        return interesse_compra 


    def get_interesse_venda_using_usuario_categoria(self, usuario_id: int, categoria_id: int) -> models.UsuarioInteressesModel | HTTPException:

        interesse_compra = self.db.query(models.UsuarioInteressesModel).filter(
            models.UsuarioInteressesModel.usuarioID==usuario_id,
            models.UsuarioInteressesModel.categoriaID==categoria_id,
            models.UsuarioInteressesModel.interesseTipo==self.INTERESSE_TIPO_VENDA
        ).first()

        if interesse_compra == None:
            raise HTTPException(status_code=404, detail=f"Não há interesse de venda definido para o Usuário {usuario_id} e Categoria {categoria_id}")

        return interesse_compra 
    

    def interesse_compra_already_setted(self, usuario_id: int, categoria_id: int) -> bool:

        interesse_compra = self.db.query(models.UsuarioInteressesModel).filter(
            models.UsuarioInteressesModel.usuarioID==usuario_id,
            models.UsuarioInteressesModel.categoriaID==categoria_id,
            models.UsuarioInteressesModel.interesseTipo==self.INTERESSE_TIPO_COMPRA
        ).first()

        return interesse_compra != None
    
    
    def interesse_venda_already_setted(self, usuario_id: int, categoria_id: int) -> bool:

        interesse_compra = self.db.query(models.UsuarioInteressesModel).filter(
            models.UsuarioInteressesModel.usuarioID==usuario_id,
            models.UsuarioInteressesModel.categoriaID==categoria_id,
            models.UsuarioInteressesModel.interesseTipo==self.INTERESSE_TIPO_VENDA
        ).first()

        return interesse_compra != None
    
    def create_usuario_interesse(self, usuario_id: int, categoria_id: int, interesse_tipo: str) -> models.UsuarioInteressesModel | HTTPException:
        
        if self.interesse_compra_already_setted(usuario_id=usuario_id, categoria_id=categoria_id):
            return self.get_interesse_compra_using_usuario_categoria(usuario_id=usuario_id, categoria_id=categoria_id)

        usuario = self.user_logic.get_user_by_id(user_id=usuario_id)
        categoria = self.categoria_logic.get_categoria_by_id(categoria_id=categoria_id)

        new_interesse_compra = models.UsuarioInteressesModel(
            usuarioID=usuario.id,
            categoriaID=categoria.id,
            interesseTipo=interesse_tipo
        )

        self.db.add(new_interesse_compra)
        self.db.commit()
        self.db.refresh(new_interesse_compra)

        return new_interesse_compra

    def create_interesse_compra(self, usuario_id: int, body: schemas.UsuarioInteresseBodySchema) -> models.UsuarioInteressesModel | HTTPException:
        return self.create_usuario_interesse(usuario_id=usuario_id, categoria_id=body.categoriaID, interesse_tipo=self.INTERESSE_TIPO_COMPRA)

    def create_interesse_venda(self, usuario_id: int, body: schemas.UsuarioInteresseBodySchema) -> models.UsuarioInteressesModel | HTTPException:
        return self.create_usuario_interesse(usuario_id=usuario_id, categoria_id=body.categoriaID, interesse_tipo=self.INTERESSE_TIPO_VENDA)
    

    def get_usuario_interesses(self, usuario_id: int) -> List[models.UsuarioInteressesModel] | HTTPException:

        usuario = self.user_logic.get_user_by_id(user_id=usuario_id)

        interesses = self.db.query(models.UsuarioInteressesModel).filter(
            models.UsuarioInteressesModel.usuarioID==usuario.id
        )

        if interesses == []:
            raise HTTPException(status_code=204, detail=f"Usuário {usuario_id} não possui Interesses cadstrados")
        
        return interesses