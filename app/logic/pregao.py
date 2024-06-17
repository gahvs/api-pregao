from typing import List
from sqlalchemy.orm import Session
from models.pregao import PregaoModel, PregaoDemandantesModel, PregaoFornecedoresModel
from schemas.pregao import PregaoSchema, PregaoCreateSchema

PREGAO_CANCELED_STATUS = 'CANCELADO'
PREGAO_AUTHORIZED_STATUS = 'AUTORIZADO'
PREGAO_REJECTED_STATUS = 'REJEITADO'

# PREGAO LOGIC

def get_pregao(db: Session, pregao_id: int) -> PregaoModel:
    return db.query(PregaoModel).filter(PregaoModel.id == pregao_id).first()

def create_pregao(db: Session, pregao_data: PregaoCreateSchema) -> PregaoModel:

    pregao = PregaoModel(**pregao_data.model_dump())

    db.add(pregao)
    db.commit()
    db.refresh(pregao)
    
    return pregao

def update_pregao_status(db: Session, pregao_id: int, new_status: str) -> PregaoModel:
    pregao = get_pregao(db, pregao_id)

    if pregao is None:
        return None
    
    pregao.status = new_status

    db.add(pregao)
    db.commit()
    db.refresh

    return pregao

def set_pregao_as_canceled(db: Session, pregao_id: int) -> PregaoModel:
    return update_pregao_status(db, pregao_id=pregao_id, new_status=PREGAO_CANCELED_STATUS)

def set_pregao_as_rejected(db: Session, pregao_id: int) -> PregaoModel:
    return update_pregao_status(db, pregao_id=pregao_id, new_status=PREGAO_REJECTED_STATUS)

def set_pregao_as_authorized(db: Session, pregao_id: int) -> PregaoModel:
    return update_pregao_status(db, pregao_id=pregao_id, new_status=PREGAO_AUTHORIZED_STATUS)

# PREGAO_DEMANDANTES LOGIC
def get_demandante(db: Session, pregao_id: int, demandante_id: int) ->PregaoDemandantesModel:
    return db.query(PregaoDemandantesModel).filter(
            PregaoDemandantesModel.pregaoID == pregao_id,
            PregaoDemandantesModel.demandanteID == demandante_id
    ).first()

def demandante_is_in_pregao(db: Session, pregao_id: int, demandante_id: int) -> bool:
    query = db.query(PregaoDemandantesModel).filter(
            PregaoDemandantesModel.pregaoID == pregao_id,
            PregaoDemandantesModel.demandanteID == demandante_id
    )

    return db.query(query.exists()).scalar()

def create_pregao_demandantes(db: Session, pregao_id: int, demandantes: List[int]) -> List[PregaoDemandantesModel]:

    demandante_models = []

    for demandante_id in demandantes:
        if not demandante_is_in_pregao(db, pregao_id, demandante_id):
            demandante = PregaoDemandantesModel(pregaoID=pregao_id, demandanteID=demandante_id)
            db.add(demandante)
            db.commit()
            db.refresh(demandante)
            demandante_models.append(demandante)
        else:
            demandante_models.append(get_demandante(db, pregao_id, demandante_id))
    
    return demandante_models


# PREGAO_FORNECEDORES LOGIC
def get_fornecedor(db: Session, pregao_id: int, fornecedor_id: int) -> PregaoFornecedoresModel:
    return db.query(PregaoFornecedoresModel).filter(
            PregaoFornecedoresModel.pregaoID == pregao_id,
            PregaoFornecedoresModel.fornecedorID == fornecedor_id
    ).first()

def fornecedor_is_in_pregao(db: Session, pregao_id: int, fornecedor_id: int) -> bool:
    query = db.query(PregaoFornecedoresModel).filter(
            PregaoFornecedoresModel.pregaoID == pregao_id,
            PregaoFornecedoresModel.fornecedor_id == fornecedor_id
    )

    return db.query(query.exists()).scalar()

def create_pregao_participants(db: Session, pregao_id: int, fornecedores: List[int]) -> List[PregaoFornecedoresModel]:

    fornecedor_models = []

    for fornecedor_id in fornecedores:
        if not fornecedor_is_in_pregao(db, pregao_id, fornecedor_id):
            fornecedor = PregaoFornecedoresModel(pregaoID=pregao_id, fornecedorID=fornecedor_id)
            db.add(fornecedor)
            db.commit()
            db.refresh(fornecedor)
            fornecedor_models.append(fornecedor)
        else:
            fornecedor_models.append(get_fornecedor(db, pregao_id, fornecedor_id))
    
    return fornecedor_models