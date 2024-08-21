from fastapi import Depends, HTTPException
from database.instance import get_db
from sqlalchemy.orm import Session
from utils import errors
from typing import List
from usuarios.logic import UserLogic, CompradoresLogic, FornecedoresLogic
from usuarios.models import UserModel, CompradoresModel, FornecedoresModel
from solicitacoes.logic import SolicitacaoItensLogic
from . import models
from . import schemas


class PregaoLogic:
    '''
        Realiza ações que tem como contexto a tabela PREGAO
        Principais operações:

        - Criação de um novo Pregão
        - Autorização, Cancelamento e Rejeição de Pregão
    '''


    PREGAO_CANCELED_STATUS = 'CANCELADO'
    PREGAO_AUTHORIZED_STATUS = 'AUTORIZADO'
    PREGAO_REJECTED_STATUS = 'REJEITADO'

    def __init__(self, 
                 db: Session = Depends(get_db), 
                 user_logic: UserLogic = Depends(UserLogic)
            ) -> None:
        
        self.db: Session = db
        self.user_logic: UserLogic = user_logic

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


class PregaoParticipantesLogic:

    '''
        Contém a lógica de relacionamento entre Participantes (Compradores, Fornecedores) e Pregões.
        
        Principais operações:
        - Listagem dos Participantes (Forncedores ou Compradores) de um Pregão
        - Inclusão de um Comprador em um Pregão
        - Remoção de um Comprador de um Pregão
        - Inclusão de um Fornecedor em um Pregão
        - Remoção de um Fornecedor de um Pregão
    '''

    PARTICIPANTE_COMPRADOR_TIPO = "COMPRADOR"
    PARTICIPANTE_FORNECEDOR_TIPO = "FORNECEDOR"

    def __init__(self,
                 db: Session = Depends(get_db),
                 user_logic: UserLogic = Depends(UserLogic),
                 pregao_logic: PregaoLogic = Depends(PregaoLogic),
                 compradores_logic: CompradoresLogic = Depends(CompradoresLogic),
                 fornecedores_logic: FornecedoresLogic = Depends(FornecedoresLogic)
                ) -> None:
        
        self.db: Session = db
        self.user_logic: UserLogic = user_logic
        self.pregao_logic: PregaoLogic = pregao_logic
        self.compradores_logic: CompradoresLogic = compradores_logic
        self.fornecedores_logic: FornecedoresLogic = fornecedores_logic


    def get_pregao_participantes(self, pregao_id: int) -> List[models.PregaoParticipantesModel] | HTTPException:

        pregao: models.PregaoModel = self.pregao_logic.get_pregao_by_id(pregao_id=pregao_id)

        participantes: List[models.PregaoParticipantesModel] = self.db.query(models.PregaoParticipantesModel).filter(
            models.PregaoParticipantesModel.pregaoID==pregao.id
        ).all()

        if participantes == []:
            raise HTTPException(status_code=204, detail=f"Não há participantes inscritos no Pregão {pregao_id}")

        return participantes

    def get_participante_by_usuario_pregao(self, pregao_id: int, usuario_id: int) -> models.PregaoParticipantesModel | HTTPException:
        
        participante: models.PregaoParticipantesModel = self.db.query(models.PregaoParticipantesModel).filter(
            models.PregaoParticipantesModel.pregaoID==pregao_id,
            models.PregaoParticipantesModel.usuarioID==usuario_id
        ).first()

        if participante == None:
            raise HTTPException(status_code=404, detail=f"O Pregão {pregao_id} não possui Participante com id {usuario_id}")

        return participante
    

    def participante_already_setted(self, pregao_id: int, usuario_id: int) -> bool:

        participante: models.PregaoParticipantesModel = self.db.query(models.PregaoParticipantesModel).filter(
            models.PregaoParticipantesModel.pregaoID==pregao_id,
            models.PregaoParticipantesModel.usuarioID==usuario_id
        ).first()

        return participante != None


    def create_pregao_participante(self, pregao_id: int, usuario_id: int, participante_id: int, participante_tipo: str) -> models.PregaoParticipantesModel | HTTPException:

        if self.participante_already_setted(pregao_id=pregao_id, usuario_id=usuario_id):

            participante: models.PregaoParticipantesModel = self.get_participante_by_usuario_pregao(pregao_id=pregao_id, usuario_id=usuario_id)
            
            if participante.participanteTipo != participante_tipo:
                raise HTTPException(status_code=409, detail=f"Não é possível definir Usuário {usuario_id} como {participante_tipo}, Usuário já cadastrado como {participante.participanteTipo}")
            
            return participante    

        pregao: models.PregaoModel = self.pregao_logic.get_pregao_by_id(pregao_id=pregao_id)
        usuario: UserModel = self.user_logic.get_user_by_id(user_id=usuario_id)

        new_pregao_participante = models.PregaoParticipantesModel(
            pregaoID=pregao.id,
            usuarioID=usuario.id,
            participanteID=participante_id,
            participanteTipo=participante_tipo
        )

        self.db.add(new_pregao_participante)
        self.db.commit()
        self.db.refresh(new_pregao_participante)

        return new_pregao_participante
    

    def create_pregao_participante_comprador(self, pregao_id: int, body: schemas.PregaoParticipanteBodySchema) -> models.PregaoParticipantesModel | HTTPException:
        comprador: CompradoresModel = self.compradores_logic.get_comprador_by_usuario_id(usuario_id=body.usuarioID)
        return self.create_pregao_participante(pregao_id=pregao_id, usuario_id=body.usuarioID, participante_id=comprador.id, participante_tipo=self.PARTICIPANTE_COMPRADOR_TIPO)


    def create_pregao_participante_fornecedor(self, pregao_id: int, body: schemas.PregaoParticipanteBodySchema) -> models.PregaoParticipantesModel | HTTPException:
        fornecedor: FornecedoresModel = self.fornecedores_logic.get_fornecedor_by_usuario_id(usuario_id=body.usuarioID)
        return self.create_pregao_participante(pregao_id=pregao_id, usuario_id=body.usuarioID, participante_id=fornecedor.id, participante_tipo=self.PARTICIPANTE_FORNECEDOR_TIPO)