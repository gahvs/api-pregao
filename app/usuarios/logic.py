from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.instance import get_db
from itens.logic import ItensCategoriaLogic
from itens.models import ItensCategoriasModel
from utils import errors
from typing import Union, List
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

    def usuario_has_comprador_profile(self, usuario_id: int) -> bool:

        comprador: models.CompradoresModel = self.db.query(models.CompradoresModel).filter(
            models.CompradoresModel.usuarioID == usuario_id
        ).first()

        return comprador != None


    def interesse_already_setted(self, comprador_id: int, categoria_id: int) -> bool:

        interesse: models.CompradoresInteressesModel = self.db.query(models.CompradoresInteressesModel).filter(
            models.CompradoresInteressesModel.compradorID == comprador_id,
            models.CompradoresInteressesModel.categoriaID == categoria_id
        ).first()

        return interesse != None


    def get_comprador_by_id(self, comprador_id: int) -> models.CompradoresModel | HTTPException:

        comprador: models.CompradoresModel = self.db.query(models.CompradoresModel).filter(
            models.CompradoresModel.id == comprador_id
        ).first()

        if comprador == None:
            raise HTTPException(status_code=404, detail=f"Não foi encontrador Comprador com o ID {comprador_id}")

        return comprador
    

    def get_comprador_by_usuario_id(self, usuario_id: int) -> models.CompradoresModel | HTTPException:

        comprador: models.CompradoresModel = self.db.query(models.CompradoresModel).filter(
            models.CompradoresModel.usuarioID == usuario_id
        ).first()

        if comprador == None:
            raise HTTPException(status_code=404, detail=f"Não existe Perfil Comprador para o Usuário {usuario_id}")

        return comprador
    

    def create_comprador(self, body: schemas.CompradorCreateSchema) -> models.CompradoresModel | HTTPException:

        if self.usuario_has_comprador_profile(body.usuarioID):
            raise HTTPException(status_code=409, detail=f"Usuário {body.usuarioID} já possui perfil Comprador") 

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
    

    def set_comprador_interesse(self, 
            comprador_id: int, 
            categoria_id: int
        ) -> Union[models.CompradoresInteressesModel, ItensCategoriasModel] | HTTPException:
    
        if self.interesse_already_setted(comprador_id=comprador_id, categoria_id=categoria_id):
            raise HTTPException(status_code=409, detail=f"Interesse na Categoria {categoria_id} já definido para o Comprador {comprador_id}")

        comprador: models.CompradoresModel = self.get_comprador_by_id(comprador_id=comprador_id)
        categoria: ItensCategoriasModel = self.itens_categoria_logic.get_categoria_by_id(categoria_id=categoria_id)

        interesse: models.CompradoresInteressesModel = models.CompradoresInteressesModel(
            compradorID=comprador.id,
            categoriaID=categoria.id
        )

        self.db.add(interesse)
        self.db.commit()
        self.db.refresh(interesse)

        return comprador, categoria
    

    def get_comprador_interesses(self, comprador_id: int) -> List[ItensCategoriasModel] | HTTPException:
        
        comprador: models.CompradoresModel = self.get_comprador_by_id(comprador_id=comprador_id)

        interesses: List[models.CompradoresInteressesModel] = self.db.query(models.CompradoresInteressesModel).filter(
            models.CompradoresInteressesModel.compradorID == comprador.id
        ).all()

        if interesses == []:
            raise HTTPException(status_code=204, detail=f"Comprador {comprador.id} não possui interesses registrados")
        
        categorias: List[ItensCategoriasModel] = list(
            map(lambda interesse: self.itens_categoria_logic.get_categoria_by_id(categoria_id=interesse.categoriaID), interesses)
        )

        return categorias



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
        

    def usuario_has_fornecedor_profile(self, usuario_id: int) -> bool:
        fornecedor: models.FornecedoresModel = self.db.query(models.FornecedoresModel).filter(
            models.FornecedoresModel.usuarioID == usuario_id
        ).first()
        
        return fornecedor != None


    def interesse_already_setted(self, fornecedor_id: int, categoria_id: int) -> bool:

        interesse: models.FornecedoresInteressesModel = self.db.query(models.FornecedoresInteressesModel).filter(
            models.FornecedoresInteressesModel.fornecedorID == fornecedor_id,
            models.FornecedoresInteressesModel.categoriaID == categoria_id
        ).first()

        return interesse != None


    def get_fornecedor_by_id(self, fornecedor_id: int) -> models.FornecedoresModel | HTTPException:

        fornecedor: models.FornecedoresModel = self.db.query(models.FornecedoresModel).filter(
            models.FornecedoresModel.id == fornecedor_id
        ).first()

        if fornecedor is None:
            raise HTTPException(status_code=404, detail=f"Não foi encontrado Fornecedor com o ID {fornecedor_id}")
        
        return fornecedor
    

    def get_fornecedor_by_usuario_id(self, usuario_id: int) -> models.FornecedoresModel | HTTPException:

        fornecedor: models.FornecedoresModel = self.db.query(models.FornecedoresModel).filter(
            models.FornecedoresModel.usuarioID == usuario_id
        ).first()

        if fornecedor == None:
            raise HTTPException(status_code=404, detail=f"Não existe Perfil Comprador para o Usuário {usuario_id}")

        return fornecedor

    def create_fornecedor(self, body: schemas.FornecedorCreateSchema) -> models.FornecedoresModel | HTTPException:

        if self.usuario_has_fornecedor_profile(usuario_id=body.usuarioID):
            raise HTTPException(status_code=409, detail=f"Usuário {body.usuarioID} já possui perfil Fornecedor")

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
    
    
    def set_fornecedor_interesse(self, 
            fornecedor_id: int, 
            categoria_id: int,
        ) -> Union[models.FornecedoresModel, ItensCategoriasModel] | HTTPException:
        
        if self.interesse_already_setted(fornecedor_id=fornecedor_id, categoria_id=categoria_id):
            raise HTTPException(status_code=409, detail=f"Interesse na categoria {categoria_id} já definido para o Fornecedor {fornecedor_id}")

        fornecedor: models.FornecedoresModel = self.get_fornecedor_by_id(fornecedor_id=fornecedor_id)
        categoria: ItensCategoriasModel = self.itens_categoria_logic.get_categoria_by_id(categoria_id=categoria_id)


        interesse: models.FornecedoresInteressesModel = models.FornecedoresInteressesModel(
            fornecedorID=fornecedor.id,
            categoriaID=categoria.id
        )

        self.db.add(interesse)
        self.db.commit()
        self.db.refresh(interesse)

        return fornecedor, categoria
    

    def get_fornecedor_interesses(self, fornecedor_id: int) -> List[ItensCategoriasModel] | HTTPException:

        fornecedor: models.FornecedoresModel = self.get_fornecedor_by_id(fornecedor_id=fornecedor_id)
        interesses: List[models.FornecedoresInteressesModel] = self.db.query(models.FornecedoresInteressesModel).filter(
            models.FornecedoresInteressesModel.fornecedorID == fornecedor.id
        ).all()

        if interesses == []:
            raise HTTPException(status_code=204, detail=f"O Fornecedor {fornecedor.id} não possui interesses definidos")
        
        categorias: List[ItensCategoriasModel] = list(map(
            lambda interesse: self.itens_categoria_logic.get_categoria_by_id(categoria_id=interesse.categoriaID), interesses
        ))

        return categorias