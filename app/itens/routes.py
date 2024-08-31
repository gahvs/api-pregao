from fastapi import APIRouter, Depends
from typing import List
from . import logic
from . import schemas

router = APIRouter(
    prefix="/itens",
    tags=["Itens"]
)

@router.post("/categorias/nova", response_model=schemas.ItensCategoriasSchema)
def create_categoria(body: schemas.ItensCategoriasBodySchema, logic: logic.ItensCategoriaLogic = Depends()):
    categoria = logic.create_categoria(body=body)
    return schemas.ItensCategoriasSchema.model_validate(categoria)

@router.get("/categorias/{categoria_id}", response_model=schemas.ItensCategoriasSchema)
def get_categoria_by_id(categoria_id: int, logic: logic.ItensCategoriaLogic = Depends()):
    item = logic.get_categoria_by_id(categoria_id=categoria_id)
    return schemas.ItensCategoriasSchema.model_validate(item)

@router.get("/categorias", response_model=List[schemas.ItensCategoriasSchema])
def get_all_categorias(logic: logic.ItensCategoriaLogic = Depends()):
    itens = logic.get_all_categorias()
    return list(map(lambda i: schemas.ItensCategoriasSchema.model_validate(i), itens))

@router.delete("/categorias/{categoria_id}", response_model=schemas.ItensCategoriasSchema)
def delete_categoria(categoria_id: int, logic: logic.ItensCategoriaLogic = Depends()):
    categoria = logic.delete_categoria(categoria_id=categoria_id)
    return schemas.ItensCategoriasSchema.model_validate(categoria)

@router.post("/subcategorias/nova", response_model=schemas.ItensSubCategoriasSchema)
def create_subcategoria(body: schemas.ItensSubCategoriasBodySchema, logic: logic.ItensSubCategoriaLogic = Depends() ):
    subcategoria = logic.create_subcategoria(body=body)
    return schemas.ItensSubCategoriasSchema.model_validate(subcategoria)

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

@router.delete("/subcategorias/{subcategoria_id}", response_model=schemas.ItensSubCategoriasSchema)
def delete_subcategoria(subcategoria_id: int, logic: logic.ItensSubCategoriaLogic = Depends()):
    subcategoria = logic.delete_subcategoria(subcategoria_id=subcategoria_id)
    return schemas.ItensSubCategoriasSchema.model_validate(subcategoria)

@router.post("/marcas/nova", response_model=schemas.ItensMarcasSchema)
def create_marca(body: schemas.ItensMarcasBodySchema, logic: logic.ItensMarcasLogic = Depends()):
    marca = logic.create_marca(body=body)
    return schemas.ItensMarcasSchema.model_validate(marca)

@router.get("/marcas/{marca_id}", response_model=schemas.ItensMarcasSchema)
def get_marca_by_id(marca_id: int, logic: logic.ItensMarcasLogic = Depends()):
    marca = logic.get_marca_by_id(marca_id=marca_id)
    return schemas.ItensMarcasSchema.model_validate(marca)

@router.get("/marcas", response_model=List[schemas.ItensMarcasSchema])
def get_all_marcas(logic: logic.ItensMarcasLogic = Depends()):
    marcas = logic.get_all_marcas()
    return list(map(lambda m: schemas.ItensMarcasSchema.model_validate(m), marcas))

@router.delete("/marcas/{marca_id}", response_model=schemas.ItensMarcasSchema)
def delete_marca(marca_id: int, logic: logic.ItensMarcasLogic = Depends()):
    marca = logic.delete_marca(marca_id=marca_id)
    return schemas.ItensMarcasSchema.model_validate(marca)

@router.post("/unidades/nova", response_model=schemas.ItensUnidadesSchema)
def create_unidade(body: schemas.ItensUnidadesBodySchema, logic: logic.ItensUnidadesLogic = Depends()):
    unidade = logic.create_unidade(body=body)
    return schemas.ItensUnidadesSchema.model_validate(unidade)

@router.get("/unidades/{unidade_id}", response_model=schemas.ItensUnidadesSchema)
def get_unidade_by_id(unidade_id: int, logic: logic.ItensUnidadesLogic = Depends()):
    unidade = logic.get_unidade_by_id(unidade_id=unidade_id)
    return schemas.ItensUnidadesSchema.model_validate(unidade)

@router.get("/unidades", response_model=List[schemas.ItensUnidadesSchema])
def get_all_unidades(logic: logic.ItensUnidadesLogic = Depends()):
    unidades = logic.get_all_unidades()
    return map(lambda u: schemas.ItensUnidadesSchema.model_validate(u), unidades)

@router.delete("/unidades/{unidade_id}", response_model=schemas.ItensUnidadesSchema)
def delete_unidade(unidade_id: int, logic: logic.ItensUnidadesLogic = Depends()):
    unidade = logic.delete_unidade(unidade_id=unidade_id)
    return schemas.ItensUnidadesSchema.model_validate(unidade)

@router.post("/novo", response_model=schemas.ItensSchema)
def create_item(body: schemas.ItensBodySchema, logic: logic.ItensLogic = Depends()):
    item = logic.create_item(body=body)
    return schemas.ItensSchema.model_validate(item)

@router.get("/{item_id}", response_model=schemas.ItensSchema)
def get_item_by_id(item_id: int, logic: logic.ItensLogic = Depends()):
    item = logic.get_item_by_id(item_id=item_id)
    return schemas.ItensSchema.model_validate(item)

@router.get("/", response_model=List[schemas.ItensSchema])
def get_all_itens(logic: logic.ItensLogic = Depends()):
    itens = logic.get_all_itens()
    return list(map(lambda i: schemas.ItensSchema.model_validate(i), itens))

@router.delete("/{item_id}", response_model=schemas.ItensSchema)
def delete_item(item_id: int, logic: logic.ItensLogic = Depends()):
    item = logic.delete_item(item_id=item_id)
    return schemas.ItensSchema.model_validate(item)