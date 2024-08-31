from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from http import HTTPStatus
from database.instance import get_db
from typing import List
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
            raise HTTPException(status_code=404, detail=f"Não foi encontrada Categeoria com o ID {categoria_id}")
        
        return categoria

    def get_all_categorias(self) -> List[models.ItensCategoriasModel] | HTTPException:

        categorias: List[models.ItensCategoriasModel] = self.db.query(models.ItensCategoriasModel).all()

        if categorias == []:
            raise HTTPException(status_code=204, detail=f"Não existem categorias cadastradas")

        return categorias
    
    def create_categoria(self, body: schemas.ItensCategoriasBodySchema) -> models.ItensCategoriasModel:

        new_categoria: models.ItensCategoriasModel = models.ItensCategoriasModel(
            nome=body.nome
        )

        self.db.add(new_categoria)
        self.db.commit()
        self.db.refresh(new_categoria)

        return new_categoria


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
            raise HTTPException(status_code=404, detail=f"Não foi encontrada Sub Categoria com o ID {subcategoria_id}")
        
        return subcategoria


    def get_all_subcategorias(self) -> List[models.ItensSubCategoriasModel] | HTTPException:

        subcategorias: List[models.ItensSubCategoriasModel] = self.db.query(models.ItensSubCategoriasModel).all()

        if subcategorias == []:
            raise HTTPException(status_code=204, detail=f"Não existem subcategorias cadastrados")

        return subcategorias
    

    def get_subcategorias_by_categoria(self, categoria_id: int) -> List[models.ItensSubCategoriasModel] | HTTPException:

        categoria: models.ItensCategoriasModel = self.categoria_logic.get_categoria_by_id(categoria_id=categoria_id)
        
        subcategorias: List[models.ItensSubCategoriasModel] = self.db.query(models.ItensSubCategoriasModel).filter(
            models.ItensSubCategoriasModel.categoriaID == categoria.id
        ).all()

        
        if subcategorias == []:
            raise HTTPException(status_code=404, detail=f"Não foram encontradas Sub Categorias para a categoria {categoria.nome}")

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
            raise HTTPException(status_code=404, detail=f"Não foi encontrada Marca com o ID {marca_id}")

        return marca
    
    def get_all_marcas(self) -> List[models.ItensMarcasModel] | HTTPException:

        marcas: List[models.ItensMarcasModel] = self.db.query(models.ItensMarcasModel).all()

        if marcas == []:
            raise HTTPException(status_code=204, detail=f"Não existem marcas cadastrados")

        return marcas
    
    def create_marca(self, body: schemas.ItensMarcasBodySchema) -> models.ItensMarcasModel:

        new_marca = models.ItensMarcasModel(nome=body.nome)

        self.db.add(new_marca)
        self.db.commit()
        self.db.refresh(new_marca)

        return new_marca
    

class ItensUnidadesLogic: 

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db: Session = db

    def get_unidade_by_id(self, unidade_id: int) -> models.ItensUnidadesModel | HTTPException:
        
        unidade = self.db.query(models.ItensUnidadesModel).filter(
            models.ItensUnidadesModel.id==unidade_id
        ).first()

        if unidade == None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Unidade com id {unidade_id} não encontrada")

        return unidade
    
    def get_all_unidades(self) -> List[models.ItensUnidadesModel] | HTTPException:

        unidades = self.db.query(models.ItensUnidadesModel).all()

        if unidades == []:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Nenhuma Unidade cadastrada")
        
        return unidades
    
    def create_unidade(self, body: schemas.ItensUnidadesBodySchema) -> models.ItensUnidadesModel | HTTPException:

        if len(body.unidade) > 3:
            raise HTTPException(status_code=HTTPStatus.EXPECTATION_FAILED, detail="O campo Unidade deve conter até 3 caracteres")
        
        new_unidade: models.ItensUnidadesModel = models.ItensUnidadesModel(
            unidade=body.unidade,
            descricao=body.descricao
        )

        self.db.add(new_unidade)
        self.db.commit()
        self.db.refresh(new_unidade)

        return new_unidade
    

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
            raise HTTPException(status_code=404, detail=f"Não foi encontrado Item com o ID {item_id}")
        
        return item
    
    def get_all_itens(self) -> List[models.ItensModel] | HTTPException:

        itens: List[models.ItensModel] = self.db.query(models.ItensModel).all()

        if itens == []:
            raise HTTPException(status_code=204, detail="Não há itens cadastrados")
        
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