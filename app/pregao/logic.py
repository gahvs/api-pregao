from fastapi import Depends, HTTPException
from database.instance import get_db
from sqlalchemy.orm import Session
from utils import errors
from typing import List
from usuarios.logic import UserLogic
from solicitacoes.logic import SolicitacaoItensLogic
from solicitacoes.models import SolicitacoesItensModel
from . import models
from . import schemas


class PregaoLogic:
    '''
        Realiza ações que tem como contexto a tabela PREGAO
    '''


    PREGAO_CANCELED_STATUS = 'CANCELADO'
    PREGAO_AUTHORIZED_STATUS = 'AUTORIZADO'
    PREGAO_REJECTED_STATUS = 'REJEITADO'

    def __init__(self, 
                 db: Session = Depends(get_db), 
                 user_logic: UserLogic = Depends(UserLogic),
                 solicitacao_itens_logic: SolicitacaoItensLogic = Depends(SolicitacaoItensLogic)
            ) -> None:
        
        self.db: Session = db
        self.user_logic: UserLogic = user_logic
        self.solicitacao_itens_logic: SolicitacaoItensLogic = solicitacao_itens_logic

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
            informacoes=body.informacoes,
            criadoPor=body.usuarioID,
            dataHoraInicio=body.dataHoraInicio,
            dataHoraFim=body.dataHoraFim,
            abertoADemandasEm=body.abertoADemandasEm,
            abertoADemandasAte=body.abertoADemandasAte
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
                 user_logic: UserLogic = Depends(UserLogic)
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


    def get_pregao_participantes(self, pregao_id: int) -> List[models.PregaoParticipantesModel]:
        pregao: models.PregaoModel = self.pregao_logic.get_pregao_by_id(pregao_id=pregao_id)

        participantes: List[models.PregaoParticipantesModel] = self.db.query(models.PregaoParticipantesModel).filter(
            models.PregaoParticipantesModel.pregaoID == pregao.id
        ).all()

        if participantes == []:
            raise HTTPException(status_code=204, detail=f"O pregão {pregao_id} não possui participantes")
        
        return participantes


class PregaoItensLogic:
    '''
        Realiza ações que tem como contexto a tabela PREGAO_PREGOES_ITENS
    '''
        
    def __init__(self, 
                 db: Session = Depends(get_db), 
                 pregao_logic: PregaoLogic = Depends(PregaoLogic),
                 pregao_participante_logic: PregaoParticipanteLogic = Depends(PregaoParticipanteLogic)
            ) -> None:
        self.db: Session = db
        self.pregao_logic: PregaoLogic = pregao_logic
        self.pregao_participante_logic: PregaoParticipanteLogic = pregao_participante_logic

    def validate_pregao(self, pregao_id: int) -> HTTPException | None: 
        _ = self.pregao_logic.get_pregao_by_id(pregao_id=pregao_id)
    
    
    def validate_participante(self, pregao_id: int, user_id: int) -> HTTPException | None:
        
        participante = self.pregao_participante_logic.get_participante_by_pregao_usuario(pregao_id=pregao_id, usuario_id=user_id)
        
        if participante is None:
            raise HTTPException(status_code=404, detail=f"Usuário {user_id} não é Demandante do Pregão {pregao_id}")

        if participante.tipoParticipante == self.pregao_participante_logic.TIPO_PARTICIPANTE_FORNECEDOR:
            raise HTTPException(status_code=400, detail=f"Usuário {user_id} é um fornecedor do Pregão {pregao_id}, não é possível definir demandas")


    def get_demanda_by_id(self, demanda_id: int) -> models.PregaoItensModel | HTTPException:

        demanda: models.PregaoItensModel = self.db.query(models.PregaoItensModel).filter(
            models.PregaoItensModel.id == demanda_id
        ).first()

        if demanda == None:
            raise HTTPException(status_code=404, detail=f"Não foi encontrada Demanda com ID {demanda_id}")
        
        return demanda    


    def create_pregao_demanda(self, pregao_id: int, body: schemas.PregaoItensSchema) -> models.PregaoItensModel:
        
        self.validate_pregao(pregao_id=pregao_id)
        self.validate_participante(pregao_id=pregao_id, user_id=body.criadoPor)

        demanda = models.PregaoItensModel(
            pregaoID=pregao_id,
            itemID=body.itemID,
            criadoPor=body.criadoPor,
            unidade=body.unidade,
            quantidade=body.quantidade
        )

        self.db.add(demanda)
        self.db.commit()
        self.db.refresh(demanda)

        return demanda
    
    
    def update_demanda_quantidade(self, demanda_id: int, body: schemas.PregaoItensUpdateQuantidadeSchema) -> models.PregaoItensModel | HTTPException:

        demanda: models.PregaoItensModel = self.get_demanda_by_id(demanda_id=demanda_id)
        demanda.quantidade = body.quantidade

        self.db.add(demanda)
        self.db.commit()
        self.db.refresh(demanda)

        return demanda


    def get_pregao_demandas(self, pregao_id: int) -> List[models.PregaoItensModel] | HTTPException:

        pregao: models.PregaoModel = self.pregao_logic.get_pregao_by_id(pregao_id=pregao_id)
        
        demandas: List[models.PregaoItensModel] = self.db.query(models.PregaoItensModel).filter(
            models.PregaoItensModel.pregaoID == pregao.id
        ).all()

        if demandas == []:
            raise HTTPException(status_code=204, detail=f"Não há demandas para o Pregão {pregao_id}")

        return demandas