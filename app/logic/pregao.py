from typing import List
from sqlalchemy.orm import Session
from models.pregao import PregaoModel, PregaoParticipantsModel
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
def get_participant(db: Session, pregao_id: int, participant_id: int) ->PregaoParticipantsModel:
    return db.query(PregaoParticipantsModel).filter(
            PregaoParticipantsModel.pregaoID == pregao_id,
            PregaoParticipantsModel.demandanteID == participant_id
    ).first()

def participant_is_in_pregao(db: Session, pregao_id: int, participant_id: int) -> bool:
    query = db.query(PregaoParticipantsModel).filter(
            PregaoParticipantsModel.pregaoID == pregao_id,
            PregaoParticipantsModel.demandanteID == participant_id
    )

    return db.query(query.exists()).scalar()

def create_pregao_participants(db: Session, pregao_id: int, participants: List[int]) -> List[PregaoParticipantsModel]:

    participant_models = []

    for participant_id in participants:
        if not participant_is_in_pregao(db, pregao_id, participant_id):
            participant = PregaoParticipantsModel(pregaoID=pregao_id, demandanteID=participant_id)
            db.add(participant)
            db.commit()
            db.refresh(participant)
            participant_models.append(participant)
        else:
            participant_models.append(get_participant(db, pregao_id, participant_id))
    
    return participant_models