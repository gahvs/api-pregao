from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.instance import get_db
from usuarios.logic import CompradoresLogic, FornecedoresLogic
from usuarios.models import CompradoresModel, FornecedoresModel
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

    def __init__(self, db: Session = Depends(get_db), compradores_logic: CompradoresLogic = Depends(CompradoresLogic)) -> None:
        self.db: Session = db
        self.compradores_logic: CompradoresLogic = compradores_logic


    def get_solicitacao_by_id(self, solicitacao_id: int) -> models.SolicitacoesModel | HTTPException:

        solicitacao = self.db.query(models.SolicitacoesModel).filter(
            models.SolicitacoesModel.id == solicitacao_id
        ).first()

        if solicitacao is None:
            raise HTTPException(status_code=404, detail=f"Não foi encontrada Solicitação de Pregão com ID: {solicitacao_id}")
        
        return solicitacao
    
    
    def create_solicitacao(self, body: schemas.SolicitacoesBodySchema) -> models.SolicitacoesModel | HTTPException:

        comprador_criador = self.compradores_logic.get_comprador_by_id(comprador_id=body.criadoPor)

        solicitacao = models.SolicitacoesModel(
            descricao=body.descricao,
            informacoes=body.informacoes,
            dataHoraInicioSugerida=body.dataHoraInicioSugerida,
            dataHoraFimSugerida=body.dataHoraFimSugerida,
            criadoPor=comprador_criador.id,
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
    

class SolicitacaoCompradoresLogic:
    '''
        Realiza ações que tem como contexto a tabela PREGAO_SOLICITACOES_COMPRADORES
    '''

    def __init__(self,
                 db: Session = Depends(get_db),
                 solicitaco_logic: SolicitacaoLogic = Depends(SolicitacaoLogic),
                 compradores_logic: CompradoresLogic = Depends(CompradoresLogic)
            ) -> None:
        
        self.db: Session = db
        self.compradores_logic: CompradoresLogic = compradores_logic
        self.solicitacao_logic: SolicitacaoLogic = solicitaco_logic

    def get_solicitacao_comprador_by_id(self, solicitacao_comprador_id: int) -> models.SolicitacoesCompradoresModel | HTTPException:

        comprador = self.db.query(models.SolicitacoesCompradoresModel).filter(
            models.SolicitacoesCompradoresModel.id == solicitacao_comprador_id
        ).first()

        if comprador is None:
            raise HTTPException(status_code=404, detail=f"Não foi encontrada uma Solicitação Comprador com ID: {solicitacao_comprador_id}")
        
        return comprador


    def get_comprador_solicitacao_by_solicitacao_usuario(self, solicitacao_id: int, comprador_id: int) -> models.SolicitacoesCompradoresModel | HTTPException:
    
        solicitacao = self.solicitacao_logic.get_solicitacao_by_id(solicitacao_id=solicitacao_id)
        comprador = self.compradores_logic.get_comprador_by_id(comprador_id=comprador_id)

        comprador = self.db.query(models.SolicitacoesCompradoresModel).filter(
            models.SolicitacoesCompradoresModel.solicitacaoID==solicitacao.id,
            models.SolicitacoesCompradoresModel.compradorID==comprador.id
        ).first()

        return comprador


    def get_compradores_by_solicitacao(self, solicitacao_id: int) -> List[models.SolicitacoesCompradoresModel] | HTTPException:

        solicitacao = self.solicitacao_logic.get_solicitacao_by_id(solicitacao_id=solicitacao_id)

        compradores: List[models.SolicitacoesCompradoresModel] = self.db.query(models.SolicitacoesCompradoresModel).filter(
            models.SolicitacoesCompradoresModel.solicitacaoID == solicitacao.id
        ).all()

        if compradores == []:
            raise HTTPException(status_code=204, detail=f"Não há compradores para a Solicitação {solicitacao_id}")
        
        return compradores
    

    def create_solicitacao_comprador(self, solicitacao_id: int, body: schemas.SolicitacoesCompradoresBodySchema) -> models.SolicitacoesCompradoresModel | HTTPException:

        solicitacao_comprador = self.get_comprador_solicitacao_by_solicitacao_usuario(solicitacao_id=solicitacao_id, comprador_id=body.compradorID)
        
        if solicitacao_comprador is not None:
            return solicitacao_comprador

        solicitacao = self.solicitacao_logic.get_solicitacao_by_id(solicitacao_id=solicitacao_id)
        comprador: CompradoresModel = self.compradores_logic.get_comprador_by_id(comprador_id=body.compradorID)

        novo_comprador = models.SolicitacoesCompradoresModel(
            solicitacaoID=solicitacao.id,
            compradorID=comprador.id
        )
        
        self.db.add(novo_comprador)
        self.db.commit()
        self.db.refresh(novo_comprador)

        return novo_comprador


    def remove_solicitacao_comprador(self, solicitacao_comprador_id: int) -> None | HTTPException:

        comprador = self.get_solicitacao_comprador_by_id(solicitacao_comprador_id=solicitacao_comprador_id)

        self.db.delete(comprador)
        self.db.commit()

        return


class SolicitacaoFornecedoresLogic:
    '''
        Realiza ações que tem como contexto a tabela PREGAO_SOLICITACOES_FORNECEDORES
    '''

    def __init__(self,
                 db: Session = Depends(get_db),
                 solicitaco_logic: SolicitacaoLogic = Depends(SolicitacaoLogic),
                 fornecedores_logic: FornecedoresLogic = Depends(FornecedoresLogic)
            ) -> None:
        
        self.db: Session = db    
        self.solicitacao_logic: SolicitacaoLogic = solicitaco_logic
        self.fornecedores_logic: FornecedoresLogic = fornecedores_logic


    def get_solicitacao_fornecedor(self, solicitacao_fornecedor_id: int) -> None | HTTPException:

        fornecedor = self.db.query(models.SolicitacoesFornecedoresModel).filter(
            models.SolicitacoesFornecedoresModel.id == solicitacao_fornecedor_id
        ).first()

        if fornecedor is None:
            raise HTTPException(status_code=404, detail=f"Não foi encontrada uma Solicitação Fornecedor com ID: {solicitacao_fornecedor_id}")
        
        return fornecedor


    def get_solicitacao_fornecedor_by_solicitacao_usuario(self, solicitacao_id: int, fornecedor_id: int) -> models.SolicitacoesFornecedoresModel | HTTPException:
        
        solicitacao = self.solicitacao_logic.get_solicitacao_by_id(solicitacao_id=solicitacao_id)
        fornecedor = self.fornecedores_logic.get_fornecedor_by_id(fornecedor_id=fornecedor_id)

        fornecedor = self.db.query(models.SolicitacoesFornecedoresModel).filter(
            models.SolicitacoesFornecedoresModel.solicitacaoID==solicitacao.id,
            models.SolicitacoesFornecedoresModel.fornecedorID==fornecedor.id
        ).first()

        return fornecedor
    
    
    def get_fornecedores_by_solicitacao(self, solicitacao_id: int) -> List[models.SolicitacoesFornecedoresModel] | HTTPException:

        solicitacao = self.solicitacao_logic.get_solicitacao_by_id(solicitacao_id=solicitacao_id)

        fornecedores: List[models.SolicitacoesFornecedoresModel] = self.db.query(models.SolicitacoesFornecedoresModel).filter(
            models.SolicitacoesFornecedoresModel.solicitacaoID == solicitacao.id
        ).all()

        if fornecedores == []:
            raise HTTPException(status_code=204, detail=f"Não há fornecedores para a Solicitação {solicitacao_id}")
        
        return fornecedores



    def create_solicitacao_fornecedor(self, solicitacao_id: int, body: schemas.SolicitacoesFornecedoresBodySchema) -> models.SolicitacoesFornecedoresModel | HTTPException:

        solicitacao_fornecedor = self.get_solicitacao_fornecedor_by_solicitacao_usuario(solicitacao_id=solicitacao_id, fornecedor_id=body.fornecedorID)
        if solicitacao_fornecedor is not None:
            return solicitacao_fornecedor

        solicitacao = self.solicitacao_logic.get_solicitacao_by_id(solicitacao_id=solicitacao_id)
        fornecedor: FornecedoresModel = self.fornecedores_logic.get_fornecedor_by_id(fornecedor_id=body.fornecedorID)

        novo_fornecedor = models.SolicitacoesFornecedoresModel(
            solicitacaoID=solicitacao.id,
            fornecedorID=fornecedor.id
        )
        
        self.db.add(novo_fornecedor)
        self.db.commit()
        self.db.refresh(novo_fornecedor)

        return novo_fornecedor


    def remove_solicitacao_fornecedor(self, solicitacao_fornecedor_id: int) -> None | HTTPException:

        fornecedor = self.get_solicitacao_fornecedor(solicitacao_fornecedor_id=solicitacao_fornecedor_id)

        self.db.delete(fornecedor)
        self.db.commit()

        return



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