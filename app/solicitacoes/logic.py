from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.instance import get_db
from user.logic import UserLogic
from user.models import UserModel
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

    def __init__(self, db: Session = Depends(get_db), user_logic: UserLogic = Depends(UserLogic)) -> None:
        self.db: Session = db
        self.user_logic: UserLogic = user_logic


    def get_solicitacao_by_id(self, solicitacao_id: int) -> models.SolicitacoesModel | HTTPException:

        solicitacao = self.db.query(models.SolicitacoesModel).filter(
            models.SolicitacoesModel.id == solicitacao_id
        ).first()

        if solicitacao is None:
            raise HTTPException(status_code=404, detail=f"Não foi encontrada Solicitação de Pregão com ID: {solicitacao_id}")
        
        return solicitacao
    

    def get_solicitacao_criador(self, criador_id: int) -> UserModel | HTTPException:
        
        user = self.user_logic.get_user_by_id(user_id=criador_id)

        if user is None:
            raise HTTPException(status_code=404, detail=f"Não foi encontrado Usuário com ID: {criador_id}")
        
        return user
    
    
    def create_solicitacao(self, body: schemas.SolicitacoesBodySchema) -> models.SolicitacoesModel | HTTPException:

        solicitacao_criador = self.get_solicitacao_criador(criador_id=body.criadoPor)

        solicitacao = models.SolicitacoesModel(
            descricao=body.descricao,
            informacoes=body.informacoes,
            dataHoraInicioSugerida=body.dataHoraInicioSugerida,
            dataHoraFimSugerida=body.dataHoraFimSugerida,
            criadoPor=solicitacao_criador.id,
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
                 solicitacao_logic: SolicitacaoLogic = Depends(SolicitacaoLogic)) -> None:
        self.db: Session = db
        self.solicitacao_logic: SolicitacaoLogic = solicitacao_logic

    
    def create_solicitacao_item(self, body: schemas.SolicitacoesItensBodySchema) -> models.SolicitacoesItensModel | HTTPException:
        
        solicitacao = self.solicitacao_logic.get_solicitacao_by_id(solicitacao_id=body.solicitacaoID)

        item = models.SolicitacoesItensModel(
            solicitacaoID=solicitacao.id,
            criadoPor=solicitacao.criadoPor,
            descricao=body.descricao,
            unidade=body.unidade,
            projecaoQuantidade=body.projecaoQuantidade,
        )

        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        return item