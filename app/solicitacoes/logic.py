from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.instance import get_db
from itens.logic import ItensLogic
from typing import List
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