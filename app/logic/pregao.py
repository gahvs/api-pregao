from fastapi import Depends, HTTPException
from database.instance import get_db
from sqlalchemy.orm import Session
from models import pregao as models
from schemas import pregao as schemas
from utils import errors
from . import user


class PregaoLogic:
    '''
        Realiza ações que tem como contexto a tabela PREGAO
    '''


    PREGAO_CANCELED_STATUS = 'CANCELADO'
    PREGAO_AUTHORIZED_STATUS = 'AUTORIZADO'
    PREGAO_REJECTED_STATUS = 'REJEITADO'


    def __init__(self, db: Session = Depends(get_db), user_logic: user.UserLogic = Depends(user.UserLogic)) -> None:
        self.db: Session = db
        self.user_logic = user_logic

    def validate(self, user_id: int):
        _ = self.user_logic.get_user_by_id(user_id=user_id)


    def get_pregao_by_id(self, pregao_id: int) -> models.PregaoModel | HTTPException:
        pregao = self.db.query(models.PregaoModel).filter(models.PregaoModel.id == pregao_id).first()
        
        if pregao is None:
            raise HTTPException(status_code=404, detail=errors.not_found_message("PREGAO", pregao_id))
        
        return pregao
        

    def create_pregao(self, body: schemas.PregaoCreateSchema) -> models.PregaoModel:
        self.validate(body.usuarioID)

        pregao = models.PregaoModel(
            descricao=body.descricao,
            criadoPor=body.usuarioID,
            dataHoraInicio=body.dataHoraInicio,
            dataHoraFim=body.dataHoraFim
        )

        self.db.add(pregao)
        self.db.commit()
        self.db.refresh(pregao)

        return pregao
    

    def change_pregao_status(self, pregao_id: int, new_status: str) -> models.PregaoModel:
        pregao = self.get_pregao_by_id(pregao_id=pregao_id)
        pregao.status = new_status
        
        self.db.add(pregao)
        self.db.commit()
        self.db.refresh(pregao)

        return pregao


    def cancel_pregao(self, pregao_id: int) -> models.PregaoModel:
        return self.change_pregao_status(pregao_id=pregao_id, new_status=self.PREGAO_CANCELED_STATUS)


    def reject_pregao(self, pregao_id: int) -> models.PregaoModel:
        return self.change_pregao_status(pregao_id=pregao_id, new_status=self.PREGAO_REJECTED_STATUS)


    def authorize_pregao(self, pregao_id: int) -> models.PregaoModel:
        return self.change_pregao_status(pregao_id=pregao_id, new_status=self.PREGAO_AUTHORIZED_STATUS)        


class PregaoParticipanteLogic:
    '''
        Realiza ações que tem como contexto a tabela PREGAO_PARTICIPANTES
    '''
        

    TIPO_PARTICIPANTE_FORNECEDOR = 'FORNECEDOR'
    TIPO_PARTICIPANTE_DEMANDANTE = 'DEMANDANTE'        


    def __init__(self, 
                 db: Session = Depends(get_db), 
                 pregao_logic: PregaoLogic = Depends(PregaoLogic),
                 user_logic: user.UserLogic = Depends(user.UserLogic)
        ) -> None:

        self.db: Session = db
        self.user_logic = user_logic
        self.pregao_logic = pregao_logic


    def validate(self, pregao_id: int, usuario_id: int) -> HTTPException | None:
        _ = self.user_logic.get_user_by_id(user_id=usuario_id)
        _ = self.pregao_logic.get_pregao_by_id(pregao_id=pregao_id)


    def get_participante_by_pregao_usuario(self, pregao_id: int, usuario_id: int) -> models.PregaoParticipantesModel | HTTPException:
        self.validate(pregao_id=pregao_id, usuario_id=usuario_id)
        print("pregao_id:", pregao_id)
        print("usuario_id:",usuario_id)

        return self.db.query(models.PregaoParticipantesModel).filter(
            models.PregaoParticipantesModel.pregaoID == pregao_id,
            models.PregaoParticipantesModel.usuarioID == usuario_id
        ).first()


    def participante_isin_pregao(self, pregao_id:int, usuario_id: int) -> bool | HTTPException:
        self.validate(pregao_id=pregao_id, usuario_id=usuario_id)

        query = self.db.query(models.PregaoParticipantesModel).filter(
            models.PregaoParticipantesModel.pregaoID == pregao_id,
            models.PregaoParticipantesModel.usuarioID == usuario_id
        )

        return self.db.query(query.exists()).scalar()        
    

    def create_participante(self, body: schemas.PregaoParticipantesResponseSchema, pregao_id: int, tipoParticipante: str) -> models.PregaoParticipantesModel:
        participante = models.PregaoParticipantesModel(
            pregaoID=pregao_id, 
            usuarioID=body.usuarioID,
            tipoParticipante=tipoParticipante
        )

        self.db.add(participante)
        self.db.commit()
        self.db.refresh(participante)

        return participante
    
    
    def create_fornecedor(self, body: schemas.PregaoParticipanteSchema, pregao_id: int) -> models.PregaoParticipantesModel | HTTPException:    
        self.validate(pregao_id, body.usuarioID)

        if self.participante_isin_pregao(pregao_id=pregao_id, usuario_id=body.usuarioID):
            return self.get_participante_by_pregao_usuario(pregao_id=pregao_id, usuario_id=body.usuarioID)
        
        return self.create_participante(body=body, pregao_id=pregao_id, tipoParticipante=self.TIPO_PARTICIPANTE_FORNECEDOR)


    def create_demandante(self, body: schemas.PregaoParticipanteSchema, pregao_id: int) -> models.PregaoParticipantesModel:
        self.validate(pregao_id, body.usuarioID)

        if self.participante_isin_pregao(pregao_id=pregao_id, usuario_id=body.usuarioID):
            return self.get_participante_by_pregao_usuario(pregao_id=pregao_id, usuario_id=body.usuarioID)
        
        return self.create_participante(body=body, pregao_id=pregao_id, tipoParticipante=self.TIPO_PARTICIPANTE_DEMANDANTE)    


class PregaoDemandasLogic:
    '''
        Realiza ações que tem como contexto a tabela PREGAO_DEMANDAS e PREGAO_PRODUTOS
    '''
        
    def __init__(self, 
                 db: Session = Depends(get_db), 
                 pregao_logic: PregaoLogic = Depends(PregaoLogic),
                 pregao_participante_logic: PregaoParticipanteLogic = Depends(PregaoParticipanteLogic)
            ) -> None:
        self.db: Session = db
        self.pregao_logic: PregaoLogic = pregao_logic
        self.pregao_participante_logic: PregaoParticipanteLogic = pregao_participante_logic

    def validate(self, pregao_id: int, user_id: int) -> HTTPException | None:
        _ = self.pregao_logic.get_pregao_by_id(pregao_id=pregao_id)
        
        participante = self.pregao_participante_logic.get_participante_by_pregao_usuario(pregao_id=pregao_id, usuario_id=user_id)
        
        if participante is None:
            raise HTTPException(status_code=404, detail=f"Usuário {user_id} não é Demandante do Pregão {pregao_id}")

        if participante.tipoParticipante == self.pregao_participante_logic.TIPO_PARTICIPANTE_FORNECEDOR:
            raise HTTPException(status_code=400, detail=f"Usuário {user_id} é um fornecedor do Pregão {pregao_id}, não é possível definir demandas")

    def __create_demanda(self, pregao_id: int, body: schemas.PregaoDemandaSchema) -> models.PregaoDemandasModel:
        demanda = models.PregaoDemandasModel(
            pregaoID=pregao_id,
            usuarioID=body.usuarioID,
            descricao=body.descricao,
            unidade=body.unidade,
            quantidade=body.quantidade
        )

        self.db.add(demanda)
        self.db.commit()
        self.db.refresh(demanda)
        
        return demanda
    

    def create_pregao_demanda(self, pregao_id: int, body: schemas.PregaoDemandaSchema) -> models.PregaoDemandasModel:
        
        self.validate(pregao_id=pregao_id, user_id=body.usuarioID)

        demanda = self.__create_demanda(pregao_id=pregao_id, body=body)

        return demanda