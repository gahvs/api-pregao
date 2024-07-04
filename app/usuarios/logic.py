from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.instance import get_db
from itens.logic import ItensCategoriaLogic
from itens.models import ItensCategoriasModel
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
    

class CompradoresLogic:
    '''
        Realiza ações que tem como contexto a tabela COMPRADORES
    '''

    def __init__(self,
            db: Session = Depends(get_db),
            user_logic: UserLogic = Depends(UserLogic),
            itens_categoria_logic: ItensCategoriaLogic = Depends(ItensCategoriaLogic)
            ) -> None:
        
        self.db: Session = db
        self.user_logic: UserLogic = user_logic
        self.itens_categoria_logic: ItensCategoriaLogic = itens_categoria_logic


    def get_comprador_by_id(self, comprador_id: int) -> models.CompradoresModel | HTTPException:

        comprador: models.CompradoresModel = self.db.query(models.CompradoresModel).filter(
            models.CompradoresModel.id == comprador_id
        ).first()

        if comprador == None:
            raise HTTPException(status_code=404, detail=f"Não foi encontrador Comprador com o ID {comprador_id}")

        return comprador
    

    def create_comprador(self, body: schemas.CompradorSchemaCreate) -> models.CompradoresModel | HTTPException:

        usuario: models.UserModel = self.user_logic.get_user_by_id(user_id=body.usuarioID)

        comprador: models.CompradoresModel = models.CompradoresModel(
            nome=body.nome,
            cpf=body.cpf,
            usuarioID=usuario.id
        )

        self.db.add(comprador)
        self.db.commit()
        self.db.refresh(comprador)

        return comprador
    

    def set_comprador_interesse(self, comprador_id: int, categoria_id: int) -> models.CompradoresInteressesModel | HTTPException:
    
        comprador: models.CompradoresModel = self.get_comprador_by_id(comprador_id=comprador_id)
        categoria: ItensCategoriasModel = self.itens_categoria_logic.get_categoria_by_id(categoria_id=categoria_id)

        interesse: models.CompradoresInteressesModel = models.CompradoresInteressesModel(
            compradorID=comprador.id,
            categoriaID=categoria.id
        )

        self.db.add(interesse)
        self.db.commit()
        self.db.refresh(interesse)

        return interesse
    

class FornecedoresLogic:
    '''
        Realiza ações que tem como contexto a tabela FORNECEDORES
    '''

    def __init__(self,
            db: Session = Depends(get_db),
            user_logic: UserLogic = Depends(UserLogic),
            itens_categoria_logic: ItensCategoriaLogic = Depends(ItensCategoriaLogic)
            ) -> None:
        
        self.db: Session = db
        self.user_logic: UserLogic = user_logic
        self.itens_categoria_logic: ItensCategoriaLogic = itens_categoria_logic
        

    def get_fornecedor_by_id(self, fornecedor_id: int) -> models.FornecedoresModel | HTTPException:
    
        fornecedor: models.FornecedoresModel = self.db.query(models.FornecedoresModel).filter(
            models.FornecedoresModel.id == fornecedor_id
        )

        if fornecedor is None:
            raise HTTPException(status_code=404, detail=f"Não foi encontrado Fornecedor com o ID {fornecedor_id}")
        
        return fornecedor
    

    def create_fornecedor(self, body: schemas.FornecedorSchemaCreate) -> models.FornecedoresModel | HTTPException:

        usuario: models.UserModel = self.user_logic.get_user_by_id(user_id=body.usuarioID)

        fornecedor: models.FornecedoresModel = models.FornecedoresModel(
            nomeEmpresa=body.nomeEmpresa,
            cnpj=body.cnpj,
            usuarioID=usuario.id
        )

        self.db.add(fornecedor)
        self.db.commit()
        self.db.refresh(fornecedor)

        return fornecedor
    
    
    def set_fornecedor_interesse(self, fornecedor_id: int, categoria_id: int) -> models.FornecedoresInteressesModel | HTTPException:
    
        comprador: models.CompradoresModel = self.get_fornecedor_by_id(fornecedor_id=fornecedor_id)
        categoria: ItensCategoriasModel = self.itens_categoria_logic.get_categoria_by_id(categoria_id=categoria_id)

        interesse: models.FornecedoresInteressesModel = models.FornecedoresInteressesModel(
            compradorID=comprador.id,
            categoriaID=categoria.id
        )

        self.db.add(interesse)
        self.db.commit()
        self.db.refresh(interesse)

        return interesse