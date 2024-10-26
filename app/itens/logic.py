from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from database.instance import get_db
from typing import List
from utils.http_exceptions import NoContentException, ResourceNotFoundException, ResourceExpectationFailedException
from . import models, schemas

class ItensCategoriaLogic:
    '''
        Realiza ações que tem como contexto a tabela ITENS_CATEGORIAS
    '''

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db: Session = db


    def get_categoria_by_id(self, categoria_id: int) -> models.ItensCategoriasModel | HTTPException:

        categoria: models.ItensCategoriasModel = self.db.query(models.ItensCategoriasModel).filter(
            models.ItensCategoriasModel.id == categoria_id
        ).first()

        if categoria is None:
            raise ResourceNotFoundException()
        
        return categoria

    def get_all_categorias(self) -> List[models.ItensCategoriasModel] | HTTPException:

        categorias: List[models.ItensCategoriasModel] = self.db.query(models.ItensCategoriasModel).filter(
            models.ItensCategoriasModel.deleted==False
        ).order_by(models.ItensCategoriasModel.id).all()

        if categorias == []:
            raise NoContentException()

        return categorias
    
    def create_categoria(self, body: schemas.ItensCategoriasBodySchema) -> models.ItensCategoriasModel:

        new_categoria: models.ItensCategoriasModel = models.ItensCategoriasModel(
            nome=body.nome
        )

        self.db.add(new_categoria)
        self.db.commit()
        self.db.refresh(new_categoria)

        return new_categoria

    def update_categoria(self, categoria_id: int, body: schemas.ItensCategoriasBodySchema) -> models.ItensCategoriasModel:

        categoria: models.ItensCategoriasModel = self.get_categoria_by_id(categoria_id=categoria_id)

        categoria.nome = body.nome
        
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)

        return categoria

    def delete_categoria(self, categoria_id: int) -> models.ItensCategoriasModel | HTTPException:

        categoria: models.ItensCategoriasModel = self.get_categoria_by_id(categoria_id=categoria_id)

        if categoria.deleted:
            return categoria

        categoria.deleted = True

        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        
        return categoria
    

class ItensSubCategoriaLogic:
    '''
        Realiza ações que tem como contexto a tabela ITENS_SUBCATEGORIAS
    '''    

    def __init__(self, 
                 db: Session = Depends(get_db),
                 categoria_logic: ItensCategoriaLogic = Depends(ItensCategoriaLogic)
            ) -> None:
        
        self.db: Session = db
        self.categoria_logic = categoria_logic


    def get_sub_categoria_by_id(self, subcategoria_id: int) -> models.ItensSubCategoriasModel | HTTPException:

        subcategoria: models.ItensSubCategoriasModel = self.db.query(models.ItensSubCategoriasModel).filter(
            models.ItensSubCategoriasModel.id == subcategoria_id
        ).first()

        if subcategoria is None:
            raise ResourceNotFoundException()
        
        return subcategoria


    def get_all_subcategorias(self) -> List[models.ItensSubCategoriasModel] | HTTPException:

        subcategorias: List[models.ItensSubCategoriasModel] = self.db.query(models.ItensSubCategoriasModel).filter(
            models.ItensSubCategoriasModel.deleted==False
        ).order_by(models.ItensSubCategoriasModel.id).all()

        if subcategorias == []:
            raise NoContentException()

        return subcategorias
    

    def get_subcategorias_by_categoria(self, categoria_id: int) -> List[models.ItensSubCategoriasModel] | HTTPException:

        categoria: models.ItensCategoriasModel = self.categoria_logic.get_categoria_by_id(categoria_id=categoria_id)
        
        subcategorias: List[models.ItensSubCategoriasModel] = self.db.query(models.ItensSubCategoriasModel).filter(
            models.ItensSubCategoriasModel.categoriaID == categoria.id,
            models.ItensSubCategoriasModel.deleted==False
        ).all()

        
        if subcategorias == []:
            raise NoContentException()

        return subcategorias    


    def create_subcategoria(self, body: schemas.ItensSubCategoriasBodySchema) -> models.ItensSubCategoriasModel | HTTPException:

        categoria: models.ItensCategoriasModel = self.categoria_logic.get_categoria_by_id(categoria_id=body.categoriaID)

        new_subcategoria = models.ItensSubCategoriasModel(
            categoriaID=categoria.id,
            nome=body.nome
        )

        self.db.add(new_subcategoria)
        self.db.commit()
        self.db.refresh(new_subcategoria)

        return new_subcategoria
    

    def update_subcategoria(self, subcategoria_id: int, body: schemas.ItensSubCategoriasBodySchema) -> models.ItensSubCategoriasModel | HTTPException:

        categoria: models.ItensCategoriasModel = self.categoria_logic.get_categoria_by_id(categoria_id=body.categoriaID)
        subcategoria: models.ItensSubCategoriasModel = self.get_sub_categoria_by_id(subcategoria_id=subcategoria_id)

        subcategoria.nome = body.nome
        subcategoria.categoriaID = categoria.id

        self.db.add(subcategoria)
        self.db.commit()
        self.db.refresh(subcategoria)

        return subcategoria
    

    def delete_subcategoria(self, subcategoria_id: int) -> models.ItensSubCategoriasModel | HTTPException:

        subcategoria: models.ItensSubCategoriasModel = self.get_sub_categoria_by_id(subcategoria_id=subcategoria_id)

        if subcategoria.deleted:
            return subcategoria
        
        subcategoria.deleted = True

        self.db.add(subcategoria)
        self.db.commit()
        self.db.refresh(subcategoria)

        return subcategoria


class ItensMarcasLogic:
    '''
        Realiza ações que tem como contexto a tabela ITENS_MARCAS
    '''    

    def __init__(self, 
                 db: Session = Depends(get_db),
                 categoria_logic: ItensCategoriaLogic = Depends(ItensCategoriaLogic),
                 subcategoria_logic: ItensSubCategoriaLogic = Depends(ItensSubCategoriaLogic)
            ) -> None:
        
        self.db: Session = db
        self.categoria_logic = categoria_logic
        self.subcategoria_logic = subcategoria_logic


    def get_marca_by_id(self, marca_id: int) -> models.ItensMarcasModel | HTTPException:

        marca: models.ItensMarcasModel = self.db.query(models.ItensMarcasModel).filter(
            models.ItensMarcasModel.id == marca_id
        ).first()

        if marca is None:
            raise ResourceNotFoundException()

        return marca
    
    def get_all_marcas(self) -> List[models.ItensMarcasModel] | HTTPException:

        marcas: List[models.ItensMarcasModel] = self.db.query(models.ItensMarcasModel).filter(
            models.ItensMarcasModel.deleted==False
        ).order_by(models.ItensMarcasModel.id).all()

        if marcas == []:
            raise NoContentException()

        return marcas
    
    def create_marca(self, body: schemas.ItensMarcasBodySchema) -> models.ItensMarcasModel:

        new_marca = models.ItensMarcasModel(nome=body.nome)

        self.db.add(new_marca)
        self.db.commit()
        self.db.refresh(new_marca)

        return new_marca
    
    def update_marca(self, marca_id: int, body: schemas.ItensMarcasBodySchema) -> models.ItensMarcasModel:

        marca: models.ItensMarcasModel = self.get_marca_by_id(marca_id=marca_id)

        marca.nome = body.nome

        self.db.add(marca)
        self.db.commit()
        self.db.refresh(marca)

        return marca    
    
    def delete_marca(self, marca_id: int) -> models.ItensMarcasModel | HTTPException:
        
        marca: models.ItensMarcasModel = self.get_marca_by_id(marca_id=marca_id)

        if marca.deleted:
            return marca
        
        marca.deleted = True

        self.db.add(marca)
        self.db.commit()
        self.db.refresh(marca)

        return marca


class ItensUnidadesLogic: 

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db: Session = db

    def get_unidade_by_id(self, unidade_id: int) -> models.ItensUnidadesModel | HTTPException:
        
        unidade = self.db.query(models.ItensUnidadesModel).filter(
            models.ItensUnidadesModel.id==unidade_id
        ).first()

        if unidade == None:
            raise ResourceNotFoundException()

        return unidade
    
    def get_all_unidades(self) -> List[models.ItensUnidadesModel] | HTTPException:

        unidades = self.db.query(models.ItensUnidadesModel).filter(
            models.ItensUnidadesModel.deleted==False
        ).order_by(models.ItensUnidadesModel.id).all()

        if unidades == []:
            raise NoContentException()
        
        return unidades
    
    def create_unidade(self, body: schemas.ItensUnidadesBodySchema) -> models.ItensUnidadesModel | HTTPException:

        if len(body.unidade) > 3:
            raise ResourceExpectationFailedException()
        
        new_unidade: models.ItensUnidadesModel = models.ItensUnidadesModel(
            unidade=body.unidade,
            descricao=body.descricao
        )

        self.db.add(new_unidade)
        self.db.commit()
        self.db.refresh(new_unidade)

        return new_unidade
    
    def update_unidade(self, unidade_id: int, body: schemas.ItensUnidadesBodySchema) -> models.ItensUnidadesModel | HTTPException:

        if len(body.unidade) > 3:
            raise ResourceExpectationFailedException()
        
        unidade: models.ItensUnidadesModel = self.get_unidade_by_id(unidade_id=unidade_id)

        unidade.unidade = body.unidade
        unidade.descricao = body.descricao

        self.db.add(unidade)
        self.db.commit()
        self.db.refresh(unidade)

        return unidade    

    def delete_unidade(self, unidade_id: int) -> models.ItensUnidadesModel | HTTPException:

        unidade: models.ItensUnidadesModel = self.get_unidade_by_id(unidade_id=unidade_id)

        if unidade.deleted:
            return unidade
        
        unidade.deleted = True

        self.db.add(unidade)
        self.db.commit()
        self.db.refresh(unidade)

        return unidade


class ItensLogic:
    '''
        Realiza ações que tem como contexto a tabela ITENS
    '''

    def __init__(self, 
                 db: Session = Depends(get_db),
                 categorias_logic: ItensCategoriaLogic = Depends(ItensCategoriaLogic),
                 subcategorias_logic: ItensSubCategoriaLogic = Depends(ItensSubCategoriaLogic),
                 marcas_logic: ItensMarcasLogic = Depends(ItensMarcasLogic)
            ) -> None:
        self.db: Session = db
        self.categorias_logic: ItensCategoriaLogic = categorias_logic
        self.subcategorias_logic: ItensSubCategoriaLogic = subcategorias_logic
        self.marcas_logic: ItensMarcasLogic = marcas_logic

    def get_item_by_id(self, item_id: int) -> models.ItensModel | HTTPException:

        item: models.ItensModel = self.db.query(models.ItensModel).filter(
            models.ItensModel.id == item_id
        ).first()

        if item is None:
            raise ResourceNotFoundException()
        
        return item
    
    def get_all_itens(self) -> List[models.ItensModel] | HTTPException:

        itens: List[models.ItensModel] = self.db.query(models.ItensModel).filter(
            models.ItensModel.deleted==False
        ).order_by(models.ItensModel.id).all()

        if itens == []:
            raise NoContentException()
        
        return itens
    
    def create_item(self, body: schemas.ItensBodySchema) -> models.ItensModel | HTTPException:

        marca = self.marcas_logic.get_marca_by_id(marca_id=body.marcaID)
        categoria = self.categorias_logic.get_categoria_by_id(categoria_id=body.categoriaID)
        subcategoria = self.subcategorias_logic.get_sub_categoria_by_id(subcategoria_id=body.subcategoriaID)

        new_item = models.ItensModel(
            nome=body.nome,
            descricao=body.descricao,
            marcaID=marca.id,
            subcategoriaID=subcategoria.id,
            categoriaID=categoria.id
        )

        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)

        return new_item
    

    def update_item(self, item_id: int, body: schemas.ItensBodySchema) -> models.ItensModel | HTTPException:

        marca = self.marcas_logic.get_marca_by_id(marca_id=body.marcaID)
        categoria = self.categorias_logic.get_categoria_by_id(categoria_id=body.categoriaID)
        subcategoria = self.subcategorias_logic.get_sub_categoria_by_id(subcategoria_id=body.subcategoriaID)

        item: models.ItensModel = self.get_item_by_id(item_id=item_id)

        item.nome = body.nome
        item.descricao = body.descricao
        item.categoriaID = categoria.id
        item.subcategoriaID = subcategoria.id
        item.marcaID = marca.id
 
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        return item

    def delete_item(self, item_id: int) -> models.ItensModel | HTTPException:

        item: models.ItensModel = self.get_item_by_id(item_id=item_id)

        if item.deleted:
            return item
        
        item.deleted = True

        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        return item