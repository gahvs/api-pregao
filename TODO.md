# Principais Atualizações:

## SOLICITACAO:
- ``EM ANDAMENTO`` Criar lógica de participantes da Solicitação, criando as entidades: ``PREGOES_SOLICITACOES_COMPRADORES`` & ``PREGOES_SOLICITACOES_FORNECEDORES``
**Tarefas**: 
    - Criar novas entidades no banco de dados seguindo estrutura do Pregão - ``DONE``
    - Criar classes *model* das entidades
    - Criar classes *schemas* das entidades
    - Criar classes *logic* para as entidades
    - Implementar operações de adicionar e remover Compradores e Fornecedores
    - Definir os *handlers* e *endpoints* das operações
            
---

## PREGAO:

- ``PARA FAZER`` Refazer lógica de participantes do Pregao, hoje a API trabalha com a tabela ``PREGAO_PARTICIPANTES``, mas o Banco foi atualizado com duas novas entidades: ``PREGOES_PREGAO_COMPRADORES`` & ``PREGOES_PREGAO_FORNECEDORES``

<BR>

- ``PARA FAZER`` Desenvolver fluxo 'Criar Pregão por Solicitacao'. Receberá o ID da Solicitação aprovada, campos adicionais que apenas o Pregão possui e irá realizar a criação do PREGAO usando os itens e participantes da Solicitação.