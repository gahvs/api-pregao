from fastapi import APIRouter, Depends
from typing import List
from . import logic
from . import schemas

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

# TODO: CRIAR ROTAS PARA MANIPULACAO DOS COMPRADORES E FORNECEDORES