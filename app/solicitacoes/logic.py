from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.instance import get_db
from usuarios.logic import UserLogic
from itens.logic import ItensLogic, ItensUnidadesLogic, ItensCategoriaLogic, ItensSubCategoriaLogic, ItensMarcasLogic
from typing import List
from http import HTTPStatus
from utils.http_exceptions import NoContentException, ResourceNotFoundException, ResourceExpectationFailedException, ResourceConflictException
from . import models
from . import schemas

class SolicitacaoLogic:
    '''
        Realiza ações que tem como contexto a tabela PREGAO_SOLICITACOES
    '''
    
    STATUS_EM_ANALISE = "PENDENTE"
    STATUS_APROVADO = "APROVADA"
    STATUS_REJEITADO = "REJEITADA"
    STATUS_CONVERTIDO = "CONVERTIDA"
    
    OBSERVACAO_DEFAULT_VALUE = "Estamos analisando sua solicitação de Pregão"

    def __init__(self, 
                 db: Session = Depends(get_db),
                 user_logic: UserLogic = Depends()
                 ) -> None:
        
        self.db: Session = db
        self.user_logic: UserLogic = user_logic


    def get_solicitacao_by_id(self, solicitacao_id: int) -> models.SolicitacoesModel | HTTPException:

        solicitacao = self.db.query(models.SolicitacoesModel).filter(
            models.SolicitacoesModel.id == solicitacao_id
        ).first()

        if solicitacao is None:
            raise HTTPException(status_code=404, detail=f"Não foi encontrada Solicitação de Pregão com ID: {solicitacao_id}")
        
        return solicitacao
    
    
    def create_solicitacao(self, body: schemas.SolicitacoesBodySchema) -> models.SolicitacoesModel | HTTPException:
    
        usuario = self.user_logic.get_user_by_id(body.criadoPor)

        solicitacao = models.SolicitacoesModel(
            descricao=body.descricao,
            informacoes=body.informacoes,
            dataHoraInicioSugerida=body.dataHoraInicioSugerida,
            dataHoraFimSugerida=body.dataHoraFimSugerida,
            criadoPor=usuario.id,
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
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Participante de Solicitação com ID {solicitacao_participante_id} não encontrado")
        
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
    
    def remove_solicitacao_participante(self, solicitacao_id: int, solicitacao_participante_id: int) -> None | HTTPException:

        _ = self.solicitacao_logic.get_solicitacao_by_id(solicitacao_id=solicitacao_id)

        participante = self.get_solicitacao_participante_by_id(solicitacao_participante_id=solicitacao_participante_id)

        self.db.delete(participante)
        self.db.commit()

        return
    
    def participante_is_comprador(self, participante: models.SolicitacoesParticipantesModel) -> bool:
        return participante.participanteTipo == self.PARTICIPANTE_COMPRADOR_TIPO
    
    
class SolicitacaoItensLogic:
    '''
        Realiza operações envolvendo Solicitaçoes e Itens da Solicitação.
        Principais operações:
        - Listagem dos Itens da Solicitação
        - Adicionar Itens à uma Solicitação
        - Alterar Itens de uma Solicitação
        - Remover Itens de uma Solicitação
    '''
    
    def __init__(self, 
                 db: Session = Depends(get_db),
                 solicitacao_logic: SolicitacaoLogic = Depends(SolicitacaoLogic),
                 participante_logic: SolicitacaoParticipantesLogic = Depends(SolicitacaoParticipantesLogic),
                 itens_logic: ItensLogic = Depends(ItensLogic),
                 unidades_logic: ItensUnidadesLogic = Depends(ItensUnidadesLogic),
                 categorias_logic: ItensCategoriaLogic = Depends(ItensCategoriaLogic),
                 subcategorias_logic: ItensSubCategoriaLogic = Depends(ItensSubCategoriaLogic),
                 itens_marcas_logic: ItensMarcasLogic = Depends(ItensMarcasLogic)
            ) -> None:
        self.db: Session = db
        self.itens_logic: ItensLogic = itens_logic
        self.solicitacao_logic: SolicitacaoLogic = solicitacao_logic
        self.participante_logic: SolicitacaoParticipantesLogic = participante_logic
        self.unidades_logic: ItensUnidadesLogic = unidades_logic
        self.categorias_logic: ItensCategoriaLogic = categorias_logic
        self.subcategorias_logic: ItensSubCategoriaLogic = subcategorias_logic
        self.itens_marcas_logic: ItensMarcasLogic = itens_marcas_logic


    def get_solicitacao_item_by_id(self, solicitacao_item_id: int) -> models.SolicitacoesItensModel | HTTPException:

        solicitacao_item = self.db.query(models.SolicitacoesItensModel).filter(
            models.SolicitacoesItensModel.id==solicitacao_item_id
        ).first()

        if solicitacao_item == None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Não existem Item de Solicitação com o ID {solicitacao_item_id}")
        
        return solicitacao_item
    

    def create_solicitacao_item(self, solicitacao_id: int, body: schemas.SolicitacoesItensBodySchema) -> models.SolicitacoesItensModel | HTTPException:    

        solicitacao = self.solicitacao_logic.get_solicitacao_by_id(solicitacao_id=solicitacao_id)
        participante = self.participante_logic.get_solicitacao_participante_by_id(solicitacao_participante_id=body.participanteID)

        new_solicitacao_item = models.SolicitacoesItensModel(
            solicitacaoID=solicitacao.id,
            criadoPor=participante.id,
            projecaoQuantidade=body.projecaoQuantidade,
            itemNome=body.itemNome,
            itemDescricao=body.itemDescricao,
            itemCategoria=body.itemUnidade,
            itemSubcategoria=body.itemSubcategoria,
            itemUnidade=body.itemUnidade,
            itemMarca=body.itemMarca,
        )
    
        new_solicitacao_item = self.create_solicitacao_referencia_if_exists(solicitacao_item=new_solicitacao_item, body=body)

        self.db.add(new_solicitacao_item)
        self.db.commit()
        self.db.refresh(new_solicitacao_item)

        return new_solicitacao_item
    

    def create_solicitacao_referencia_if_exists(self, solicitacao_item: models.SolicitacoesItensModel, body: schemas.SolicitacoesItensBodySchema) -> models.SolicitacoesItensModel:
        
        if body.itemReferenciaID is not None:
            item = self.itens_logic.get_item_by_id(item_id=body.itemReferenciaID)
            solicitacao_item.itemReferenciaID = item.id
        
        if body.categoriaReferenciaID is not None:
            categoria = self.categorias_logic.get_categoria_by_id(categoria_id=body.categoriaReferenciaID)
            solicitacao_item.categoriaReferenciaID = categoria.id

        if body.subcategoriaReferenciaID is not None:
            subcategoria = self.subcategorias_logic.get_sub_categoria_by_id(subcategoria_id=body.subcategoriaReferenciaID)
            solicitacao_item.subcategoriaReferenciaID = subcategoria.id
        
        if body.unidadeReferenciaID is not None:
            unidade = self.unidades_logic.get_unidade_by_id(unidade_id=body.unidadeReferenciaID)
            solicitacao_item.unidadeReferenciaID = unidade.id
        
        if body.marcaReferenciaID is not None:
            marca = self.itens_marcas_logic.get_marca_by_id(marca_id=body.marcaReferenciaID)
            solicitacao_item.marcaReferenciaID = marca.id

        return solicitacao_item    

    def update_solicitacao_referencia_if_exists(self, solicitacao_item_id: int, body: schemas.SolicitacoesItensReferenciasSchema) -> models.SolicitacoesItensModel | HTTPException:

        solicitacao_item = self.get_solicitacao_item_by_id(solicitacao_item_id=solicitacao_item_id)
        
        if body.itemReferenciaID is not None:
            item = self.itens_logic.get_item_by_id(item_id=body.itemReferenciaID)
            solicitacao_item.itemReferenciaID = item.id
        
        if body.categoriaReferenciaID is not None:
            categoria = self.categorias_logic.get_categoria_by_id(categoria_id=body.categoriaReferenciaID)
            solicitacao_item.categoriaReferenciaID = categoria.id

        if body.subcategoriaReferenciaID is not None:
            subcategoria = self.subcategorias_logic.get_sub_categoria_by_id(subcategoria_id=body.subcategoriaReferenciaID)
            solicitacao_item.subcategoriaReferenciaID = subcategoria.id
        
        if body.unidadeReferenciaID is not None:
            unidade = self.unidades_logic.get_unidade_by_id(unidade_id=body.unidadeReferenciaID)
            solicitacao_item.unidadeReferenciaID = unidade.id
        
        if body.marcaReferenciaID is not None:
            marca = self.itens_marcas_logic.get_marca_by_id(marca_id=body.marcaReferenciaID)
            solicitacao_item.marcaReferenciaID = marca.id

        self.db.add(solicitacao_item)
        self.db.commit()
        self.db.refresh(solicitacao_item)

        return solicitacao_item

    def get_solicitacao_itens(self, solicitacao_id: int) -> List[models.SolicitacoesItensModel] | HTTPException:

        solicitacao: models.SolicitacoesModel = self.solicitacao_logic.get_solicitacao_by_id(solicitacao_id=solicitacao_id)

        itens: List[models.SolicitacoesItensModel] = self.db.query(models.SolicitacoesItensModel).filter(
            models.SolicitacoesItensModel.solicitacaoID == solicitacao.id,
            models.SolicitacoesItensModel.deleted==False
        ).all()

        if itens == []:
            raise NoContentException()
        
        return itens
    

    def delete_solicitacao_itens(self, solicitacao_item_id: int) -> models.SolicitacoesItensModel | HTTPException:

        solicitacao_item = self.get_solicitacao_item_by_id(solicitacao_item_id=solicitacao_item_id)
        
        if solicitacao_item.deleted:
            return solicitacao_item
        
        solicitacao_item.deleted = True

        self.db.add(solicitacao_item)
        self.db.commit()
        self.db.refresh(solicitacao_item)

        return solicitacao_item
