from typing import List
from sqlalchemy.orm import Session
from models.pregao import PregaoModel, PregaoDemandantesModel, PregaoFornecedoresModel, PregaoParticipantesModel
from schemas.pregao import PregaoSchema, PregaoCreateSchema

# PREGAO CONSTS
PREGAO_CANCELED_STATUS = 'CANCELADO'
PREGAO_AUTHORIZED_STATUS = 'AUTORIZADO'
PREGAO_REJECTED_STATUS = 'REJEITADO'
# PREGAO_PARTICIPANTES CONSTS
TIPO_PARTICIPANTE_FORNECEDOR = 'FORNECEDOR'
TIPO_PARTICIPANTE_DEMANDANTE = 'DEMANDANTE'


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

# PREGAO_PARTICIPANTES LOGIC

def get_participante(db: Session, pregao_id: int, usuario_id: int) -> PregaoParticipantesModel:
    return db.query(PregaoParticipantesModel).filter(
        PregaoParticipantesModel.pregaoID == pregao_id,
        PregaoParticipantesModel.usuarioID == usuario_id
    ).first()

def participante_is_in_pregao(db: Session, pregao_id: int, usuario_id: int) -> bool:
    query = db.query(PregaoParticipantesModel).filter(
        PregaoParticipantesModel.pregaoID == pregao_id,
        PregaoParticipantesModel.usuarioID == usuario_id
    )

    return db.query(query.exists()).scalar()

def create_pregao_participante(db: Session, pregao_id: int, usuario_id: int, tipo_participante: str) -> PregaoParticipantesModel:

    if participante_is_in_pregao(db, pregao_id, usuario_id):
        return get_participante(db, pregao_id, usuario_id)

    participante = PregaoParticipantesModel(pregaoID=pregao_id, usuarioID=usuario_id, tipoParticipante=tipo_participante)

    db.add(participante)
    db.commit()
    db.refresh(participante)

    return participante

def create_pregao_fornecedor(db: Session, pregao_id: int, usuario_id: int) -> PregaoParticipantesModel:
    return create_pregao_participante(db, pregao_id, usuario_id, TIPO_PARTICIPANTE_FORNECEDOR)

def create_pregao_demandante(db: Session, pregao_id: int, usuario_id: int) -> PregaoParticipantesModel:
    return create_pregao_participante(db, pregao_id, usuario_id, TIPO_PARTICIPANTE_DEMANDANTE)