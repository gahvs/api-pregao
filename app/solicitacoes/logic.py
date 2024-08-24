from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.instance import get_db
from usuarios.logic import UserLogic
from itens.logic import ItensLogic
from typing import List
from http import HTTPStatus
from . import models
from . import schemas

class SolicitacaoLogic:
    '''
        Realiza ações que tem como contexto a tabela PREGAO_SOLICITACOES
    '''
    
    STATUS_EM_ANALISE = "Em análise"
    STATUS_APROVADO = "Aprovado"
    STATUS_REJEITADO = "Rejeitado"
    
    OBSERVACAO_DEFAULT_VALUE = "Estamos analisando sua solicitação de Pregão"

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db: Session = db


    def get_solicitacao_by_id(self, solicitacao_id: int) -> models.SolicitacoesModel | HTTPException:

        solicitacao = self.db.query(models.SolicitacoesModel).filter(
            models.SolicitacoesModel.id == solicitacao_id
        ).first()

        if solicitacao is None:
            raise HTTPException(status_code=404, detail=f"Não foi encontrada Solicitação de Pregão com ID: {solicitacao_id}")
        
        return solicitacao
    
    
    def create_solicitacao(self, body: schemas.SolicitacoesBodySchema) -> models.SolicitacoesModel | HTTPException:
    

        solicitacao = models.SolicitacoesModel(
            descricao=body.descricao,
            informacoes=body.informacoes,
            dataHoraInicioSugerida=body.dataHoraInicioSugerida,
            dataHoraFimSugerida=body.dataHoraFimSugerida,
            criadoPor=1, # usar id do usuario
            status=self.STATUS_EM_ANALISE,
            motivoRejeicao="",
        )

        self.db.add(solicitacao)
        self.db.commit()
        self.db.refresh(solicitacao)

        return solicitacao
    

    def update_solicitacao_status(self, solicitacao_id: int, new_status: str) -> models.SolicitacoesModel | HTTPException:
        solicitacao: models.SolicitacoesItensModel = self.get_solicitacao_by_id(solicitacao_id=solicitacao_id)

        solicitacao.status = new_status
        self.db.add(solicitacao)
        self.db.commit()
        self.db.refresh(solicitacao)

        return solicitacao
    

    def approve_solicitacao(self, solicitacao_id: int) -> models.SolicitacoesItensModel | HTTPException:
        return self.update_solicitacao_status(solicitacao_id=solicitacao_id, new_status=self.STATUS_APROVADO)


    def reject_solicitacao(self, solicitacao_id: int, body: schemas.SolicitacoesRejeicaoBodySchema) -> models.SolicitacoesItensModel | HTTPException:
        solicitacao = self.update_solicitacao_status(solicitacao_id=solicitacao_id, new_status=self.STATUS_REJEITADO)

        solicitacao.motivoRejeicao = body.motivoRejeicao
        
        self.db.add(solicitacao)
        self.db.commit()
        self.db.refresh(solicitacao)

        return solicitacao
    

class SolicitacaoItensLogic:
    '''
        Realiza ações que tem como contexto a tabela PREGAO_SOLICITACOES_ITENS
    '''
    
    def __init__(self, 
                 db: Session = Depends(get_db),
                 solicitacao_logic: SolicitacaoLogic = Depends(SolicitacaoLogic),
                 itens_logic: ItensLogic = Depends(ItensLogic)
            ) -> None:
        self.db: Session = db
        self.itens_logic: ItensLogic = itens_logic
        self.solicitacao_logic: SolicitacaoLogic = solicitacao_logic

    
    def create_solicitacao_item(self, solicitacao_id: int, body: schemas.SolicitacoesItensBodySchema) -> models.SolicitacoesItensModel | HTTPException:
        
        solicitacao = self.solicitacao_logic.get_solicitacao_by_id(solicitacao_id=solicitacao_id)

        item = models.SolicitacoesItensModel(
            solicitacaoID=solicitacao.id,
            criadoPor=solicitacao.criadoPor,
            itemID=body.itemID,
            unidade=body.unidade,
            projecaoQuantidade=body.projecaoQuantidade,
        )

        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        return item
    

    def get_solicitacao_itens(self, solicitacao_id: int) -> List[models.SolicitacoesItensModel] | HTTPException:

        solicitacao: models.SolicitacoesModel = self.solicitacao_logic.get_solicitacao_by_id(solicitacao_id=solicitacao_id)

        itens: List[models.SolicitacoesItensModel] = self.db.query(models.SolicitacoesItensModel).filter(
            models.SolicitacoesItensModel.solicitacaoID == solicitacao.id
        ).all()

        if itens == []:
            raise HTTPException(status_code=204, detail=f"A solicitação {solicitacao_id} não tem itens cadastrados")
        
        return itens
    

class SolicitacaoParticipantesLogic:

    '''
        Realiza operações envolvendo Participantes de uma Solicitação de Pregão. Entidade: PREGAO_SOLICITACOES_PARTICIPANTES
        Principais Operações:
        - Definir usuário como Comprador/Fornecedor em uma solicitação de Pregão
        - Remover usuário como Comprador/Fornecedor em uma solicitação de Pregão
        - Listar usuários Participantes em uma solicitação de Pregão
    '''
    
    PARTICIPANTE_COMPRADOR_TIPO = "COMPRADOR"
    PARTICIPANTE_FORNECEDOR_TIPO = "FORNECEDOR"

    def __init__(self,
                db: Session = Depends(get_db),
                solicitacao_logic: SolicitacaoLogic = Depends(SolicitacaoLogic),
                user_logic: UserLogic = Depends(UserLogic)
                 ) -> None:
        
        self.db: Session = db
        self.solicitacao_logic: SolicitacaoLogic = solicitacao_logic
        self.user_logic: UserLogic = user_logic

    def get_solicitacao_participante_by_id(self, solicitacao_participante_id: int) -> models.SolicitacoesParticipantesModel | HTTPException:

        participante = self.db.query(models.SolicitacoesParticipantesModel).filter(
            models.SolicitacoesParticipantesModel.id==solicitacao_participante_id
        ).first()

        if participante == None:
            raise HTTPException(status_code=HTTPStatus.NO_CONTENT, detail=f"Participante de Solicitação com ID {solicitacao_participante_id} não encontrado")
        
        return participante
    

    def get_solicitacao_participantes(self, solicitacao_id: int) -> List[models.SolicitacoesParticipantesModel] | HTTPException:

        solicitacao = self.solicitacao_logic.get_solicitacao_by_id(solicitacao_id=solicitacao_id)

        participantes = self.db.query(models.SolicitacoesParticipantesModel).filter(
            models.SolicitacoesParticipantesModel.solicitacaoID==solicitacao.id
        ).all()

        if participantes == []:
            raise HTTPException(status_code=HTTPStatus.NO_CONTENT, detail=f"Solicitação {solicitacao_id} não possui Participantes")
        
        return participantes
    

    def get_participante_using_solicitacao_usuario(self, solicitacao_id: int, usuario_id: int) -> models.SolicitacoesParticipantesModel | HTTPException:

        participante = self.db.query(models.SolicitacoesParticipantesModel).filter(
            models.SolicitacoesParticipantesModel.solicitacaoID==solicitacao_id,
            models.SolicitacoesParticipantesModel.usuarioID==usuario_id
        ).first()

        if participante == None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Usuário {usuario_id} não é Participante da Solicitação de Pregão {solicitacao_id}")

        return participante
    

    def participante_already_setted(self, solicitacao_id: int, usuario_id: int) -> bool:

        participante = self.db.query(models.SolicitacoesParticipantesModel).filter(
            models.SolicitacoesParticipantesModel.solicitacaoID==solicitacao_id,
            models.SolicitacoesParticipantesModel.usuarioID==usuario_id
        ).first()


        return participante != None

    
    def create_solicitacao_participante(self, solicitacao_id: int, usuario_id: int, participante_tipo: str) -> models.SolicitacoesParticipantesModel | HTTPException:

        if self.participante_already_setted(solicitacao_id=solicitacao_id, usuario_id=usuario_id):

            participante = self.get_participante_using_solicitacao_usuario(solicitacao_id=solicitacao_id, usuario_id=usuario_id)
            
            if participante.participanteTipo == participante_tipo:
                return participante
            
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=f"Não é possível definir o Usuário {usuario_id} como {participante_tipo}, Usuário já participa como {participante.participanteTipo}")

        solicitacao = self.solicitacao_logic.get_solicitacao_by_id(solicitacao_id=solicitacao_id)
        usuario = self.user_logic.get_user_by_id(user_id=usuario_id)

        new_solicitacao_participante = models.SolicitacoesParticipantesModel(
            solicitacaoID=solicitacao.id,
            usuarioID=usuario.id,
            participanteTipo=participante_tipo
        )

        self.db.add(new_solicitacao_participante)
        self.db.commit()
        self.db.refresh(new_solicitacao_participante)

        return new_solicitacao_participante
    

    def create_solicitacao_comprador(self, solicitacao_id: int, body: schemas.SolicitacoesParticipantesBodySchema) -> models.SolicitacoesParticipantesModel | HTTPException:
        return self.create_solicitacao_participante(solicitacao_id=solicitacao_id, usuario_id=body.usuarioID, participante_tipo=self.PARTICIPANTE_COMPRADOR_TIPO)
    
    
    def create_solicitacao_fornecedor(self, solicitacao_id: int, body: schemas.SolicitacoesParticipantesBodySchema) -> models.SolicitacoesParticipantesModel | HTTPException:
        return self.create_solicitacao_participante(solicitacao_id=solicitacao_id, usuario_id=body.usuarioID, participante_tipo=self.PARTICIPANTE_FORNECEDOR_TIPO)
    
    def remove_solicitacao_participante(self, solicitacao_participante_id: int) -> None | HTTPException:

        participante = self.get_solicitacao_participante_by_id(solicitacao_participante_id=solicitacao_participante_id)

        self.db.delete(participante)
        self.db.commit()

        return