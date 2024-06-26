from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from database.instance import get_db
from typing import List
from . import models

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
            raise HTTPException(status_code=204, detail=f"Não existem categorias cadastrados")

        return categorias


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

        
        if subcategorias is None:
            raise HTTPException(status_code=404, detail=f"Não foram encontradas Sub Categorias para a categoria {categoria.nome}")

        return subcategorias
    


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
    



class ItensLogic:
    '''
        Realiza ações que tem como contexto a tabela ITENS
    '''

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db: Session = db

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