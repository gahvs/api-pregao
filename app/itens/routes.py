from fastapi import APIRouter, Depends
from typing import List
from . import logic
from . import schemas

router = APIRouter(
    prefix="/itens",
    tags=["Itens"]
)


@router.get("/{item_id}", response_model=schemas.ItensSchema)
def get_item_by_id(item_id: int, logic: logic.ItensLogic = Depends()):
    item = logic.get_item_by_id(item_id=item_id)
    return schemas.ItensSchema.model_validate(item)

@router.get("/", response_model=List[schemas.ItensSchema])
def get_all_itens(logic: logic.ItensLogic = Depends()):
    itens = logic.get_all_itens()
    return list(map(lambda i: schemas.ItensSchema.model_validate(i), itens))

@router.get("/categorias/{categoria_id}", response_model=schemas.ItensCategoriasSchema)
def get_categoria_by_id(categoria_id: int, logic: logic.ItensCategoriaLogic = Depends()):
    item = logic.get_categoria_by_id(categoria_id=categoria_id)
    return schemas.ItensCategoriasSchema.model_validate(item)

@router.get("/categorias", response_model=List[schemas.ItensCategoriasSchema])
def get_all_categorias(logic: logic.ItensCategoriaLogic = Depends()):
    itens = logic.get_all_categorias()
    return list(map(lambda i: schemas.ItensCategoriasSchema.model_validate(i), itens))

@router.get("/subcategorias/{subcategoria_id}", response_model=schemas.ItensSubCategoriasSchema)
def get_subcategoria_by_id(subcategoria_id: int, logic: logic.ItensSubCategoriaLogic = Depends()):
    subcategoria = logic.get_sub_categoria_by_id(subcategoria_id=subcategoria_id)
    return schemas.ItensSubCategoriasSchema.model_validate(subcategoria)

@router.get("/subcategorias", response_model=List[schemas.ItensSubCategoriasSchema])
def get_all_subcategorias(logic: logic.ItensSubCategoriaLogic = Depends()):
    subcategorias = logic.get_all_subcategorias()
    return list(map(lambda s: schemas.ItensSubCategoriasSchema.model_validate(s), subcategorias))

@router.get("/categorias/{categoria_id}/subcategorias", response_model=List[schemas.ItensSubCategoriasSchema])
def get_subcategorias_by_categoria(categoria_id: int, logic: logic.ItensSubCategoriaLogic = Depends()):
    subcategorias = logic.get_subcategorias_by_categoria(categoria_id=categoria_id)
    return list(map(lambda s: schemas.ItensSubCategoriasSchema.model_validate(s), subcategorias))

@router.get("/marcas/{marca_id}", response_model=schemas.ItensMarcasSchema)
def get_marca_by_id(marca_id: int, logic: logic.ItensMarcasLogic = Depends()):
    marca = logic.get_marca_by_id(marca_id=marca_id)
    return schemas.ItensMarcasSchema.model_validate(marca)

@router.get("/marcas", response_model=List[schemas.ItensMarcasSchema])
def get_all_marcas(logic: logic.ItensMarcasLogic = Depends()):
    marcas = logic.get_all_marcas()
    return list(map(lambda m: schemas.ItensMarcasSchema.model_validate(m), marcas))
