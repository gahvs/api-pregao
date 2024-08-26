from fastapi import Depends, HTTPException
from database.instance import get_db
from sqlalchemy.orm import Session
from sqlalchemy import asc
from utils import errors
from typing import List
from itertools import chain
from collections import defaultdict
from http import HTTPStatus
from datetime import datetime, timedelta
from usuarios.logic import UserLogic
from usuarios.models import UserModel
from solicitacoes.logic import SolicitacaoLogic, SolicitacaoItensLogic, SolicitacaoParticipantesLogic
from solicitacoes.models import SolicitacoesModel, SolicitacoesItensModel, SolicitacoesParticipantesModel
from itens.logic import ItensLogic, ItensUnidadesLogic
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
                 pregao_logic: PregaoLogic = Depends(PregaoLogic)
                ) -> None:
        
        self.db: Session = db
        self.user_logic: UserLogic = user_logic
        self.pregao_logic: PregaoLogic = pregao_logic

    def get_pregao_participante_by_id(self, pregao_participante_id: int) -> models.PregaoParticipantesModel | HTTPException:

        pregao_participante = self.db.query(models.PregaoParticipantesModel).filter(
            models.PregaoParticipantesModel.id==pregao_participante_id
        ).first()

        if pregao_participante == None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=errors.not_found_message(resource_name="Participante de Pregão", resource_id=pregao_participante_id))
        
        return pregao_participante

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


    def create_pregao_participante(self, pregao_id: int, usuario_id: int, participante_tipo: str) -> models.PregaoParticipantesModel | HTTPException:

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
            participanteTipo=participante_tipo
        )

        self.db.add(new_pregao_participante)
        self.db.commit()
        self.db.refresh(new_pregao_participante)

        return new_pregao_participante
    

    def create_pregao_participante_comprador(self, pregao_id: int, body: schemas.PregaoParticipanteBodySchema) -> models.PregaoParticipantesModel | HTTPException:
        return self.create_pregao_participante(pregao_id=pregao_id, usuario_id=body.usuarioID, participante_tipo=self.PARTICIPANTE_COMPRADOR_TIPO)


    def create_pregao_participante_fornecedor(self, pregao_id: int, body: schemas.PregaoParticipanteBodySchema) -> models.PregaoParticipantesModel | HTTPException:
        return self.create_pregao_participante(pregao_id=pregao_id, usuario_id=body.usuarioID, participante_tipo=self.PARTICIPANTE_FORNECEDOR_TIPO)
    
    def participante_is_comprador(self, participante: models.PregaoParticipantesModel) -> bool:
        return participante.participanteTipo == self.PARTICIPANTE_COMPRADOR_TIPO
    

class PregaoItensLogic:
    '''
        Realiza operações envolvendo Pregões e Itens do Pregão.
        Principais operações:
        - Listagem dos Itens do Pregão
        - Adicionar Itens à um Pregão
        - Alterar Itens de um Pregão
        - Remover Itens de um Pregão
    '''    

    def __init__(self,
                    db: Session = Depends(get_db),
                    pregao_logic: PregaoLogic = Depends(PregaoLogic),
                    participantes_logic: PregaoParticipantesLogic = Depends(PregaoParticipantesLogic),
                    itens_logic: ItensLogic = Depends(ItensLogic),
                    unidades_logic: ItensUnidadesLogic = Depends(ItensUnidadesLogic)
            ) -> None:
        
        self.db: Session = db
        self.pregao_logic: PregaoLogic = pregao_logic
        self.participantes_logic: PregaoParticipantesLogic = participantes_logic
        self.itens_logic: ItensLogic = itens_logic
        self.unidades_logic: ItensUnidadesLogic = unidades_logic

    
    def get_pregao_item_by_id(self, pregao_item_id: int) -> models.PregaoItensModel | HTTPException:

        pregao_item = self.db.query(models.PregaoItensModel).filter(
            models.PregaoItensModel.id==pregao_item_id
        ).first()

        if pregao_item == None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=errors.not_found_message(resource_name="Item de Pregão", resource_id=pregao_item_id))
        
        return pregao_item
    
    def get_pregao_item_using_pregao_item(self, pregao_id: int, item_id: int) -> models.PregaoItensModel | HTTPException:

        pregao_item = self.db.query(models.PregaoItensModel).filter(
            models.PregaoItensModel.pregaoID==pregao_id,
            models.PregaoItensModel.itemID==item_id
        ).first()

        if pregao_item == None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        
        return pregao_item
    
    def pregao_item_already_setted(self, pregao_id: int, item_id: int) -> bool:

        pregao_item = self.db.query(models.PregaoItensModel).filter(
            models.PregaoItensModel.pregaoID==pregao_id,
            models.PregaoItensModel.itemID==item_id
        ).first()

        return pregao_item != None 

    def create_pregao_item(self, pregao_id: int, body: schemas.PregaoItensBodySchema) -> models.PregaoItensModel | HTTPException:

        if self.pregao_item_already_setted(pregao_id=pregao_id, item_id=body.itemID):
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Item já adicionado ao Pregão")
        
        pregao = self.pregao_logic.get_pregao_by_id(pregao_id=pregao_id)
        participante = self.participantes_logic.get_pregao_participante_by_id(pregao_participante_id=body.participanteID)
        item = self.itens_logic.get_item_by_id(item_id=body.itemID)
        unidade = self.unidades_logic.get_unidade_by_id(unidade_id=body.unidadeID)

        if not self.participantes_logic.participante_is_comprador(participante=participante):
            raise HTTPException(status_code=HTTPStatus.EXPECTATION_FAILED)
        
        new_pregao_item = models.PregaoItensModel(
            pregaoID=pregao.id,
            criadoPor=participante.id,
            itemID=item.id,
            unidadeID=unidade.id,
            projecaoQuantidade=body.projecaoQuantidade
        )

        self.db.add(new_pregao_item)
        self.db.commit()
        self.db.refresh(new_pregao_item)

        return new_pregao_item
    
    def update_pregao_item(self, pregao_item_id: int, body: schemas.PregaoItensBodyUpdateSchema) -> models.PregaoItensModel | HTTPException:

        pregao_item = self.get_pregao_item_by_id(pregao_item_id=pregao_item_id)
        if pregao_item.deleted:
            raise HTTPException(status_code=HTTPStatus.EXPECTATION_FAILED)
        
        pregao_item.projecaoQuantidade = body.projecaoQuantidade if body.projecaoQuantidade else pregao_item.projecaoQuantidade

        self.db.add(pregao_item)
        self.db.commit()
        self.db.refresh(pregao_item)

        return pregao_item
    
    def get_pregao_itens(self, pregao_id: int) -> List[models.PregaoItensModel] | HTTPException:

        pregao: models.PregaoModel = self.pregao_logic.get_pregao_by_id(pregao_id=pregao_id)

        itens: List[models.PregaoItensModel] = self.db.query(models.PregaoItensModel).filter(
            models.PregaoItensModel.pregaoID==pregao.id,
            models.PregaoItensModel.deleted==False
        ).all()

        if itens == []:
            raise HTTPException(status_code=HTTPStatus.NO_CONTENT)
        
        return itens
    
    def delete_pregao_item(self, pregao_item_id: int) -> models.PregaoItensModel | HTTPException:

        pregao_item = self.get_pregao_item_by_id(pregao_item_id=pregao_item_id)
        
        if pregao_item.deleted:
            return pregao_item
        
        pregao_item.deleted = True

        self.db.add(pregao_item)
        self.db.commit()
        self.db.refresh(pregao_item)

        return pregao_item


class PregaoLancesLogic: 

    '''
        Realiza as operações de Lances do Pregao
    '''

    REGRA_LANCE_DEFAULT = models.PregaoLancesRegrasModel(
        diferencaDeValorMinima=2.00,
        intervaloDeTempoEmMinutos=30,
        lancesPorIntervaloDeTempo=2,
    )

    def __init__(self,
                db: Session = Depends(get_db),
                pregao_logic: PregaoLogic = Depends(PregaoLogic),
                pregao_itens_logic: PregaoItensLogic = Depends(PregaoItensLogic),
                pregao_participantes_logic: PregaoParticipantesLogic = Depends(PregaoParticipantesLogic)     
            ) -> None:
        
        self.db: Session = db
        self.pregao_logic: PregaoLogic = pregao_logic
        self.pregao_itens_logic: PregaoItensLogic = pregao_itens_logic
        self.pregao_participantes_logic: PregaoParticipantesLogic = pregao_participantes_logic


    def get_lances_regra_ativa(self) -> models.PregaoLancesRegrasModel | HTTPException:

        regra: models.PregaoLancesRegrasModel = self.db.query(models.PregaoLancesRegrasModel).filter(
            models.PregaoLancesRegrasModel.ativa == True
        ).first()

        if regra == None:
            return self.REGRA_LANCE_DEFAULT
        
        return regra


    def get_lance_vencedor(self, pregao_id: int) -> models.PregaoLancesModel:

        lance_vencedor = (
            self.db.query(models.PregaoLancesModel).filter(
                models.PregaoLancesModel.pregaoID==pregao_id
            ).order_by(
                asc(models.PregaoLancesModel.valorLance), asc(models.PregaoLancesModel.dataHoraLance), asc(models.PregaoLancesModel.dataHoraRegistro)
            ).first()
        )

        return lance_vencedor

    def get_fornecedor_recent_lances(self, pregao_id: int, participante_id: int, intervalo_minutos: int) -> List[models.PregaoLancesModel]:

        data_hora_limite = datetime.now() - timedelta(minutes=intervalo_minutos)

        lances = (
            self.db.query(models.PregaoLancesModel).filter(
                models.PregaoLancesModel.pregaoID==pregao_id,
                models.PregaoLancesModel.participanteID==participante_id,
                models.PregaoLancesModel.dataHoraRegistro > data_hora_limite
            ).all()
        )

        return lances

    def create_pregao_lance(self, pregao_id: int, body: schemas.PregaoLancesBodySchema) -> models.PregaoLancesModel | HTTPException:

        pregao = self.pregao_logic.get_pregao_by_id(pregao_id=pregao_id)
        pregao_item = self.pregao_itens_logic.get_pregao_item_by_id(pregao_item_id=body.itemID)
        pregao_participante = self.pregao_participantes_logic.get_pregao_participante_by_id(pregao_participante_id=body.participanteID)

        if pregao_participante.participanteTipo != self.pregao_participantes_logic.PARTICIPANTE_FORNECEDOR_TIPO:
            raise HTTPException(status_code=HTTPStatus.EXPECTATION_FAILED, detail=f"O Participante {pregao_participante.id} do Pregão {pregao_id} não é {self.pregao_participantes_logic.PARTICIPANTE_FORNECEDOR_TIPO} do Pregão")

        # Aplicar aqui as restricoes de lance e verificoes de datas
        # Verificar status do Pregao para aceite de lances, etc.

        regra = self.get_lances_regra_ativa()
        lance_vencedor = self.get_lance_vencedor(pregao_id=pregao_id)
        
        if lance_vencedor is not None:

            # Verificando se o valor do lance é menor que o lance vencedor atual
            if body.valorLance > lance_vencedor.valorLance:
                raise HTTPException(status_code=HTTPStatus.EXPECTATION_FAILED, detail=f"Valor de Lance ({body.valorLance}) maior que o Lance Vencedor Atual ({lance_vencedor.valorLance})")
            
            # Verificando se a diferença mínima do valor do lance foi antendida
            diferenca_valor = abs(lance_vencedor.valorLance - body.valorLance)
            if diferenca_valor < regra.diferencaDeValorMinima:
                raise HTTPException(status_code=HTTPStatus.EXPECTATION_FAILED, detail=f"A diferença de Valor para o Lance Vencedor Atual é menor que o Limite Mínimo de {regra.diferencaDeValorMinima}")
            
            # Verificando se o numero máximo de lances por minuto não foi excedido
            fornecedor_lances = self.get_fornecedor_recent_lances(pregao_id=pregao, participante_id=body.participanteID, intervalo_minutos=regra.intervaloDeTempoEmMinutos)
            if len(fornecedor_lances) >= regra.lancesPorIntervaloDeTempo:
                raise HTTPException(status_code=HTTPStatus.EXPECTATION_FAILED, detail=f"Número máximo de Lances Excedido. Permitido são {regra.lancesPorIntervaloDeTempo} Lances a cada {regra.diferencaDeValorMinima} minutos")
        
        new_pregao_lance = models.PregaoLancesModel(
            pregaoID=pregao.id,
            participanteID=pregao_participante.id,
            itemID=pregao_item.id,
            valorLance=body.valorLance,
            dataHoraLance=body.dataHoraLance
        )

        self.db.add(new_pregao_lance)
        self.db.commit()
        self.db.refresh(new_pregao_lance)

        return new_pregao_lance


class PregaoConversoesLogic:

    '''
        Realiza as operações que criam Pregões através de Solicitacoes de Pregão
    '''

    def __init__(self,
                db: Session = Depends(get_db),
                user_logic: UserLogic = Depends(UserLogic),
                pregao_logic: PregaoLogic = Depends(PregaoLogic),
                pregao_participantes_logic: PregaoParticipantesLogic = Depends(PregaoParticipantesLogic),
                solicitacao_logic: SolicitacaoLogic = Depends(SolicitacaoLogic),
                solicitacao_participantes_logic: SolicitacaoParticipantesLogic = Depends(SolicitacaoParticipantesLogic),
                solicitacao_itens_logic: SolicitacaoItensLogic = Depends(SolicitacaoItensLogic)
            ) -> None:
        
        self.db: Session = db
        self.user_logic: UserLogic = user_logic
        self.pregao_logic: PregaoLogic = pregao_logic
        self.pregao_participantes_logic: PregaoParticipantesLogic = pregao_participantes_logic
        self.solicitacao_logic: SolicitacaoLogic = solicitacao_logic
        self.solicitacao_participantes_logic: SolicitacaoParticipantesLogic = solicitacao_participantes_logic
        self.solicitacao_itens_logic: SolicitacaoItensLogic = solicitacao_itens_logic

    def save_conversion(self, pregao_id: int, solicitacoes: List[int]) -> None:

        for solicitacao_id in solicitacoes:
            new_conversao = models.PregaoConversoesModel(
                pregaoID=pregao_id,
                solicitacaoID=solicitacao_id
            )  

            self.db.add(new_conversao)
            self.db.commit()

    def criar_pregao_por_conversao(self, body: schemas.PregaoCreateSchema) -> models.PregaoModel | HTTPException:

        if body.solicitacoes == []:
            raise HTTPException(status_code=HTTPStatus.EXPECTATION_FAILED, detail="É necessário enviar os ID's de Solicitação")
        
        solicitacoes = list(map(lambda solicitacao_id: self.solicitacao_logic.get_solicitacao_by_id(solicitacao_id=solicitacao_id), body.solicitacoes))
        for solicitacao in solicitacoes:
            if solicitacao.status == self.solicitacao_logic.STATUS_CONVERTIDO:
                raise HTTPException(status_code=HTTPStatus.EXPECTATION_FAILED, detail=f"Solicitacao {solicitacao.id} já convertida em Pregão")

        solicitacoes_itens = list(map(lambda solicitacao: self.solicitacao_itens_logic.get_solicitacao_itens(solicitacao_id=solicitacao.id), solicitacoes))
        solicitacoes_participantes = list(map(lambda solicitacao: self.solicitacao_participantes_logic.get_solicitacao_participantes(solicitacao_id=solicitacao.id), solicitacoes))

        pregao_itens = self.unifiy_solicitacao_itens_in_pregao_itens(solicitacao_itens=solicitacoes_itens)
        pregao_participantes = self.unify_solicitacao_participantes_in_pregao_participantes(solicitacao_participantes=solicitacoes_participantes)

        usuario = self.user_logic.get_user_by_id(user_id=body.usuarioID)

        new_pregao = models.PregaoModel(
            descricao=body.descricao,
            informacoes=body.informacoes,
            criadoPor=usuario.id,
            dataHoraInicio=body.dataHoraInicio,
            dataHoraFim=body.dataHoraFim,
            abertoADemandasEm=body.abertoADemandasEm,
            abertoADemandasAte=body.abertoADemandasAte
        )

        self.db.add(new_pregao)
        self.db.commit()
        self.db.refresh(new_pregao)

        # Adicionando Criador como Participante do Pregao
        criador_participante = self.pregao_participantes_logic.create_pregao_participante(pregao_id=new_pregao.id, usuario_id=usuario.id, participante_tipo=self.pregao_participantes_logic.PARTICIPANTE_COMPRADOR_TIPO)

        # Salvando Itens do Pregao importados das Solicitacoes
        for pregao_item in pregao_itens:
            pregao_item.pregaoID = new_pregao.id
            pregao_item.criadoPor = criador_participante.id
            self.db.add(pregao_item)
            self.db.commit()

        # Salvando Participantes do Pregao importados das Solicitacoes
        for pregao_participante in pregao_participantes:
            if pregao_participante.usuarioID != criador_participante.usuarioID:
                pregao_participante.pregaoID = new_pregao.id
                self.db.add(pregao_participante)
                self.db.commit()

        # Atualizando Status das Solicitacoes
        for solicitacao in solicitacoes:
            solicitacao.status = self.solicitacao_logic.STATUS_CONVERTIDO
            self.db.add(solicitacao)
            self.db.commit()

        # Registrando Conversoes
        self.save_conversion(pregao_id=new_pregao.id, solicitacoes=body.solicitacoes)

        return new_pregao


    def unifiy_solicitacao_itens_in_pregao_itens(self, solicitacao_itens: List[SolicitacoesItensModel]) -> List[models.PregaoItensModel] | HTTPException:

        # Unpacking Itens and group by Item id    

        itens_group = defaultdict(list)
        all_solicitacoes_itens = list(chain(*solicitacao_itens))
        
        for item in all_solicitacoes_itens:
             itens_group[item.itemID].append(item)        

        itens_matrix = list(itens_group.values())

        # Unify Itens in PregaoItens after Check 'Unidade' consistency

        pregao_itens: List[models.PregaoItensModel] = []

        for itens_group in itens_matrix:
            
            unidades = {item.unidadeID for item in itens_group}
            if len(unidades) > 1:
                raise HTTPException(status_code=HTTPStatus.EXPECTATION_FAILED, detail=f"O Item {itens_group[0].itemID} possui inconsistência de Unidade")
            
            item_sample = itens_group[0]

            pregao_itens.append(models.PregaoItensModel(
                itemID=item_sample.itemID,
                projecaoQuantidade=sum(item.projecaoQuantidade for item in itens_group),
                unidadeID=item_sample.unidadeID
            ))

        return pregao_itens
    
    def unify_solicitacao_participantes_in_pregao_participantes(self, solicitacao_participantes: List[SolicitacoesParticipantesModel]) -> List[models.PregaoParticipantesModel] | HTTPException:

        # Unpacking Participantes and group by Usuario ID
        participantes_group = defaultdict(list)
        all_participantes = list(chain(*solicitacao_participantes))

        for participante in all_participantes:
            participantes_group[participante.usuarioID].append(participante)

        participantes_matrix = list(participantes_group.values())

        # Unify Participantes in PregaoParticipantesModel after Check 'participanteTipo' consistency

        pregao_participantes: List[models.PregaoParticipantesModel] = []

        for participante_group in participantes_matrix:
            participacao_tipo = {participante.participanteTipo for participante in participante_group}
            if len(participacao_tipo) > 1:
                raise HTTPException(status_code=HTTPStatus.EXPECTATION_FAILED, detail=f"O Usuário {participante_group[0].usuarioID} possui inconsistência de Participação")
            
            participante_sample = participante_group[0]
            pregao_participantes.append(models.PregaoParticipantesModel(
                usuarioID=participante_sample.usuarioID,
                participanteTipo=participante_sample.participanteTipo
            ))

        return pregao_participantes